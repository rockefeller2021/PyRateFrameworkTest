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
        scenario_log = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('@'): continue

            processed_line = self._inject_vars(line)
            log_step(processed_line)

            step_record = {
                "iteration": iteration_idx,
                "name": processed_line, "status": "PASS", "error": None,
                "response_data": None, "screenshot": None, "screenshot_bytes": None
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
            self.context['headers']['Authorization'] = f"Bearer {match.group(1).strip("'").strip('"')}"

        # 4. API Requests
        elif match := re.match(r'Given url (.*)', line, re.IGNORECASE):
            self.context['base_url'] = match.group(1).strip("'").strip('"')

        elif match := re.match(r'(?:Given|And)\s+path\s+(.*)', line, re.IGNORECASE):
            base = self.context['base_url'].rstrip('/')
            self.context['base_url'] = f"{base}/{match.group(1).strip("'").strip('"').lstrip('/')}"

        elif match := re.match(r'(?:Given|And)\s+header\s+(.*) = (.*)', line, re.IGNORECASE):
            self.context['headers'][match.group(1).strip("'").strip('"')] = match.group(2).strip("'").strip('"')

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
            # Use configured browser timeout
            self.context['page'].goto(url, timeout=self.config.browser_timeout)

        elif match := re.match(r'(?:Given|And)\s+input (.*) (.*)', line, re.IGNORECASE):
            self.context['page'].fill(match.group(1).strip("'").strip('"'), match.group(2).strip("'").strip('"'))
        elif match := re.match(r'(?:Given|And)\s+click (.*)', line, re.IGNORECASE):
            self.context['page'].click(match.group(1).strip("'").strip('"'))
        elif match := re.match(r'(?:Given|And)\s+wait (\d+)', line, re.IGNORECASE):
            time.sleep(int(match.group(1)))
        elif match := re.match(r'(?:Then|And)\s+match text (.*) == (.*)', line, re.IGNORECASE):
            act = self.context['page'].inner_text(match.group(1).strip("'").strip('"'))
            if match.group(2).strip("'").strip('"') not in act: raise AssertionError(f"Texto no coincide")
        else:
            raise StepExecutionError(line, "Comando desconocido")