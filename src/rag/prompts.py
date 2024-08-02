from llama_index.core import PromptTemplate

custom_text_to_sql_prompt = PromptTemplate("""Given an input question, create a precise {dialect} PostgreSQL query to answer it. Follow these guidelines:

1. Use only tables and columns from the provided schema.
2. Select only relevant columns, never all columns.
3. Qualify column names with table names when necessary.
4. Use appropriate JOINs, WHERE clauses, and aggregations.
5. Order results to highlight the most pertinent information.
6. Avoid querying non-existent columns or tables.
7. Optimize the query for performance where possible.

Your response should contain only the SQL query, without any additional explanation or formatting. Do not use markdown or prepend the query with the term `sql`.

Schema:
{schema}

Question: {query_str}
SQL Query:
""")

custom_sql_response_synthesis_prompt = PromptTemplate("""Given an input question, synthesize a response from the query results.
Query: {query_str}
SQL: {sql_query}
SQL Response: {context_str}
Response: 
""")