import pandas as pd
import sqlite3

# Read CSV
df = pd.read_csv("support_tickets.csv")

# Create/connect to database
connection = sqlite3.connect("customer_support_tickets.db")

# Put entire DataFrame into SQLite
df.to_sql("customer_support_tickets", connection, if_exists="replace", index=False)

connection.close()