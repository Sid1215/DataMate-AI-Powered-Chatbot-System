from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)

from dbop import get_database_schema, execute_sql_query

# LOAD ENVIRONMENT VARIABLES
load_dotenv()


# LLM
llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
    reasoning_effort="none"
)


# OUTPUT PARSER
output_parser = StrOutputParser()


# PROMPT 1: SQL GENERATION
sql_prompt = PromptTemplate.from_template("""
You are an expert SQLite assistant for a supermarket database.

Database Schema:
{schema}

Instructions:
1. Read the user's question carefully.
2. Generate ONLY a valid SQLite SQL query.
3. Use only the tables and columns provided in the schema.
4. Never invent table names or column names.
5. Handle spelling mistakes and similar product names whenever possible.
6. Use aggregate functions (SUM, COUNT, AVG, MAX, MIN) whenever required.
7. Return ONLY the SQL query.
8. Do not include explanations.
9. Do not include markdown.
10. Do not use code fences.

User Question:
{user_input}
""")


# SQL GENERATION CHAIN
sql_chain = (
    sql_prompt
    | llm
    | output_parser
)


# PROMPT 2: FINAL ANSWER
answer_prompt = PromptTemplate.from_template("""
You are an intelligent supermarket AI assistant.

User Question:
{user_input}

Database Result:
{query_result}

SQL Execution Error:
{error}

Instructions:
1. If SQL Execution Error is not empty, reply:
   "Sorry, I couldn't process your request."
2. Otherwise answer ONLY using the database result.
3. Never make assumptions.
4. If the database result is empty, reply exactly:
   "The requested information is not available in the database."
5. Keep the response short and natural.
6. Do not mention SQL.
7. Do not mention queries.
8. Do not mention the database.
9. Return only the final answer.
""")


# FINAL ANSWER CHAIN
answer_chain = (
    answer_prompt
    | llm
    | output_parser
)


# PREPARE INPUT FOR SQL CHAIN
prepare_sql_input = RunnableLambda(
    lambda x: {
        "schema": x["schema"],
        "user_input": x["user_input"]
    }
)


# EXECUTE SQL
def execute_query(data):

    sql_query = data["sql_query"]
    db_path = data["db_path"]
    user_input = data["user_input"]

    try:

        # Execute generated SQL
        result = execute_sql_query(
            sql_query,
            db_path
        )

        return {
            "user_input": user_input,
            "query_result": result,
            "error": ""
        }

    except Exception as e:

        return {
            "user_input": user_input,
            "query_result": "",
            "error": str(e)
        }


# Convert normal Python function into LangChain Runnable
execute_query_runnable = RunnableLambda(execute_query)


# COMPLETE CHAIN
final_chain = (
    
    {
        # Generate SQL
        "sql_query": (
            prepare_sql_input
            | sql_chain
        ),

        # Pass original user question
        "user_input": RunnableLambda(
            lambda x: x["user_input"]
        ),

        # Pass database path
        "db_path": RunnableLambda(
            lambda x: x["db_path"]
        )
    }

    # Execute SQL
    | execute_query_runnable

    # Generate final natural-language answer
    | answer_chain
)


# MAIN FUNCTION
def get_ai_response(user_input, db_path):

    # Get database schema
    schema = get_database_schema(db_path)

    # Run complete LangChain pipeline
    final_answer = final_chain.invoke({
        "schema": schema,
        "user_input": user_input,
        "db_path": db_path
    })

    return final_answer