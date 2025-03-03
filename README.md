# Real-Time E-Commerce Analytics Dashboard

A powerful real-time analytics solution for e-commerce platforms that processes sales data from BigQuery, generates AI-powered insights with LangChain and OpenAI, and visualizes trends through Looker Studio.

## Features

- **Real-time Data Processing**: Fetches and analyzes sales data from BigQuery in real-time
- **AI-Powered Insights**: Generates concise summaries and strategic recommendations using LangChain and OpenAI's GPT-4
- **Interactive Dashboards**: Creates visualizations in Looker Studio for easy data interpretation
- **Scheduled Analysis**: Automatically runs analysis jobs at configurable intervals

## Project Structure

```
real-time-ecommerce-analytics/
├── config.py                   # Configuration settings
├── main.py                     # Main application entry point
├── requirements.txt            # Project dependencies
├── credentials/                # API keys and service account files (gitignored)
│   └── bigquery-service-account.json
├── data/                       # Generated analysis data
│   ├── dashboard_data.json
│   └── latest_analysis.json
├── modules/                    # Core modules
│   ├── __init__.py
│   ├── bigquery_connector.py   # Handles BigQuery data fetching
│   ├── langchain_summarizer.py # Generates insights with LangChain
│   └── dashboard_generator.py  # Prepares data for Looker Studio
└── templates/                  # Dashboard templates
    └── dashboard_template.json
```

## Setup Instructions

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/real-time-ecommerce-analytics.git
   cd real-time-ecommerce-analytics
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   - Create a `credentials` directory
   - Place your BigQuery service account JSON file in the credentials directory
   - Update `config.py` with your API keys and settings

4. **Run the application**
   ```
   python main.py
   ```

## Configuration Options

- `ANALYSIS_TIMEFRAME_HOURS`: Define the time window for analysis (default: 24)
- `TOP_PRODUCTS_COUNT`: Number of top products to include in the analysis (default: 10)
- `TOP_CATEGORIES_COUNT`: Number of top categories to include in the analysis (default: 5)

## Setting Up Looker Studio Integration

1. Create a new Looker Studio report
2. Set up a JSON data source
3. Copy your report ID to the `LOOKER_STUDIO_REPORT_ID` in `config.py`
4. The dashboard will automatically update with the latest data

## License

This project is licensed under the MIT License - see the LICENSE file for details.