"""
Report generation utilities for PyRate Framework.

Generates interactive HTML reports with execution metrics, step details,
screenshots, and iteration grouping for data-driven tests.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import traceback
import json
from collections import defaultdict


def generate_report(execution_log: List[Dict[str, Any]], is_success: bool) -> None:
    """
    Generate interactive HTML report from execution log.
    
    Creates a beautiful, interactive HTML dashboard with:
    - Execution metrics (pass/fail counts, success rate)
    - Steps grouped by iteration (for data-driven tests)
    - Screenshots embedded in collapsible sections
    - Color-coded pass/fail indicators
    
    Args:
        execution_log: List of step execution records
        is_success: Overall execution success status
        
    Example:
        >>> log = [
        ...     {"name": "Get users", "status": "PASS", "iteration": 1},
        ...     {"name": "Verify response", "status": "PASS", "iteration": 1}
        ... ]
        >>> generate_report(log, is_success=True)
    """
    print("\n📢 [DEBUG] Generando Dashboard Agrupado por Iteraciones...")

    try:
        # 1. Crear directorio
        if not os.path.exists("reports"):
            os.makedirs("reports")

        # 2. Métricas y Datos Generales
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")

        # 3. AGRUPACIÓN POR ITERACIÓN (Test Cases)
        iterations_map = defaultdict(list)
        for step in execution_log:
            it_num = step.get('iteration', 1)
            iterations_map[it_num].append(step)

        # ========================================
        # MÉTRICAS POR TEST CASES (NO POR PASOS)
        # ========================================
        total_test_cases = len(iterations_map)
        passed_test_cases = 0
        failed_test_cases = 0
        
        # Contar test cases exitosos y fallidos
        for it_num, steps in iterations_map.items():
            # Un test case FALLA si CUALQUIER paso falla
            has_failure = any(s.get('status') == 'FAIL' for s in steps)
            if has_failure:
                failed_test_cases += 1
            else:
                passed_test_cases += 1
        
        # Calcular efectividad por test cases
        success_rate = round((passed_test_cases / total_test_cases) * 100, 2) if total_test_cases > 0 else 0
        global_color = "#27ae60" if success_rate == 100 else "#e67e22" if success_rate >= 50 else "#e74c3c"
        global_status = "EXITOSO" if is_success else "FALLIDO"
        
        # Contar pasos totales para el pie chart
        total_steps = len(execution_log)
        passed_steps = sum(1 for s in execution_log if s.get('status') != 'FAIL')
        failed_steps = total_steps - passed_steps

        # 4. Construcción del HTML por Test Cases
        iterations_html = ""

        for it_num, steps in sorted(iterations_map.items()):
            # Verificamos si esta iteración tuvo fallos para pintar el borde rojo o verde
            it_has_fail = any(s['status'] == 'FAIL' for s in steps)
            it_color = "#e74c3c" if it_has_fail else "#27ae60"
            it_icon = "❌" if it_has_fail else "✅"
            it_status = "FALLIDO" if it_has_fail else "EXITOSO"  # <-- AÑADIDO

            # Tabla interna de la iteración
            rows_html = ""
            for i, step in enumerate(steps):
                status_badge = '<span class="badge bg-pass">PASS</span>'
                row_class = ""
                if step['status'] == 'FAIL':
                    status_badge = '<span class="badge bg-fail">FAIL</span>'
                    row_class = "row-fail"

                details_html = ""
                if step.get('error'):
                    details_html += f'<div class="error-msg">❌ {step["error"]}</div>'

                if step.get('response_data'):
                    content = str(step['response_data'])
                    if "<html" in content or "<!DOCTYPE" in content:
                        content = content.replace("<", "&lt;").replace(">", "&gt;")
                    details_html += f"<details><summary>📦 Ver Datos</summary><pre>{content}</pre></details>"

                if step.get('screenshot'):
                    details_html += f"<div class='screenshot-box'><details><summary>📷 Ver Captura</summary><img src='data:image/png;base64,{step['screenshot']}' /></details></div>"

                rows_html += f"""
                <tr class="{row_class}">
                    <td style="text-align: center;">{i + 1}</td>
                    <td>{step['name']}</td>
                    <td style="text-align: center;">{status_badge}</td>
                    <td>{details_html}</td>
                </tr>
                """

            # Bloque HTML del Test Case Completo
            iterations_html += f"""
            <div class="iteration-card" style="border-left: 5px solid {it_color};">
                <div class="iteration-header">
                    <h3>{it_icon} Test Case #{it_num} - {it_status}</h3>
                    <span class="step-count">{len(steps)} pasos</span>
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 5%">#</th>
                                <th style="width: 40%">Paso</th>
                                <th style="width: 10%; text-align: center;">Estado</th>
                                <th style="width: 45%">Datos</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
            """

        # 5. Plantilla HTML Final
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte PyRate</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                :root {{ --primary: #2c3e50; --success: #27ae60; --fail: #e74c3c; --bg: #f8f9fa; }}
                body {{ font-family: 'Inter', sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}

                /* HEADER */
                .header {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid {global_color}; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
                .header h1 {{ margin: 0; font-size: 1.5rem; color: var(--primary); }}
                .badge {{ padding: 5px 12px; border-radius: 20px; font-weight: 700; color: white; }}

                /* METRICS */
                .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
                .card .value {{ font-size: 2rem; font-weight: 700; color: var(--primary); }}
                .card.pass .value {{ color: var(--success); }} .card.fail .value {{ color: var(--fail); }}

                /* ITERATION CARDS */
                .iteration-card {{ background: white; margin-bottom: 30px; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
                .iteration-header {{ background: #fff; padding: 15px 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }}
                .iteration-header h3 {{ margin: 0; font-size: 1.1rem; color: var(--primary); }}
                .step-count {{ background: #eee; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; }}

                /* TABLE */
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ text-align: left; padding: 12px 15px; background: #f8f9fa; color: #666; font-size: 0.9rem; }}
                td {{ padding: 12px 15px; border-bottom: 1px solid #eee; vertical: top; font-size: 0.9rem; }}
                .row-fail {{ background-color: #fdedec; }}

                .bg-pass {{ background: var(--success); }} .bg-fail {{ background: var(--fail); }}
                details {{ margin-top: 5px; }} summary {{ color: #3498db; font-weight: 600; cursor: pointer; }}
                pre {{ background: #2d3436; color: #dfe6e9; padding: 10px; border-radius: 5px; overflow-x: auto; max-height: 300px; font-size: 0.8rem; margin-top: 5px; }}
                
                /* FILTER BUTTONS */
                .filter-btn {{ background: white; border: 2px solid #ddd; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-size: 0.9rem; transition: all 0.3s; }}
                .filter-btn:hover {{ background: #f8f9fa; border-color: #bbb; }}
                .filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div><h1>🚀 Reporte de Ejecución PyRate</h1><div>{formatted_date}</div></div>
                    <span class="badge" style="background: {global_color}; font-size: 1rem;">{global_status}</span>
                </div>

                <div class="dashboard">
                    <div class="card"><h3>Total Test Cases</h3><div class="value">{total_test_cases}</div></div>
                    <div class="card pass"><h3>Test Cases Exitosos</h3><div class="value">{passed_test_cases}</div></div>
                    <div class="card fail"><h3>Test Cases Fallidos</h3><div class="value">{failed_test_cases}</div></div>
                    <div class="card"><h3>Efectividad</h3><div class="value" style="color: {global_color}">{success_rate}%</div></div>
                </div>

                <!-- Pie Chart -->
                <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h2 style="color: #2c3e50; text-align: center; margin-bottom: 20px;">📊 Distribución de Resultados</h2>
                    <div style="max-width: 400px; margin: 0 auto;">
                        <canvas id="resultChart"></canvas>
                    </div>
                </div>

                <!-- Filtros -->
                <div style="background: white; padding: 15px 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; gap: 15px; align-items: center;">
                    <span style="font-weight: 600; color: #2c3e50;">🔍 Filtrar:</span>
                    <button onclick="filterIterations('all')" class="filter-btn active" id="btn-all">Todos ({total_test_cases})</button>
                    <button onclick="filterIterations('pass')" class="filter-btn" id="btn-pass">✅ Exitosos ({passed_test_cases})</button>
                    <button onclick="filterIterations('fail')" class="filter-btn" id="btn-fail">❌ Fallidos ({failed_test_cases})</button>
                </div>

                <h2 style="color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px;">Detalle por Test Case</h2>

                {iterations_html}

            </div>

            <script>
                // Pie Chart
                const ctx = document.getElementById('resultChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'pie',
                    data: {{
                        labels: ['Pasos Exitosos', 'Pasos Fallidos'],
                        datasets: [{{
                            data: [{passed_steps}, {failed_steps}],
                            backgroundColor: ['#27ae60', '#e74c3c'],
                            borderWidth: 2,
                            borderColor: '#fff'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 15,
                                    font: {{ size: 14 }}
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const label = context.label || '';
                                        const value = context.parsed || 0;
                                        const total = {total_steps};
                                        const percentage = ((value / total) * 100).toFixed(1);
                                        return label + ': ' + value + ' (' + percentage + '%)';
                                    }}
                                }}
                            }}
                        }}
                    }}
                }});

                // Filtros
                function filterIterations(type) {{
                    const cards = document.querySelectorAll('.iteration-card');
                    const buttons = document.querySelectorAll('.filter-btn');
                    
                    // Remove active class from all buttons
                    buttons.forEach(btn => btn.classList.remove('active'));
                    
                    // Add active to clicked button
                    document.getElementById('btn-' + type).classList.add('active');
                    
                    cards.forEach(card => {{
                        if (type === 'all') {{
                            card.style.display = 'block';
                        }} else if (type === 'pass') {{
                            // Show only cards with green border (all passed)
                            const borderColor = card.style.borderLeftColor;
                            card.style.display = borderColor.includes('39, 174, 96') ? 'block' : 'none';
                        }} else if (type === 'fail') {{
                            // Show only cards with red border (has failures)
                            const borderColor = card.style.borderLeftColor;
                            card.style.display = borderColor.includes('231, 76, 60') ? 'block' : 'none';
                        }}
                    }});
                }}
            </script>
        </body>
        </html>
        """

        # 6. Guardar archivos
        filename = f"reports/report_{timestamp}.html"
        latest_filename = "reports/ultimo_reporte.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        with open(latest_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("\n✅ REPORTE AGRUPADO GENERADO CORRECTAMENTE.")

    except Exception as e:
        print("\n❌ ERROR GENERANDO REPORTE:")
        traceback.print_exc()