import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from config import OPENAI_API_KEY

class LangChainSummarizer:
    """
    Creates sales data summaries using LangChain and OpenAI
    """
    
    def __init__(self):
        """
        Initialize LangChain and OpenAI connection
        """
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        
        # Configure OpenAI model
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        
        # Create prompt template for summary
        self.summary_prompt = PromptTemplate(
            input_variables=["sales_data", "category_data", "trends_data"],
            template="""
            Create a brief summary of the following e-commerce sales data:
            
            Total Sales Information:
            {sales_data}
            
            Category Sales Information:
            {category_data}
            
            Sales Trends:
            {trends_data}
            
            Based on this data, provide a short summary of the sales performance over the last 24 hours,
            highlight notable product categories, analyze trends in sales hours, and
            provide 2-3 strategic recommendations for business owners.
            """
        )
        
        # Create modern LangChain pipeline using | operator
        self.chain = self.summary_prompt | self.llm
    
    def generate_summary(self, sales_data, category_sales, sales_trends):
        """
        Generate summary for the given sales data
        """
        # Prepare data texts
        sales_text = f"""
        - Total Sales Count: {sales_data['total_sales']}
        - Total Revenue: ${sales_data['total_revenue']}
        - Analysis Period: Last {sales_data['timeframe_hours']} hours
        """
        
        category_text = "\n".join([
            f"- {cat['category']}: {cat['sale_count']} sales, ${cat['revenue']} revenue"
            for cat in category_sales['data']
        ])
        
        trends_text = f"""
        - Peak Sales Hour: {sales_trends['peak_hour']}:00
        - Slowest Sales Hour: {sales_trends['slowest_hour']}:00
        - Hourly Revenue Trend: {', '.join([str(rev) for rev in sales_trends['hourly_trend']])}
        """
        
        # Generate summary using modern invoke method
        result = self.chain.invoke({
            "sales_data": sales_text,
            "category_data": category_text,
            "trends_data": trends_text
        })
        
        # Extract the content from the result
        # (modern LangChain returns a more complex object)
        if hasattr(result, 'content'):
            summary = result.content
        else:
            # Fallback for different return types
            summary = str(result)
        
        return summary