import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import datetime


# Step 1: Read the CSV file
def read_data(filepath="/content/sales_data.csv"):
    """Reads the sales data from a CSV file."""
    try:
        data = pd.read_csv("/content/sales_data.csv")
        print("Data successfully loaded!")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return None


# Step 2: Calculate KPIs
def calculate_kpis(data):
    """Calculates yearly KPIs."""
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year

    # Calculate Total Sales per Category
    total_sales = data.groupby(['Year', 'Category'])['TotalSales'].sum().reset_index()

    # Calculate Return on Marketing Spend (ROMS)
    # Assuming Marketing Spend is 10% of TotalSales (just an assumption for demonstration)
    total_sales['MarketingSpend'] = total_sales['TotalSales'] * 0.10
    total_sales['ROMS'] = total_sales['TotalSales'] / total_sales['MarketingSpend']

    # Calculate Average Order Value (AOV)
    data['AOV'] = data['TotalSales'] / data['QuantitySold']
    avg_aov = data.groupby(['Year', 'Category'])['AOV'].mean().reset_index()

    print("KPIs successfully calculated!")
    return total_sales, avg_aov


# Step 3: Create Visualizations
def create_visualizations(total_sales, avg_aov):
    """Generates bar charts and visualizations."""
    visualizations = []

    # Total Sales per Category (Bar Chart)
    plt.figure(figsize=(10, 6))
    for year in total_sales['Year'].unique():
        subset = total_sales[total_sales['Year'] == year]
        plt.bar(subset['Category'], subset['TotalSales'], label=f"{year}")
    plt.title("Total Sales per Category (Yearly)")
    plt.xlabel("Category")
    plt.ylabel("Total Sales")
    plt.legend()
    plt.tight_layout()
    visualizations.append(plt.gcf())

    # Average Order Value (Line Chart)
    plt.figure(figsize=(10, 6))
    for year in avg_aov['Year'].unique():
        subset = avg_aov[avg_aov['Year'] == year]
        plt.plot(subset['Category'], subset['AOV'], marker='o', label=f"{year}")
    plt.title("Average Order Value (AOV) per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Order Value (AOV)")
    plt.legend()
    plt.tight_layout()
    visualizations.append(plt.gcf())

    print("Visualizations successfully created!")
    return visualizations


# Step 4: Save Dashboard to PDF
def save_dashboard_to_pdf(data, total_sales, avg_aov, visualizations, file_name="kpi_dashboard.pdf"):
    """Saves the KPI dashboard to a PDF file."""
    with PdfPages(file_name) as pdf:
        # Add raw data
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('tight')
        ax.axis('off')
        table_data = data.head(20).values.tolist()
        column_headers = data.columns.tolist()
        table = ax.table(cellText=table_data, colLabels=column_headers, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(data.columns))))
        plt.title("Sample Raw Data")
        pdf.savefig(fig)
        plt.close()

        # Add KPIs as a table
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.axis('tight')
        ax.axis('off')
        kpi_table_data = total_sales.values.tolist()
        kpi_column_headers = total_sales.columns.tolist()
        table = ax.table(cellText=kpi_table_data, colLabels=kpi_column_headers, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(total_sales.columns))))
        plt.title("Yearly KPIs - Total Sales, ROMS")
        pdf.savefig(fig)
        plt.close()

        # Add Visualizations
        for viz in visualizations:
            pdf.savefig(viz)

    print(f"KPI Dashboard saved as {file_name}!")


#Open Task Scheduler:

#Search "Task Scheduler" in the Windows search bar and open it.
#Create Basic Task:

#Click "Create Basic Task".
#Name the task (e.g., "KPI Dashboard Automation").
#Set Trigger:

#Choose how often you want the task to run (e.g., daily, weekly).
#Set Action:

#Select "Start a Program".
##Browse to python.exe (e.g., C:\Python39\python.exe).
#Add the script path as an argument (e.g., C:\path\to\kpi_dashboard.py).
#Finish:

#Review the settings and save.

# Main Script
if __name__ == "__main__":
    # File paths and constants
    input_file = "sales_data.csv"  # Your converted CSV file
    output_file = "kpi_dashboard.pdf"

    # Step 1: Read data
    sales_data = read_data(input_file)

    if sales_data is not None:
        # Step 2: Calculate KPIs
        total_sales_kpis, avg_aov_kpis = calculate_kpis(sales_data)

        # Step 3: Create Visualizations
        charts = create_visualizations(total_sales_kpis, avg_aov_kpis)

        # Step 4: Save to PDF
        save_dashboard_to_pdf(sales_data, total_sales_kpis, avg_aov_kpis, charts, output_file)