#!/usr/bin/env python3
"""
HTML Report Generator for LLM Benchmark Results
Converts JSON benchmark results into a formatted HTML report.
"""

import json
import argparse
import os
from datetime import datetime
from typing import Dict, Any


def load_benchmark_results(json_file: str) -> Dict[str, Any]:
    """Load benchmark results from JSON file."""
    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load JSON file: {e}")


def format_code(code: str) -> str:
    """Format code for HTML display."""
    if not code:
        return ""
    # Escape HTML characters and preserve formatting
    code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return code


def get_status_icon(status: str) -> str:
    """Get icon for exercise status."""
    icons = {
        'passed': '✅',
        'failed': '❌', 
        'error': '⚠️',
        'pending': '⏳'
    }
    return icons.get(status, '❓')


def get_status_class(status: str) -> str:
    """Get CSS class for status."""
    return f"status-{status}"


def generate_html_report(data: Dict[str, Any], output_file: str = None) -> str:
    """Generate HTML report from benchmark data."""
    
    stats = data['stats']
    exercises = data['exercises']
    
    # Generate output filename if not provided
    if not output_file:
        model_name = stats['model_name'].replace(':', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"benchmark_report_{model_name}_{timestamp}.html"
    
    # Calculate additional statistics
    total_time = stats['total_time']
    avg_time_per_exercise = total_time / stats['total_exercises'] if stats['total_exercises'] > 0 else 0
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM Benchmark Report - {stats['model_name']}</title>
    
    <!-- Highlight.js for syntax highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"></script>
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .report-header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .report-title {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .model-name {{
            font-size: 1.3em;
            color: #7f8c8d;
            margin-bottom: 20px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            border-left: 4px solid #3498db;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .success-rate {{
            font-size: 3em;
            font-weight: bold;
            color: #27ae60;
            margin: 20px 0;
        }}
        
        .exercises-container {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }}
        
        .section-title {{
            font-size: 2em;
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .exercise {{
            border: 1px solid #e1e8ed;
            border-radius: 12px;
            margin-bottom: 25px;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .exercise:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .exercise-header {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-bottom: 1px solid #e1e8ed;
        }}
        
        .exercise-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
        }}
        
        .exercise-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .difficulty {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        
        .difficulty-easy {{ background: #d4edda; color: #155724; }}
        .difficulty-medium {{ background: #fff3cd; color: #856404; }}
        .difficulty-hard {{ background: #f8d7da; color: #721c24; }}
        
        .attempt-info {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        .exercise-description {{
            padding: 15px 20px;
            background: #f8f9fa;
            font-style: italic;
            color: #495057;
        }}
        
        .attempts {{
            padding: 20px;
        }}
        
        .attempt {{
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
        }}
        
        .attempt:last-child {{
            margin-bottom: 0;
        }}
        
        .attempt-header {{
            padding: 12px 16px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .status-passed {{ background: #d4edda !important; color: #155724; }}
        .status-failed {{ background: #f8d7da !important; color: #721c24; }}
        .status-error {{ background: #fff3cd !important; color: #856404; }}
        
        .execution-time {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        /* Enhanced code block styling for syntax highlighting */
        .code-container {{
            position: relative;
            margin: 0;
        }}
        
        .code-header {{
            background: #21252b;
            color: #abb2bf;
            padding: 10px 16px;
            font-size: 0.85em;
            font-weight: 500;
            border-bottom: 1px solid #3a3f4b;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .code-language {{
            color: #61dafb;
        }}
        
        .copy-button {{
            background: #61dafb;
            color: #21252b;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            cursor: pointer;
            transition: background 0.2s;
        }}
        
        .copy-button:hover {{
            background: #4fa8c5;
        }}
        
        pre {{
            margin: 0 !important;
            background: #282c34 !important;
        }}
        
        pre code {{
            display: block;
            padding: 20px !important;
            font-family: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
            font-size: 0.9em !important;
            line-height: 1.5 !important;
            overflow-x: auto;
            background: transparent !important;
        }}
        
        /* Custom highlight.js overrides for better visibility */
        .hljs {{
            background: #282c34 !important;
            color: #abb2bf !important;
        }}
        
        .hljs-keyword,
        .hljs-built_in {{
            color: #c678dd !important;
        }}
        
        .hljs-string {{
            color: #98c379 !important;
        }}
        
        .hljs-number {{
            color: #d19a66 !important;
        }}
        
        .hljs-comment {{
            color: #5c6370 !important;
            font-style: italic;
        }}
        
        .hljs-function {{
            color: #61dafb !important;
        }}
        
        .hljs-variable,
        .hljs-attr {{
            color: #e06c75 !important;
        }}
        
        .error-message {{
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
            border-left: 4px solid #dc3545;
        }}
        
        .output-section {{
            padding: 15px;
            background: #f8f9fa;
        }}
        
        .output-label {{
            font-weight: bold;
            color: #495057;
            margin-bottom: 5px;
        }}
        
        .output-value {{
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            background: white;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #dee2e6;
        }}
        
        .summary-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin: 0 5px;
        }}
        
        .badge-success {{ background: #28a745; color: white; }}
        .badge-danger {{ background: #dc3545; color: white; }}
        .badge-warning {{ background: #ffc107; color: #212529; }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .report-header {{ padding: 20px; }}
            .exercises-container {{ padding: 20px; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .exercise-meta {{ flex-direction: column; align-items: flex-start; }}
            .code-header {{ flex-direction: column; gap: 8px; }}
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: white;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="report-header">
            <h1 class="report-title">🤖 LLM Benchmark Report</h1>
            <div class="model-name">Model: <strong>{stats['model_name']}</strong></div>
            
            <div class="success-rate">{stats['success_rate']:.1f}% Success Rate</div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{stats['total_exercises']}</div>
                    <div class="stat-label">Total Exercises</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['passed_exercises']}</div>
                    <div class="stat-label">Passed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['failed_exercises']}</div>
                    <div class="stat-label">Failed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['error_exercises']}</div>
                    <div class="stat-label">Errors</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['total_attempts']}</div>
                    <div class="stat-label">Total Attempts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['average_attempts']:.1f}</div>
                    <div class="stat-label">Avg Attempts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_time:.1f}s</div>
                    <div class="stat-label">Total Time</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{avg_time_per_exercise:.1f}s</div>
                    <div class="stat-label">Avg Time/Exercise</div>
                </div>
            </div>
        </div>
        
        <div class="exercises-container">
            <h2 class="section-title">📋 Exercise Results</h2>
"""
    
    # Add exercises
    for i, exercise in enumerate(exercises, 1):
        completed_badge = "✅ Completed" if exercise['completed'] else "❌ Failed"
        completed_class = "badge-success" if exercise['completed'] else "badge-danger"
        
        html_content += f"""
            <div class="exercise">
                <div class="exercise-header">
                    <div>
                        <div class="exercise-title">{i}. {exercise['name']}</div>
                        <div class="exercise-meta">
                            <span class="difficulty difficulty-{exercise['difficulty']}">{exercise['difficulty']}</span>
                            <span class="summary-badge {completed_class}">{completed_badge}</span>
                            <span class="attempt-info">{exercise['attempts']}/{exercise['max_attempts']} attempts</span>
                        </div>
                    </div>
                </div>
                
                <div class="exercise-description">
                    {exercise['description']}
                </div>
                
                <div class="attempts">
"""
        
        # Add attempts
        for attempt_num, result in enumerate(exercise['results'], 1):
            status_icon = get_status_icon(result['status'])
            status_class = get_status_class(result['status'])
            execution_time = result.get('execution_time', 0)
            
            html_content += f"""
                    <div class="attempt">
                        <div class="attempt-header {status_class}">
                            <span><strong>Attempt {attempt_num}</strong> {status_icon} {result['status'].title()}</span>
                            <span class="execution-time">⏱️ {execution_time:.2f}s</span>
                        </div>
"""
            
            # Add error message if present
            if result.get('error_message'):
                html_content += f"""
                        <div class="error-message">
                            <strong>Error:</strong> {result['error_message']}
                        </div>
"""
            
            # Add output information for failed tests
            if result['status'] == 'failed' and result.get('expected_output') and result.get('actual_output'):
                html_content += f"""
                        <div class="output-section">
                            <div class="output-label">Expected Output:</div>
                            <div class="output-value">{result['expected_output']}</div>
                            <div class="output-label" style="margin-top: 10px;">Actual Output:</div>
                            <div class="output-value">{result['actual_output']}</div>
                        </div>
"""
            
            # Add generated code with syntax highlighting
            if result.get('code_generated'):
                formatted_code = format_code(result['code_generated'])
                code_id = f"code_{i}_{attempt_num}"
                html_content += f"""
                        <div class="code-container">
                            <div class="code-header">
                                <span class="code-language">🐍 Python</span>
                                <button class="copy-button" onclick="copyCode('{code_id}')">📋 Copy</button>
                            </div>
                            <pre><code id="{code_id}" class="language-python hljs">{formatted_code}</code></pre>
                        </div>
"""
            
            html_content += "                    </div>\n"
        
        html_content += """
                </div>
            </div>
"""
    
    # Close HTML with JavaScript for syntax highlighting and copy functionality
    html_content += f"""
        </div>
    </div>
    
    <div class="footer">
        <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} by LLM Benchmarking Framework</p>
    </div>

    <script>
        // Initialize syntax highlighting
        document.addEventListener('DOMContentLoaded', function() {{
            hljs.highlightAll();
        }});
        
        // Copy code functionality
        function copyCode(elementId) {{
            const codeElement = document.getElementById(elementId);
            const text = codeElement.textContent;
            
            navigator.clipboard.writeText(text).then(function() {{
                // Visual feedback
                const button = event.target;
                const originalText = button.textContent;
                button.textContent = '✅ Copied!';
                button.style.background = '#28a745';
                
                setTimeout(function() {{
                    button.textContent = originalText;
                    button.style.background = '#61dafb';
                }}, 2000);
            }}).catch(function(err) {{
                console.error('Failed to copy: ', err);
                alert('Failed to copy code to clipboard');
            }});
        }}
        
        // Add smooth scrolling for better UX
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    return html_content, output_file


def main():
    """Main function to generate HTML report."""
    parser = argparse.ArgumentParser(description="Generate HTML report from LLM benchmark JSON results")
    parser.add_argument("json_file", help="Path to the benchmark results JSON file")
    parser.add_argument("-o", "--output", help="Output HTML file name")
    
    args = parser.parse_args()
    
    try:
        # Load benchmark results
        print(f"Loading benchmark results from {args.json_file}...")
        data = load_benchmark_results(args.json_file)
        
        # Add calculated stats
        stats = data['stats']
        stats['success_rate'] = (stats['passed_exercises'] / stats['total_exercises']) * 100 if stats['total_exercises'] > 0 else 0
        stats['average_attempts'] = stats['total_attempts'] / stats['total_exercises'] if stats['total_exercises'] > 0 else 0
        
        # Generate HTML report
        print("Generating HTML report...")
        html_content, output_file = generate_html_report(data, args.output)
        
        # Write HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML report generated successfully: {output_file}")
        print(f"📊 Summary: {stats['passed_exercises']}/{stats['total_exercises']} exercises passed ({stats['success_rate']:.1f}% success rate)")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 