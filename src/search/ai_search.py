import os
import polars as pl
from dotenv import load_dotenv
from google import genai

"""Query the database using plain English.It will instantly translate your natural language prompts into Polars code, retrieving the top 10  results. It takes api key from .env which is hidden.""" 


# load API 
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#gmini client
client = genai.Client(api_key=api_key)

def simple_search(user_query):
    df = pl.read_parquet("data/dblp_parquet/dblp_data_2015_plus.parquet")

    #instructions for the AI
    prompt = f"""
    You are a Polars assistant. Dataframe 'df' has columns: 
    ['key', 'type', 'title', 'year', 'venue', 'authors'].
    
    User wants: {user_query}
    
    Return ONLY the python code to filter 'df'. 
    Example: df.filter(pl.col('year') == 2018)
    No markdown, no backticks, just one line of code.
    """

    # get respons
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    #clean the output 
    ai_code = response.text.strip().replace("```python", "").replace("```", "")

    try:
        # run the code generated
        result = eval(ai_code)
        return result.head(10)
    except Exception as e:
        return f"Error: {e} Generated code was: {ai_code}"

if __name__ == "__main__":
    query = input("daj mi dane z 2018 roku ")
    print(simple_search(query))