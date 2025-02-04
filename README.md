##Python Automation Scripts

1. Web Scraper for Books Data
Description:

This script scrapes book data (title, price, availability, rating, and product URL) from http://books.toscrape.com and saves it to a CSV file. 
Additionally, it visualizes the data with bar charts showing:
Number of books by rating.
Average price by availability.
Instructions

Setup:
Ensure Python 3.7+ is installed on your system.
Install required libraries:
##pip install requests beautifulsoup4 pandas matplotlib
Run the Script:
##Save the script as web_scraper.py.
Execute the script:
##python web_scraper.py
Outputs:
##sales_data.csv: A CSV file containing scraped book data.

Visualization graphs for:
##Number of books by rating.
##Average price by availability.
External Dependencies
##requests: For HTTP requests to fetch web pages.
##beautifulsoup4: For parsing HTML and extracting data.
##pandas: For data manipulation and saving to CSV.
##matplotlib: For visualizing the scraped data.


2. KPI Dashboard Generator
Description
This script reads sales data from a CSV file, calculates yearly KPIs, and generates a PDF dashboard with:

Total sales per category.
Return on Marketing Spend (ROMS).
Average Order Value (AOV) per category.
Visualizations (bar and line charts).


##Instructions
Setup:
##Install required libraries:
pip install pandas matplotlib
##Prepare Input:
Ensure the input file (sales_data.csv) is formatted with columns:
Date: Date of sales.
Category: Product category.
TotalSales: Total sales amount.
QuantitySold: Number of items sold.
##Run the Script:
Save the script as kpi_dashboard.py.
##Execute the script:
python kpi_dashboard.py
Outputs:
##kpi_dashboard.pdf: A PDF file containing KPIs and visualizations.

Visualizations include:
Bar chart: Total sales per category (yearly).
Line chart: Average Order Value (AOV) per category.
##External Dependencies
pandas: For data processing and KPI calculations.
matplotlib: For creating visualizations.
##matplotlib.backends.backend_pdf: For saving visualizations and tables to a PDF.


##Automation with Task Scheduler

##The KPI Dashboard Generator script can be automated using Task Scheduler (Windows):

##Open Task Scheduler and click "Create Basic Task."
##Provide a task name (e.g., KPI Dashboard Automation).
Choose a trigger (e.g., daily or weekly).
Set the action to "Start a Program."
Browse to your python.exe (e.g., C:\Python39\python.exe).
Add the script path (e.g., C:\path\to\kpi_dashboard.py) as an argument.
Save the task. Task Scheduler will now run the script automatically.
