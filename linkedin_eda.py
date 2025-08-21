import pandas as pd

# Load LinkedIn dataset
df = pd.read_csv('data/LinkedInData.csv')

# Simple EDA
summary = df.describe(include='all')

# Generate HTML report in data folder and open in Chrome
import os
import webbrowser
project_dir = os.path.dirname(os.path.abspath(__file__))
html_dir = os.path.join(project_dir, 'html_reports')
os.makedirs(html_dir, exist_ok=True)
print(f"html_reports directory path: {html_dir}")
print(f"Directory exists: {os.path.isdir(html_dir)}")
print(f"Directory contents: {os.listdir(project_dir)}")
report_path = os.path.join(html_dir, 'LinkedIn_report.html')
print(f"Attempting to write report to: {report_path}")
try:
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('<html><head><link rel="stylesheet" href="../style.css"></head><body>')
        f.write('<h1>LinkedIn Job Data EDA Report</h1>')
        f.write(df.head().to_html(index=False, classes='data-table'))
        f.write('<h2>Summary Statistics</h2>')
        f.write(summary.to_html(classes='data-table'))
        f.write('</body></html>')
    webbrowser.get('windows-default').open(report_path)
    print(f"Report successfully written to: {report_path}")
except Exception as e:
    print(f"Failed to write report: {e}")
