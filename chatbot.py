from langchain_groq import ChatGroq
from dotenv import load_dotenv
from dbop import get_database_schema, execute_sql_query

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0,
    reasoning_effort="none"
)


def get_ai_response(user_input, db_path):
    # Get database schema
    schema = get_database_schema(db_path)

    # -------------------- Prompt 1 : Generate SQL -------------------- #



    sql_prompt = f"""
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
8. Do not include explanations, markdown, or code fences.

User Question:
{user_input}
"""

    sql_query = llm.invoke(sql_prompt).content.strip()

    # -------------------- Execute SQL -------------------- #

    try:
        query_result = execute_sql_query(
        sql_query,
        db_path
    )
    except Exception as e:
        return f"Error:\n\n{e}"

    # -------------------- Prompt 2 : Generate Answer -------------------- #

    answer_prompt = f"""
You are an intelligent supermarket AI assistant.

User Question:
{user_input}

Database Result:
{query_result}

Instructions:
1. Answer ONLY using the database result.
2. Never make assumptions.
3. If the database result is empty, reply exactly:
   "The requested information is not available in the database."
4. Keep the response short and natural.
5. Do not mention SQL, queries, or the database.
6. Return only the final answer.
"""

    final_answer = llm.invoke(answer_prompt).content.strip()

    return final_answer