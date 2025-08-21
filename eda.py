

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO

# Load the dataset
df = pd.read_csv("data/NaukriData_data_analytics.csv", encoding='latin1')

# Drop rows with missing important data
df.dropna(subset=["Job_Titles", "Skills", "Locations"], inplace=True)

# Prepare HTML report
html = ['<html><head><link rel="stylesheet" href="style.css"></head><body>']
html.append('<h1>Naukri Data Analytics EDA Report</h1>')
html.append('<h2>Sample Data</h2>')
html.append(df.head().to_html(index=False, classes='data-table'))
html.append('<h2>Summary Statistics</h2>')
html.append(df.describe(include="all").to_html(classes='data-table'))

# Top 10 Job Titles
top_titles = df["Job_Titles"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_titles.values, y=top_titles.index, palette="Blues_d")
plt.title("Top 10 Job Titles")
plt.xlabel("Number of Postings")
plt.ylabel("Job Title")
plt.tight_layout()
buf = BytesIO()
plt.savefig(buf, format='png')
plt.close()
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')
html.append('<h2>Top 10 Job Titles</h2>')
html.append(f'<img src="data:image/png;base64,{img_base64}"/>')

# Top Hiring Locations
top_locations = df["Locations"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_locations.values, y=top_locations.index, palette="Greens_d")
plt.title("Top Hiring Cities")
plt.xlabel("Number of Jobs")
plt.ylabel("Location")
plt.tight_layout()
buf = BytesIO()
plt.savefig(buf, format='png')
plt.close()
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')
html.append('<h2>Top Hiring Cities</h2>')
html.append(f'<img src="data:image/png;base64,{img_base64}"/>')

# Word Cloud for Skills
text = " ".join(df["Skills"].dropna().astype(str).tolist())
wordcloud = WordCloud(width=1000, height=600, background_color='white').generate(text)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most In-Demand Skills")
buf = BytesIO()
plt.savefig(buf, format='png')
plt.close()
buf.seek(0)
img_base64 = base64.b64encode(buf.read()).decode('utf-8')
html.append('<h2>Most In-Demand Skills (Word Cloud)</h2>')
html.append(f'<img src="data:image/png;base64,{img_base64}"/>')

html.append('</body></html>')


# Always save report in the script's directory
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
if not os.path.isdir(data_dir):
	print(f"ERROR: Data folder does not exist: {data_dir}")
else:
	report_path = os.path.join(data_dir, 'Naukri_report.html')
	print(f"Attempting to write HTML report to: {report_path}")
	try:
		with open(report_path, 'w', encoding='utf-8') as f:
			f.write('\n'.join(html))
		print(f"Report successfully written to: {report_path}")
		# Open in Chrome automatically (Windows)
		import webbrowser
		webbrowser.get('windows-default').open(report_path)
	except Exception as e:
		print(f"Failed to write report: {e}")
