from fastapi import FastAPI, HTTPException
import psycopg2
import os
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_openai import OpenAI

# Load environment variables
load_dotenv()

# Database connection details
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()


def fetch_database_schema():
    """Dynamically fetch the schema of the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()

        # Query to get table and column details
        cur.execute("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        
        schema_rows = cur.fetchall()
        cur.close()
        conn.close()

        # Format the schema into a readable string
        db_schema = "Database Schema:\n"
        current_table = None
        for table_name, column_name, data_type in schema_rows:
            if table_name != current_table:
                db_schema += f"\nTABLE: {table_name}\n"
                current_table = table_name
            db_schema += f"  - {column_name} ({data_type})\n"

        print("Fetched Database Schema:\n", db_schema)
        return db_schema

    except Exception as e:
        print("Database Schema Fetch Error:", e)
        return "Error fetching schema."


# Fetch schema at startup
DB_SCHEMA = fetch_database_schema()

# LangChain LLM Setup
llm = OpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)

# **Updated Prompt Template**
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=f"""
You are an AI assistant with access to the following PostgreSQL **database schema**:

{DB_SCHEMA}

**Instructions:**
1️ **If the user's question is related to the database**, **ONLY return a valid SQL query** without any explanation.  
2️ **If the user's question is general (not database-related), respond normally** as a conversational assistant.  

**User Question:** {{question}}

**Response:**""",
)

llm_chain = LLMChain(llm=llm, prompt=prompt_template)


@app.get("/")
def home():
    return {"message": "Q&A System with FastAPI and LangChain!"}


@app.post("/ask")
def ask_question(question: str):
    """Handles user questions by determining if an SQL query is needed or not."""
    try:
        # Get response from LLM
        response = llm_chain.run({"question": question}).strip()

        # **If response starts with SELECT/INSERT/UPDATE/DELETE, treat it as an SQL query**
        if response.lower().startswith(("select", "insert", "update", "delete")):
            # Connect to DB and execute the query
            conn = psycopg2.connect(
                dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
            )
            cur = conn.cursor()
            cur.execute(response)
            results = cur.fetchall()
            cur.close()
            conn.close()

            # Return SQL query & results
            return {"question": question, "sql_query": response, "results": results}

        # **Otherwise, return normal response**
        return {"question": question, "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn main:app --reload
