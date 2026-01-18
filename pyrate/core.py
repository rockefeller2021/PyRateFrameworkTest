import re
import requests
import os
import time
import json
import base64
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from .exceptions import StepExecutionError, ElementNotFoundError, ApiConnectionError, DataFileError
from .logger import log_step, log_success, log_error, log_info, log_warning
from .assertions import Assertions
from .data_loader import load_dataset
from .report_generator import generate_report
from .evidence import EvidenceGenerator
from .config import PyRateConfig
from .validators import is_valid_url
from .selectors import SelectorStrategy, SelectorType


class PyRateRunner:
    def __init__(self, tags=None, config=None):
        """
        Initialize PyRate test runner.
        
        Args:
            tags: Optional tag filter for scenario execution (e.g., "@smoke")
            config: Optional PyRateConfig instance. If None, uses defaults.
        """
        load_dotenv()
        
        # Configuration
        self.config = config if config is not None else PyRateConfig()
        
        # Tag filtering
        self.tags_filter = tags.replace("'", "").replace('"', "").strip() if tags else None
        
        # Evidence generator with configurable folder
        self.evidence_gen = EvidenceGenerator(output_folder=self.config.evidence_folder)

        # Playwright instances
        self.playwright_engine = None
        self.browser_engine = None
        self._main_page = None  # Store main page for iframe context switchings


        # --- CONTEXTO BASE ---
        self.base_context = {
            "base_url": "",
            "response": None, 
            "response_json": {},
            "headers": self.config.default_headers.copy(),  # Use configured headers
            "vars": {}, 
            "auth": None, 
            "verify_ssl": self.config.verify_ssl,  # Use configured SSL verification
            "cert": None,
            "request_body": None, 
            "last_method": "UNKNOWN",
            "page": None
        }
        self.base_context['vars'].update(os.environ)

        self.execution_log = []
        self.is_success = True


    def execute_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            scenarios = self._parse_scenarios(lines)

            if self.tags_filter:
                all_tags = []
                for sc in scenarios: all_tags.extend([t.replace('#', '').replace('@', '').strip() for t in sc['tags']])
                if self.tags_filter.replace('@', '').strip() not in all_tags: return

            log_info(f"▶️ Procesando: {os.path.basename(file_path)}")

            dataset = [self.base_context['vars']]
            for line in lines[:10]:
                if match := re.match(r'Data source: (.*)', line, re.IGNORECASE):
                    path = match.group(1).strip().strip("'").strip('"')
                    log_info(f"📂 Modo Data-Driven: {path}")
                    dataset = load_dataset(path)
                    break

            for i, row in enumerate(dataset):
                iter_num = i + 1
                if len(dataset) > 1: log_info(f"--- Iteración {iter_num} ---")

                for sc in scenarios:
                    if self.tags_filter:
                        sc_tags = [t.replace('#', '').replace('@', '').strip() for t in sc['tags']]
                        if self.tags_filter.replace('@', '').strip() not in sc_tags: continue

                    log_info(f"🎬 Ejecutando Escenario: {sc['name']}")

                    self.context = self.base_context.copy()
                    self.context['vars'].update(row)

                    scenario_log = self._execute_lines(sc['steps'], iteration_idx=iter_num)
                    self.execution_log.extend(scenario_log)

                    try:
                        if self.context['page']:
                            path = self.evidence_gen.generate_ui_evidence(sc['name'], scenario_log, iteration=i)
                            log_success(f"📄 Evidencia UI: {path}")
                            try:
                                self.context['page'].close()
                            except Exception as e:
                                log_warning(f"No se pudo cerrar la página del navegador: {e}")
                        else:
                            resp = self.context.get('response_json', {})
                            method = self.context.get('last_method', 'N/A')
                            path = self.evidence_gen.generate_api_evidence(sc['name'], method, resp, iteration=i)
                            log_success(f"📄 Log API: {path}")
                    except Exception as ev_error:
                        log_error("EVIDENCIA", f"Error generando evidencia: {ev_error}")

        except Exception as e:
            self.is_success = False
            log_error("SISTEMA", str(e))
        finally:
            if self.execution_log:
                generate_report(self.execution_log, self.is_success)
            self._global_cleanup()

    def _parse_scenarios(self, lines):
        scenarios = []
        current_sc = {'name': 'Default', 'tags': [], 'steps': []}
        current_tags = []
        found_kw = False
        for line in lines:
            raw = line.strip()
            if not raw or raw.lower().startswith("data source:"): continue
            if re.match(r'^#?\s*@', raw):
                current_tags.append(raw.replace('#', '').strip())
                continue
            if raw.lower().startswith("scenario:"):
                if found_kw: scenarios.append(current_sc)
                found_kw = True
                current_sc = {'name': raw.split(":", 1)[1].strip(), 'tags': current_tags, 'steps': []}
                current_tags = []
                continue
            current_sc['steps'].append(raw)
        if current_sc['steps']: scenarios.append(current_sc)
        return scenarios


    def _execute_lines(self, lines, iteration_idx=1):
        """
        Execute Gherkin lines with optional descriptive comments.
        
        Supports optional descriptions before commands:
            # This is a description
            And input '#user' 'admin'
        
        The description will be used in evidence generation instead of raw command.
        Tags (# @smoke) are not captured as descriptions.
        """
        scenario_log = []
        pending_description = None  # Store description for next command
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip tags (e.g., @smoke, @ui)
            if line.startswith('@'):
                continue
            
            # Check if line is a comment
            if line.startswith('#'):
                # Distinguish between tags and descriptions
                # Tags: "# @smoke", "# @ui @regression"
                # Descriptions: "# Navigate to login page"
                if re.match(r'^#\s*@', line):
                    # It's a tag comment, skip it
                    continue
                else:
                    # It's a description, capture it
                    pending_description = line[1:].strip()  # Remove # and whitespace
                    continue

            processed_line = self._inject_vars(line)
            log_step(processed_line)

            step_record = {
                "iteration": iteration_idx,
                "name": pending_description if pending_description else processed_line,  # Use description if available
                "raw_command": processed_line,  # Keep original command for reference
                "status": "PASS",
                "error": None,
                "response_data": None,
                "screenshot": None,
                "screenshot_bytes": None
            }

            try:
                self._process_step(processed_line, step_record)
                if self.context['page']:
                    try:
                        step_record['screenshot_bytes'] = self.context['page'].screenshot()
                    except Exception as e:
                        log_warning(f"No se pudo capturar screenshot en paso exitoso: {e}")

            except Exception as e:
                step_record["status"] = "FAIL"
                step_record["error"] = str(e)
                self.is_success = False
                if self.context['page']:
                    try:
                        b = self.context['page'].screenshot()
                        step_record['screenshot_bytes'] = b
                        step_record['screenshot'] = base64.b64encode(b).decode('utf-8')
                    except Exception as e:
                        log_warning(f"No se pudo capturar screenshot en paso fallido: {e}")

                scenario_log.append(step_record)
                log_error("EJECUCIÓN", f"Paso fallido: {str(e)}")
                break

            scenario_log.append(step_record)
            
            # Reset pending description after use
            pending_description = None
            
        return scenario_log

    def _inject_vars(self, line):
        for key, value in self.context['vars'].items():
            if value is not None: line = line.replace(f"#({key})", str(value))
        return line

    def _global_cleanup(self):
        if self.browser_engine:
            try:
                self.browser_engine.close()
            except Exception as e:
                log_warning(f"Error cerrando el navegador: {e}")
            self.browser_engine = None
        if self.playwright_engine:
            try:
                self.playwright_engine.stop()
            except Exception as e:
                log_warning(f"Error deteniendo Playwright: {e}")
            self.playwright_engine = None

    def _resolve_value(self, expression):
        expression = expression.strip()
        if match := re.match(r"^read\(['\"](.*)['\"]\)$", expression, re.IGNORECASE):
            file_path = match.group(1)
            candidates = [file_path, os.path.join("data", file_path), os.path.join("features", file_path),
                          os.path.join("tests", "features", file_path)]
            found_path = None
            for p in candidates:
                if os.path.exists(p):
                    found_path = p
                    break

            if not found_path:
                raise DataFileError(f"Archivo no encontrado: {file_path}")

            try:
                with open(found_path, 'r', encoding='utf-8') as f:
                    if found_path.endswith('.json'): return json.load(f)
                    if found_path.endswith('.feature'): return f.readlines()
                    return f.read()
            except Exception as e:
                raise DataFileError(f"Error leyendo {found_path}: {str(e)}")
        return expression

    def _process_step(self, line, step_record):
        # 0. CALL READ (Modularidad)
        if match := re.match(r'\*?\s*call read\((.*)\)', line, re.IGNORECASE):
            raw_path = match.group(1).strip()
            feature_lines = self._resolve_value(f"read({raw_path})")
            if not isinstance(feature_lines, list):
                raise StepExecutionError(line, "El archivo llamado no es un feature válido")

            log_info(f"🔄 Llamando sub-feature...")
            sub_scenarios = self._parse_scenarios(feature_lines)
            for sub_sc in sub_scenarios:
                self._execute_lines(sub_sc['steps'], iteration_idx=step_record.get('iteration', 1))
            log_info(f"🔙 Retorno de llamada.")
            step_record['response_data'] = "Sub-feature ejecutado correctamente."
            return

        # 1. DEF (Variables) - ¡AHORA SOPORTA DOT NOTATION!
        if match := re.match(r'\*?\s*def (.*) = (.*)', line, re.IGNORECASE):
            var_name = match.group(1).strip()
            expression = match.group(2).strip()
            final_value = expression

            if expression == 'response':
                final_value = self.context.get('response_json') or (
                    self.context['response'].text if self.context.get('response') is not None else None)
            elif expression == 'responseStatus':
                final_value = self.context['response'].status_code if self.context.get('response') is not None else None
            # SOPORTE: response.id, response.token, etc.
            elif expression.startswith('response.'):
                path = expression.split('.', 1)[1]  # quitamos 'response.'
                act = self.context.get('response_json', {})
                try:
                    for k in path.split('.'):
                        if isinstance(act, list) and k.isdigit():
                            act = act[int(k)]
                        elif isinstance(act, dict):
                            act = act.get(k)
                        else:
                            act = None
                    final_value = act
                except:
                    final_value = None

            self.context['vars'][var_name] = final_value

        # 2. PRINT - ¡AHORA EVALÚA EXPRESIONES!
        elif match := re.match(r'\*?\s*print (.*)', line, re.IGNORECASE):
            expression = match.group(1).strip()
            content = expression

            # Keywords directos
            if expression == 'response':
                content = self.context.get('response_json') or "NULL"
            elif expression == 'responseStatus':
                content = self.context['response'].status_code if self.context.get('response') is not None else "NULL"
            else:
                # INTENTO DE EVALUACIÓN PYTHON (Para concatenación y variables)
                try:
                    # Creamos un contexto seguro con las variables disponibles
                    # Esto permite: print 'Hola ' + nombre
                    content = eval(expression, {}, self.context['vars'])
                except:
                    # Si falla el eval (ej: es texto simple sin comillas),
                    # verificamos si es una variable directa
                    if expression in self.context['vars']:
                        content = self.context['vars'][expression]
                    else:
                        # Si no, lo imprimimos tal cual
                        content = expression

            log_info(f"🖨️ [PRINT]: {content}")
            step_record['response_data'] = str(content)

        # 3. Configuración SSL y Auth
        elif match := re.match(r'configure ssl (true|false)', line, re.IGNORECASE):
            self.context['verify_ssl'] = (match.group(1).lower() == 'true')
        elif match := re.match(r'(?:Given|And)\s+auth basic (.*) (.*)', line, re.IGNORECASE):
            self.context['auth'] = HTTPBasicAuth(match.group(1).strip("'").strip('"'),
                                                 match.group(2).strip("'").strip('"'))
        elif match := re.match(r'(?:Given|And)\s+auth bearer (.*)', line, re.IGNORECASE):
            # Python 3.8+ compatible
            token = match.group(1).strip("'").strip('"')
            self.context['headers']['Authorization'] = f"Bearer {token}"

        # 4. API Requests
        elif match := re.match(r'Given url (.*)', line, re.IGNORECASE):
            self.context['base_url'] = match.group(1).strip("'").strip('"')

        elif match := re.match(r'(?:Given|And)\s+path\s+(.*)', line, re.IGNORECASE):
            base = self.context['base_url'].rstrip('/')
            # Python 3.8+ compatible - extract value outside f-string
            path_value = match.group(1).strip("'").strip('"').lstrip('/')
            self.context['base_url'] = f"{base}/{path_value}"

        elif match := re.match(r'(?:Given|And)\s+header\s+(.*) = (.*)', line, re.IGNORECASE):
            # Python 3.8+ compatible
            header_name = match.group(1).strip("'").strip('"')
            header_value = match.group(2).strip("'").strip('"')
            self.context['headers'][header_name] = header_value

        elif match := re.match(r'(?:Given|And)\s+request\s+(.*)', line, re.IGNORECASE):
            raw = match.group(1).strip()
            content = self._resolve_value(raw)
            if isinstance(content, (dict, list)):
                self.context['request_body'] = content
            else:
                try:
                    self.context['request_body'] = json.loads(content)
                except:
                    raise StepExecutionError(line, "JSON inválido o error en read()")

        # 5. EXECUTE METHOD
        elif match := re.match(r'(?:When|And)\s+method\s+(.*)', line, re.IGNORECASE):
            method = match.group(1).strip().upper()
            print(f"📢 [DEBUG] Ejecutando Método: {method} en URL: {self.context['base_url']}")
            self.context['last_method'] = method
            try:
                res = requests.request(
                    method, 
                    self.context['base_url'], 
                    headers=self.context['headers'],
                    json=self.context.get('request_body'), 
                    auth=self.context['auth'],
                    verify=self.context['verify_ssl'],
                    timeout=self.config.api_timeout  # Use configured API timeout
                )
                self.context['request_body'] = None
                self.context['response'] = res
                try:
                    j = res.json()
                    self.context['response_json'] = j
                    step_record['response_data'] = json.dumps(j, indent=2, ensure_ascii=False)
                except:
                    self.context['response_json'] = {}
                    step_record['response_data'] = res.text[:500]
            except Exception as e:
                raise ApiConnectionError(str(e))

        # 6. Validaciones
        elif match := re.match(r'Then status (\d+)', line, re.IGNORECASE):
            exp = int(match.group(1))
            if self.context.get('response') is not None:
                act_code = self.context['response'].status_code
                act_body = self.context.get('response_json') or self.context['response'].text
            else:
                act_code = "N/A"
                act_body = "Sin respuesta"

            debug_info = f"Esperado: {exp} | Recibido: {act_code}\nBody: {act_body}"
            step_record['response_data'] = debug_info
            if act_code != exp: raise AssertionError(f"Status Incorrecto. {debug_info}")

        elif match := re.match(r'(?:Then|And)\s+match response\.(.*) == (.*)', line, re.IGNORECASE):
            path, exp = match.group(1).strip(), match.group(2).strip().strip("'").strip('"')
            act = self.context['response_json']
            try:
                for k in path.split('.'): act = act[int(k)] if isinstance(act, list) and k.isdigit() else act[k]
            except:
                act = None
            Assertions.match(act, exp)
        elif match := re.match(r'(?:Then|And)\s+match response == (.*)', line, re.IGNORECASE):
            try:
                Assertions.match(self.context['response_json'], json.loads(match.group(1).strip()))
            except:
                Assertions.match(str(self.context['response_json']), match.group(1).strip())

        # 7. UI (PLAYWRIGHT)
        elif match := re.match(r'Given driver (.*)', line, re.IGNORECASE):
            url = match.group(1).strip("'").strip('"')
            if not self.playwright_engine:
                self.playwright_engine = sync_playwright().start()
                self.browser_engine = self.playwright_engine.chromium.launch(
                    headless=self.config.headless  # Use configured headless mode
                )
            context = self.browser_engine.new_context()
            self.context['page'] = context.new_page()
            self._main_page = self.context['page']  # Store main page reference
            # Use configured browser timeout
            self.context['page'].goto(url, timeout=self.config.browser_timeout)

        elif match := re.match(r'(?:Given|And)\s+input (.*) (.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            value = match.group(2).strip("'").strip('"')
            
            # Parse selector (CSS or XPath)
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").fill(value)
            else:
                self.context['page'].fill(selector, value)
        elif match := re.match(r'(?:Given|And)\s+click (.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            
            # Parse selector (CSS or XPath)
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").click()
            else:
                self.context['page'].click(selector)
        elif match := re.match(r'(?:Given|And)\s+wait (\d+)', line, re.IGNORECASE):
            time.sleep(int(match.group(1)))
        elif match := re.match(r'(?:Then|And)\s+match text (.*) == (.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            expected_text = match.group(2).strip("'").strip('"')
            
            # Parse selector (CSS or XPaths)
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                act = self.context['page'].locator(f"xpath={selector}").inner_text()
            else:
                act = self.context['page'].inner_text(selector)
            
            if expected_text not in act:
                raise AssertionError(f"Texto no coincide. Esperado: '{expected_text}' en '{act}'")

        # ========================================
        # SCROLL COMMANDS (Sprint 3)
        # ========================================
        elif 'scroll to' in line.lower():
            if match := re.match(r'(?:Given|And)\s+scroll to element\s+(.*)', line, re.IGNORECASE):
                selector_raw = match.group(1).strip("'").strip('"')
                selector_type, selector = SelectorStrategy.parse(selector_raw)
                
                if selector_type == SelectorType.XPATH:
                    self.context['page'].locator(f"xpath={selector}").scroll_into_view_if_needed()
                else:
                    self.context['page'].locator(selector).scroll_into_view_if_needed()
                    
            elif 'scroll to top' in line.lower():
                self.context['page'].evaluate("window.scrollTo(0, 0)")
                
            elif 'scroll to bottom' in line.lower():
                self.context['page'].evaluate("window.scrollTo(0, document.body.scrollHeight)")
                
            elif match := re.match(r'(?:Given|And)\s+scroll to\s+(\d+)\s*,\s*(\d+)', line, re.IGNORECASE):
                x = int(match.group(1))
                y = int(match.group(2))
                self.context['page'].evaluate(f"window.scrollTo({x}, {y})")

        # ========================================
        # DROPDOWN/SELECT COMMANDS (Sprint 3)
        # ========================================
        elif match := re.match(r'(?:Given|And)\s+select\s+(.*)\s+by text\s+(.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            text = match.group(2).strip("'").strip('"')
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").select_option(label=text)
            else:
                self.context['page'].select_option(selector, label=text)
                
        elif match := re.match(r'(?:Given|And)\s+select\s+(.*)\s+by value\s+(.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            value = match.group(2).strip("'").strip('"')
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").select_option(value=value)
            else:
                self.context['page'].select_option(selector, value=value)
                
        elif match := re.match(r'(?:Given|And)\s+select\s+(.*)\s+by index\s+(\d+)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            index = int(match.group(2))
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").select_option(index=index)
            else:
                self.context['page'].select_option(selector, index=index)

        # ========================================
        # CHECKBOX COMMANDS (Sprint 3)
        # ========================================
        elif match := re.match(r'(?:Given|And)\s+check\s+(.*)', line, re.IGNORECASE):
            if 'radio' not in line.lower():  # Avoid conflict with radio buttons
                selector_raw = match.group(1).strip("'").strip('"')
                selector_type, selector = SelectorStrategy.parse(selector_raw)
                
                if selector_type == SelectorType.XPATH:
                    self.context['page'].locator(f"xpath={selector}").check()
                else:
                    self.context['page'].locator(selector).check()
                    
        elif match := re.match(r'(?:Given|And)\s+uncheck\s+(.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").uncheck()
            else:
                self.context['page'].locator(selector).uncheck()
                
        elif match := re.match(r'(?:Given|And)\s+toggle\s+(.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                checkbox = self.context['page'].locator(f"xpath={selector}")
            else:
                checkbox = self.context['page'].locator(selector)
                
            # Toggle logic
            if checkbox.is_checked():
                checkbox.uncheck()
            else:
                checkbox.check()

        # ========================================
        # RADIO BUTTON COMMANDS (Sprint 3)
        # ========================================
        elif match := re.match(r'(?:Given|And)\s+check radio\s+(.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            selector_type, selector = SelectorStrategy.parse(selector_raw)
            
            if selector_type == SelectorType.XPATH:
                self.context['page'].locator(f"xpath={selector}").check()
            else:
                self.context['page'].locator(selector).check()

        # ========================================
        # IFRAME COMMANDS (Sprint 3)
        # ========================================
        elif match := re.match(r'(?:Given|And)\s+switch to frame\s+(.*)', line, re.IGNORECASE):
            selector_raw = match.group(1).strip("'").strip('"')
            
            # Check if it's an index (number)
            if selector_raw.isdigit():
                frame_index = int(selector_raw)
                frames = self.context['page'].frames
                if frame_index < len(frames):
                    self.context['page'] = frames[frame_index]
                else:
                    raise ValueError(f"Frame index {frame_index} out of range")
            else:
                # Selector-based frame switching
                selector_type, selector = SelectorStrategy.parse(selector_raw)
                
                if selector_type == SelectorType.XPATH:
                    frame_locator = self.context['page'].frame_locator(f"xpath={selector}")
                else:
                    frame_locator = self.context['page'].frame_locator(selector)
                    
                # Note: Playwright's frame_locator returns a FrameLocator for chaining
                # Store it as the current page context
                self.context['page'] = frame_locator
                
        elif 'switch to default' in line.lower() or 'switch to main' in line.lower():
            # Return to main page context
            if self._main_page:
                self.context['page'] = self._main_page
                
        elif 'switch to parent' in line.lower():
            # Return to parent frame (simplified: return to main)
            if self._main_page:
                self.context['page'] = self._main_page

        # ========================================
        # POPUP/ALERT COMMANDS (Sprint 3)
        # ========================================
        elif 'accept alert' in line.lower():
            def handle_dialog(dialog):
                dialog.accept()
            self.context['page'].on("dialog", handle_dialog)
            
        elif 'dismiss alert' in line.lower():
            def handle_dialog(dialog):
                dialog.dismiss()
            self.context['page'].on("dialog", handle_dialog)
            
        elif match := re.match(r'(?:Then|And)\s+match alert text\s+==\s+(.*)', line, re.IGNORECASE):
            expected_text = match.group(1).strip("'").strip('"')
            captured_text = None
            
            def handle_dialog(dialog):
                nonlocal captured_text
                captured_text = dialog.message
                dialog.accept()
                
            self.context['page'].on("dialog", handle_dialog)
            
            time.sleep(0.5)  # Wait for dialog to appear
            
            if captured_text != expected_text:
                raise AssertionError(
                    f"Alert text mismatch. Expected: '{expected_text}', Got: '{captured_text}'"
                )
                
        elif match := re.match(r'(?:Given|And)\s+type in prompt\s+(.*)', line, re.IGNORECASE):
            prompt_text = match.group(1).strip("'").strip('"')
            
            def handle_dialog(dialog):
                dialog.accept(prompt_text)
                
            self.context['page'].on("dialog", handle_dialog)
        else:
            raise StepExecutionError(line, "Comando desconocido")