from fastapi import FastAPI, HTTPException
import psycopg2
import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details
DB_NAME = "qa_system"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL!")
except Exception as e:
    print("❌ Database Connection Error:", e)

# LangChain LLM Setup
llm = OpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="Convert this question into an SQL query for a PostgreSQL database: {question}",
)
sql_chain = LLMChain(llm=llm, prompt=prompt_template)


@app.get("/")
def home():
    return {"message": "Q&A System with FastAPI and LangChain!"}


@app.post("/ask")
def ask_question(question: str):
    """Accepts a question, converts it to SQL, and fetches data from PostgreSQL."""
    try:
        # Convert question into SQL query
        sql_query = sql_chain.run(question)

        # Execute query
        cur.execute(sql_query)
        results = cur.fetchall()

        # Format response
        return {"question": question, "sql_query": sql_query, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn main:app --reload
