import os
import json
import time
import schedule
from datetime import datetime
from modules.bigquery_connector import BigQueryConnector
from modules.langchain_summarizer import LangChainSummarizer
from modules.dashboard_generator import DashboardGenerator
from config import BIGQUERY_PROJECT_ID, BIGQUERY_DATASET, BIGQUERY_TABLE

def run_analysis():
    """
    Run real-time e-commerce analysis
    """
    print(f"[{datetime.now()}] Starting analysis...")
    
    # Create BigQuery connection
    bq_connector = BigQueryConnector(
        project_id=BIGQUERY_PROJECT_ID,
        dataset_id=BIGQUERY_DATASET,
        table_id=BIGQUERY_TABLE
    )
    
    # Get sales data for the last 24 hours
    sales_data = bq_connector.get_last_24h_sales()
    
    # Analyze sales by product categories
    category_sales = bq_connector.analyze_sales_by_category()
    
    # Analyze sales trends
    sales_trends = bq_connector.analyze_sales_trends()
    
    # Generate summary with LangChain and OpenAI
    summarizer = LangChainSummarizer()
    sales_summary = summarizer.generate_summary(sales_data, category_sales, sales_trends)
    
    # Update dashboard data
    dashboard = DashboardGenerator()
    dashboard.update_data(sales_data, category_sales, sales_trends, sales_summary)
    
    # Save results
    with open('data/latest_analysis.json', 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'sales_data': sales_data,
            'category_sales': category_sales,
            'sales_trends': sales_trends,
            'summary': sales_summary
        }, f, ensure_ascii=False, indent=2)
    
    print(f"[{datetime.now()}] Analysis completed and dashboard updated.")

def schedule_jobs():
    """
    Schedule regular analysis jobs
    """
    # Run analysis every hour
    schedule.every().hour.do(run_analysis)
    
    print("Real-time analysis scheduled. Will run every hour.")
    print("Press Ctrl+C to exit.")
    
    # Run first analysis immediately
    run_analysis()
    
    # Run scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Check if directories exist, create if not
    os.makedirs('data', exist_ok=True)
    
    try:
        schedule_jobs()
    except KeyboardInterrupt:
        print("\nProgram terminated.")