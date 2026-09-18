import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import AsyncGroq



app = FastAPI(title="Groq LLM Service")
load_dotenv()

#Create Groq Client Connection
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str


async def call_groq_api(prompt):
    response = await groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        reasoning_effort="medium"
    )

    return response.choices[0].message.content

#Database Connection
connection=sqlite3.connect("customer_support_tickets.db")


#Function to convert text into sql query
async def convert_text_query_into_sql_query(user_input):
    prompt = f"""You are an SQL Professional your job is to convert text query into sql query to execute in my SQLite database
    ### DATABASE Details
    Table name:customer_support_tickets
    Columns : ticket_id,created_at,category,priority,status,response_time_hrs,resolution_time_hrs,agent_id,customer_rating,issue_summary
    Category values:General,Billing,Technical
    Priority values:Low,Medium,High,Critical
    Status values:Open,Resolved,Escalated

    
    ### Note 
    1.Generate only SQL Query According to Text query
    2. Do not include markdown code fences.
    3. Do not include explanations or extra text.
    4.Ensure strictly return only the Equivalent SQL query without any extra contents

    ### IMPORTANT SQL RULES
    1. When the question asks for the most, least, highest, lowest, maximum, or minimum, include the calculated value in the SELECT statement.
    2. When counting records, return the count along with the relevant column.
    3. Use SQLite-compatible SQL Syntax.
    4. Return only the SQL query.
    5. Only use values that actually exist in the DATABASE Details.Please do not hallucinate.
    6. Anomoly means tickets with abnormally long resolution times, unresolved high-priority tickets older than 24 hours.For anomaly-related questions, identify anomalies using these rules:
        i) A resolved ticket is an anomaly if its resolution_time_hrs is more than 2 standard deviations above the average resolution_time_hrs of all resolved tickets.
        ii) An Open or Escalated ticket is an anomaly if its priority is High or Critical and more than 24 hours have elapsed between its created_at time and the latest created_at time available in the database.
        iii) Do not use resolution_time_hrs to determine how long an Open or Escalated ticket has been waiting because resolution_time_hrs is NULL for unresolved tickets.
        iv) For "anomalies" without further clarification, consider both types of anomalies.
    v) Return only tickets that satisfy at least one applicable anomaly condition.
    7. Calculate standard deviation using SQLite-compatible expressions because SQLite does not have a built-in STDDEV function.

    ### INPUT FORMAT
    What is the status of the TKT-002 ?
    
    ### OUTPUT FORMAT
    SELECT status
    FROM customer_support_tickets
    WHERE ticket_id = 'TKT-002'

    ### TEXT QUERY
    Convert following text query into SQL Query : {user_input}
    """
    sql_query=await call_groq_api(prompt)
    print(sql_query)
    return sql_query

#Function to get the records from table
def query_to_sqllite_database(query,connection):
    result=pd.read_sql_query(query,connection)
    print("Database result:",result)
    return result.to_dict(orient="records")

#Fast APIs

@app.get("/health")
async def health_check():

    return {
        "status": "ok",
        "message": "Service is up and running"
    }

@app.get("/anomalies")
async def detect_anomalies():

    try:

        anomaly_query = """
        WITH stats AS (
            SELECT
                AVG(resolution_time_hrs) AS avg_res,
                SQRT(
                    AVG(resolution_time_hrs * resolution_time_hrs)
                    - AVG(resolution_time_hrs) * AVG(resolution_time_hrs)
                ) AS stddev_res
            FROM customer_support_tickets
            WHERE status = 'Resolved'
        ),
        date_filter AS (
            SELECT MAX(created_at) AS max_date
            FROM customer_support_tickets
        )
        SELECT t.*
        FROM customer_support_tickets t, stats, date_filter
        WHERE
            (
                t.status = 'Resolved'
                AND (
                    t.resolution_time_hrs > (stats.avg_res + 2 * stats.stddev_res)
                    OR
                    t.resolution_time_hrs < (stats.avg_res - 2 * stats.stddev_res)
                )
            )
            OR
            (
                t.status IN ('Open', 'Escalated')
                AND t.priority IN ('High', 'Critical')
                AND (
                    julianday(date_filter.max_date)
                    - julianday(t.created_at)
                ) * 24 > 24
            )
        """

        result = pd.read_sql_query(
            anomaly_query,
            connection
        )

        result = result.astype(object).where(pd.notna(result), None)

        return {
        "count": len(result),
        "anomalies": result.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting anomalies: {str(e)}"
        )


@app.post(
    "/generate",
    response_model=PromptResponse
)
async def generate_response(payload: PromptRequest):

    if not payload.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty."
        )

    try:

        user_input = payload.prompt

        query_response = await convert_text_query_into_sql_query(
            user_input
        )

        database_result = query_to_sqllite_database(
            query_response,
            connection
        )

        prompt = f"""
        You are answering a user's question using the database results provided below.

Database results:
{database_result}

User question:
{user_input}

Instructions:
1. Answer the user's question directly.
2. Use only the database results provided above.
3. Treat every row returned by the database as a matching result for the user's question.
4. Do not independently re-evaluate, reinterpret, or reject the database results.
5. Do not say that a returned record is "not an anomaly" or "not significant" when the SQL query returned it as an anomaly.
6. If the question asks for tickets, list the relevant ticket IDs and important details.
7. If the database result is empty, clearly say that no matching tickets were found.
8. Do not change the meaning of the user's question.
9. Do not invent any records or values.
10. State the number of matching records when the database result contains multiple rows.
11. Provide a concise and clear answer.
12. If the user's question asks about anomalies, treat all rows returned by the SQL query as the identified anomalies and explicitly state that they are anomalies.
    """

        response = await call_groq_api(prompt)

        return PromptResponse(
            response=response
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )