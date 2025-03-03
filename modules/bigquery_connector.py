import os
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, timedelta
from config import BIGQUERY_CREDENTIALS_PATH, ANALYSIS_TIMEFRAME_HOURS, TOP_PRODUCTS_COUNT, TOP_CATEGORIES_COUNT

class BigQueryConnector:
    """
    Manages BigQuery connections and queries
    """
    
    def __init__(self, project_id, dataset_id, table_id):
        """
        Initialize BigQuery connection
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        
        # Authentication
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = BIGQUERY_CREDENTIALS_PATH
        credentials = service_account.Credentials.from_service_account_file(
            BIGQUERY_CREDENTIALS_PATH,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        # Create BigQuery client
        self.client = bigquery.Client(credentials=credentials, project=project_id)
        
    def get_last_24h_sales(self):
        """
        Get sales data for the last 24 hours
        """
        query = f"""
        SELECT
            transaction_id,
            product_id,
            product_name,
            category,
            price,
            quantity,
            timestamp,
            customer_id,
            payment_method
        FROM
            `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE
            timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {ANALYSIS_TIMEFRAME_HOURS} HOUR)
        ORDER BY
            timestamp DESC
        """
        
        # Execute query and convert results to list of dictionaries
        query_job = self.client.query(query)
        rows = list(query_job)
        
        # Convert query results to list of dictionaries
        data = []
        for row in rows:
            data.append(dict(row.items()))
        
        # Calculate total sales and revenue
        total_sales = len(data)
        total_revenue = sum(row['price'] * row['quantity'] for row in data)
        
        return {
            'data': data,
            'total_sales': total_sales,
            'total_revenue': float(total_revenue),
            'timeframe_hours': ANALYSIS_TIMEFRAME_HOURS
        }
    
    def analyze_sales_by_category(self):
        """
        Get sales analysis by category
        """
        query = f"""
        SELECT
            category,
            COUNT(*) as sale_count,
            SUM(price * quantity) as revenue
        FROM
            `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE
            timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {ANALYSIS_TIMEFRAME_HOURS} HOUR)
        GROUP BY
            category
        ORDER BY
            revenue DESC
        LIMIT {TOP_CATEGORIES_COUNT}
        """
        
        # Execute query and convert results to list of dictionaries
        query_job = self.client.query(query)
        rows = list(query_job)
        
        # Convert query results to list of dictionaries
        data = []
        for row in rows:
            data.append(dict(row.items()))
        
        # Find top category
        top_category = data[0]['category'] if data else None
        top_category_revenue = float(data[0]['revenue']) if data else 0
        
        return {
            'data': data,
            'top_category': top_category,
            'top_category_revenue': top_category_revenue
        }
    
    def analyze_sales_trends(self):
        """
        Get hourly sales trends
        """
        query = f"""
        SELECT
            EXTRACT(HOUR FROM timestamp) as hour,
            COUNT(*) as sale_count,
            SUM(price * quantity) as revenue
        FROM
            `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE
            timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {ANALYSIS_TIMEFRAME_HOURS} HOUR)
        GROUP BY
            hour
        ORDER BY
            hour
        """
        
        # Execute query and convert results to list of dictionaries
        query_job = self.client.query(query)
        rows = list(query_job)
        
        # Convert query results to list of dictionaries
        data = []
        for row in rows:
            data.append(dict(row.items()))
        
        # Find peak and slowest hours
        if data:
            max_revenue_row = max(data, key=lambda x: x['revenue'])
            min_revenue_row = min(data, key=lambda x: x['revenue'])
            max_revenue_hour = int(max_revenue_row['hour'])
            min_revenue_hour = int(min_revenue_row['hour'])
            hourly_trend = [float(row['revenue']) for row in data]
        else:
            max_revenue_hour = 0
            min_revenue_hour = 0
            hourly_trend = []
        
        return {
            'data': data,
            'peak_hour': max_revenue_hour,
            'slowest_hour': min_revenue_hour,
            'hourly_trend': hourly_trend
        }
    
    def get_top_selling_products(self):
        """
        Get top selling products
        """
        query = f"""
        SELECT
            product_id,
            product_name,
            COUNT(*) as sale_count,
            SUM(quantity) as units_sold,
            SUM(price * quantity) as revenue
        FROM
            `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE
            timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {ANALYSIS_TIMEFRAME_HOURS} HOUR)
        GROUP BY
            product_id, product_name
        ORDER BY
            units_sold DESC
        LIMIT {TOP_PRODUCTS_COUNT}
        """
        
        # Execute query and convert results to list of dictionaries
        query_job = self.client.query(query)
        rows = list(query_job)
        
        # Convert query results to list of dictionaries
        data = []
        for row in rows:
            data.append(dict(row.items()))
        
        return data