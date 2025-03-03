import json
import os
from datetime import datetime
from config import LOOKER_STUDIO_REPORT_ID

class DashboardGenerator:
    """
    Prepare and update data for Looker Studio (Google Data Studio)
    """
    
    def __init__(self):
        """
        Initialize dashboard data
        """
        self.data_path = 'data/dashboard_data.json'
        self.template_path = 'templates/dashboard_template.json'
        
        # Check if data file exists, create if not
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'report_id': LOOKER_STUDIO_REPORT_ID,
                    'sales_data': {},
                    'category_sales': {},
                    'sales_trends': {},
                    'summary': ""
                }, f, ensure_ascii=False, indent=2)
    
    def update_data(self, sales_data, category_sales, sales_trends, summary):
        """
        Update dashboard data
        """
        # Load existing data
        with open(self.data_path, 'r', encoding='utf-8') as f:
            dashboard_data = json.load(f)
        
        # Update data
        dashboard_data.update({
            'last_updated': datetime.now().isoformat(),
            'sales_data': sales_data,
            'category_sales': category_sales,
            'sales_trends': sales_trends,
            'summary': summary
        })
        
        # Save updated data
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
        
        print(f"Dashboard data updated: {self.data_path}")
        print(f"To use this data in Looker Studio: https://lookerstudio.google.com/reporting/create?c.reportId={LOOKER_STUDIO_REPORT_ID}")