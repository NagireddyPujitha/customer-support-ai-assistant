# Customer Support AI Assistant

An AI-powered customer support ticket analysis application built with **Python, FastAPI, Streamlit, SQLite, Pandas, and Groq**.

The application allows a user to:

- Load customer support ticket data from `support_tickets.csv` into a SQLite database.
- Ask questions about the tickets using natural language.
- Convert natural-language questions into SQLite SQL queries using an LLM.
- Detect predefined ticket anomalies.
- Access the functionality through a REST API.
- Use the same functionality through a simple Streamlit web interface.

---

## 1. What This Application Does

The application has three main features in the Streamlit interface:

### 1. Health

Checks whether the FastAPI backend is running.

The application calls:

```text
GET /health
```

If the backend is running correctly, the UI displays:

```text
Service is up and running
```

### 2. NL Query

Allows the user to ask questions about the customer support tickets in normal English language.

For example:

```text
How many tickets are currently open?
```

or:

```text
What is the status of the TKT-002?
```

The application then:

1. Sends the question from Streamlit to the FastAPI `/generate` endpoint.
2. Uses the Groq LLM to convert the natural-language question into SQL.
3. Executes the generated SQL against the SQLite database.
4. Sends the database result back to the LLM.
5. Generates a concise natural-language answer.
6. Displays the answer in Streamlit.

### 3. Anomalies

Detects tickets matching the anomaly rules implemented in `app.py`.

The application considers two types of anomalies:

#### Resolved-ticket anomaly

A resolved ticket is considered an anomaly when its `resolution_time_hrs` is more than **2 standard deviations above or below** the average resolution time of resolved tickets.

#### Open/Escalated high-priority anomaly

An `Open` or `Escalated` ticket is considered an anomaly when:

- its priority is `High` or `Critical`, and
- more than 24 hours have elapsed between its `created_at` time and the latest `created_at` time available in the database.

The anomaly logic is implemented directly in the `/anomalies` endpoint.

---

# 2. Project Structure

After cloning the repository, the project should look approximately like this:

```text
customer_support_ai/
│
├── app.py
├── customer_streamlit.py
├── data_ingestion.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run.bat
├── run.sh
├── support_tickets.csv
│
└── README.md
```

The SQLite database:

```text
customer_support_tickets.db
```

is created by `data_ingestion.py`, so it does not have to be manually created.

You may also see:

```text
venv/
__pycache__/
```

These are local Python environment/cache folders and should not be committed to GitHub.

---

# 3. Files and Their Purpose

| File | Purpose |
|---|---|
| `app.py` | FastAPI backend, Groq integration, SQL generation, database querying, and anomaly detection |
| `customer_streamlit.py` | Streamlit user interface |
| `data_ingestion.py` | Reads `support_tickets.csv` and creates/populates the SQLite database |
| `support_tickets.csv` | Customer support ticket dataset |
| `customer_support_tickets.db` | SQLite database created from the CSV |
| `.env.example` | Template showing where the Groq API key is configured |
| `.gitignore` | Prevents secrets, virtual environments, cache files, and database files from being committed |
| `requirements.txt` | Python packages required by the application |
| `run.bat` | Windows startup script |
| `run.sh` | Linux/macOS shell startup script |
| `README.md` | Project documentation |

---

# 4. Technologies Used

The project uses:

- **Python** — main programming language
- **FastAPI** — REST API backend
- **Streamlit** — web-based user interface
- **SQLite** — local database
- **Pandas** — CSV/database data processing
- **Groq** — LLM API
- **`openai/gpt-oss-120b`** — LLM model used by the Groq client
- **Pydantic** — request/response validation
- **python-dotenv** — loading the API key from `.env`
- **Requests** — communication between Streamlit and FastAPI

The assessment specifies Python as the language and allows Groq's free tier.

---

# 5. Requirements

Before starting, you need:

1. A computer with Python installed.
2. Git installed if you are cloning the project from GitHub.
3. A Groq API key.
4. Internet access for the Groq API.
5. The project files.

No separate database software is required because SQLite is used as a local database.

---

# 6. Clone the Repository

If the project has been uploaded to GitHub, open a terminal/Command Prompt and run:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Then move into the project folder:

```bash
cd <YOUR_REPOSITORY_FOLDER>
```

For example:

```bash
git clone https://github.com/your-username/customer-support-ai.git
cd customer-support-ai
```

Replace the example repository URL with the actual GitHub repository URL.

If you downloaded the repository as a ZIP file instead, extract the ZIP file and open a terminal inside the extracted project folder.

---

# 7. Create a Python Virtual Environment

Using a virtual environment keeps this project's Python packages separate from other Python projects on your computer.

## Windows

Open Command Prompt or PowerShell in the project folder:

```bash
python -m venv venv
```

Activate it:

### Command Prompt

```bash
venv\Scripts\activate
```

### PowerShell

```powershell
venv\Scripts\Activate.ps1
```

After activation, you should see something similar to:

```text
(venv)
```

at the beginning of your terminal prompt.

## Linux/macOS

Run:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

# 8. Install Required Packages

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains the Python dependencies used by the project.

---

# 9. Create the `.env` File

The repository contains:

```text
.env.example
```

Its contents are:

```env
GROQ_API_KEY=your_groq_api_key_here
```

You need to create a real `.env` file from this example.

## Windows

### Option 1 — Command Prompt

Run:

```cmd
copy .env.example .env
```

### Option 2 — Manually

1. Open the project folder.
2. Make a copy of `.env.example`.
3. Rename the copy to:

```text
.env
```

4. Open `.env`.
5. Replace:

```env
GROQ_API_KEY=your_groq_api_key_here
```

with your actual Groq API key:

```env
GROQ_API_KEY=YOUR_ACTUAL_GROQ_API_KEY
```

Do not put quotation marks around the key unless required by your environment.

## Linux/macOS

Run:

```bash
cp .env.example .env
```

Then open `.env` and replace the placeholder with your actual API key.

---

# 10. Keep the API Key Secret

Do **not** upload your real `.env` file to GitHub.

The `.gitignore` file already contains:

```text
.env
```

which prevents the `.env` file from being committed.

Your GitHub repository should contain:

```text
.env.example
```

but **not**:

```text
.env
```

Never replace the placeholder in `.env.example` with your real API key before committing it.

---

# 11. Make Sure `support_tickets.csv` Is Available

The application expects this exact file:

```text
support_tickets.csv
```

The assessment dataset contains 500 rows and uses the customer-support ticket schema defined in the assessment. fileciteturn0file0L28-L30

The important columns are:

```text
ticket_id
created_at
category
priority
status
response_time_hrs
resolution_time_hrs
agent_id
customer_rating
issue_summary
```

### Important GitHub note

Current `.gitignore` contains:

```text
support_tickets.csv
```

That means Git will ignore the CSV file.

---

# 12. Create the SQLite Database

You do not need to manually create:

```text
customer_support_tickets.db
```

Run:

```bash
python data_ingestion.py
```

This script:

1. Reads:

```text
support_tickets.csv
```

2. Connects to:

```text
customer_support_tickets.db
```

3. Creates/replaces the SQLite table:

```text
customer_support_tickets
```

4. Inserts the complete CSV DataFrame into the table.

After successful execution, you should see:

```text
customer_support_tickets.db
```

in the project folder.

---

# 13. Start the FastAPI Backend

There are two ways to start the backend.

## Method 1 — Uvicorn command

Run:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Keep this terminal window running.

The `app:app` part means:

- `app` before `:` = the Python file `app.py`
- `app` after `:` = the FastAPI application object created with `app = FastAPI(...)`

## Check the backend

Open a browser and visit:

```text
http://127.0.0.1:8000/health
```

You should receive:

```json
{
  "status": "ok",
  "message": "Service is up and running"
}
```

---

# 14. FastAPI Endpoints

The backend provides these endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Checks whether the service is running |
| `POST` | `/generate` | Converts a natural-language question to SQL, queries the database, and generates an answer |
| `GET` | `/anomalies` | Detects and returns anomaly tickets |

FastAPI therefore exposes the three main backend capabilities required by the assessment: health check, natural-language querying, and anomaly detection.

---

# 15. FastAPI Interactive Documentation

When the FastAPI server is running, you can also open:

```text
http://127.0.0.1:8000/docs
```

This opens FastAPI's interactive API documentation.

You can use it to inspect and test endpoints such as:

```text
GET /health
POST /generate
GET /anomalies
```

For `/generate`, the request body should look like:

```json
{
  "prompt": "How many tickets are currently open?"
}
```

---

# 16. Start the Streamlit Application

Open a **second terminal window** in the project folder.

Make sure the virtual environment is activated.

Then run:

```bash
streamlit run customer_streamlit.py
```

Streamlit will display a local URL, usually similar to:

```text
http://localhost:8501
```

Open that address in your web browser.

---

# 17. Using the Streamlit Application

When the application opens, you will see:

```text
Customer Support AI Assistant
```

On the left side, there is a **Features** menu containing:

```text
Health
NL Query
Anomalies
```

---

## Feature 1 — Health

Select:

```text
Health
```

Then click:

```text
Check Health
```

The application contacts:

```text
http://127.0.0.1:8000/health
```

If FastAPI is running, you will see:

```text
Service is up and running
```

If you see a connection error, make sure the FastAPI/Uvicorn server is running.

---

## Feature 2 — NL Query

Select:

```text
NL Query
```

You will see:

```text
Ask your question:
```

Enter a question in normal English.

For example:

```text
How many tickets are currently open?
```

Then click:

```text
Submit
```

The application sends your question to:

```text
POST /generate
```

The FastAPI backend then uses the Groq LLM to generate SQL.

The generated SQL is executed against:

```text
customer_support_tickets
```

The result is then passed to the LLM to generate the final answer.

### Example questions

Try questions such as:

```text
How many tickets are currently open?
```

```text
What is the status of the TKT-002?
```

```text
How many Critical tickets are unresolved?
```

```text
What is the average customer rating for Technical category tickets?
```

```text
Which agent resolved the most tickets?
```

```text
Show me all Critical tickets not resolved within 12 hours.
```

---

# 18. Feature 3 — Anomalies

Select:

```text
Anomalies
```

Then click:

```text
Detect Anomalies
```

The Streamlit application sends a request to:

```text
GET /anomalies
```

The FastAPI backend executes the anomaly-detection SQL query.

The UI displays:

```text
Number of Anomalies
```

and, when anomalies are found, displays them in a table.

The table can contain fields such as:

```text
ticket_id
created_at
category
priority
status
response_time_hrs
resolution_time_hrs
agent_id
customer_rating
issue_summary
```

If no anomalies are found, the UI displays:

```text
No anomalies found.
```

---

# 19. How the Natural-Language Query Works

The NL Query feature follows this flow:

```text
User
  |
  v
Streamlit
  |
  | POST /generate
  v
FastAPI
  |
  v
Groq LLM
  |
  | Natural language -> SQL
  v
SQLite Database
  |
  | Query result
  v
FastAPI
  |
  v
Groq LLM
  |
  | Database result -> Natural-language answer
  v
Streamlit
  |
  v
User sees answer
```

The first LLM call is responsible for generating a SQL query from the user's question.

The second LLM call uses the database result to produce the final response.

---

# 20. Database Structure

The SQLite database contains the table:

```text
customer_support_tickets
```

with these columns:

| Column | Description |
|---|---|
| `ticket_id` | Unique ticket identifier |
| `created_at` | Ticket creation timestamp |
| `category` | Issue category |
| `priority` | Ticket urgency |
| `status` | Current ticket status |
| `response_time_hrs` | Hours from creation to first agent response |
| `resolution_time_hrs` | Hours from creation to resolution; unresolved tickets can have NULL |
| `agent_id` | Assigned support agent identifier |
| `customer_rating` | Post-resolution customer rating |
| `issue_summary` | Brief description of the reported issue |

These definitions match the dataset schema supplied in the assessment. fileciteturn0file0L93-L116

---

# 21. Groq Configuration

The Groq client is created in `app.py` using:

```python
groq_client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY")
)
```

The model configured in the project is:

```text
openai/gpt-oss-120b
```

The code uses:

```text
reasoning_effort="medium"
```

The API key is loaded from the `.env` file using `python-dotenv`.

---

# 22. Running the Entire Application on Windows

The repository contains:

```text
run.bat
```

Its purpose is to automate the startup process.

From Command Prompt, run:

```cmd
run.bat
```

It performs these operations:

```text
1. python data_ingestion.py
2. Start Uvicorn/FastAPI
3. Wait briefly for the API to start
4. Start Streamlit
```

So the intended Windows workflow can be as simple as:

```cmd
run.bat
```

After Streamlit starts, open the URL shown in the terminal, normally:

```text
http://localhost:8501
```

---

# 23. Running the Entire Application on Linux/macOS

The repository contains:

```text
run.sh
```

Make it executable if necessary:

```bash
chmod +x run.sh
```

Then run:

```bash
./run.sh
```

The script:

1. Runs `data_ingestion.py`.
2. Starts Uvicorn in the background.
3. Waits for the FastAPI server.
4. Starts Streamlit.

---

# 24. Recommended Manual Startup

If you are using the application for the first time and want to understand each step, use this sequence.

### Terminal 1

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Then create/update the database:

```bash
python data_ingestion.py
```

Then start FastAPI:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

### Terminal 2

Activate the virtual environment again:

```bash
venv\Scripts\activate
```

Then start Streamlit:

```bash
streamlit run customer_streamlit.py
```

Finally, open the Streamlit URL shown in the terminal.

---

# 25. Troubleshooting

## Problem: `python` is not recognized

Install Python and make sure Python is added to your system PATH.

Then reopen the terminal and check:

```bash
python --version
```

---

## Problem: `pip install -r requirements.txt` fails

Make sure the virtual environment is activated:

```text
(venv)
```

Then upgrade pip:

```bash
python -m pip install --upgrade pip
```

and try again:

```bash
pip install -r requirements.txt
```

---

## Problem: Cannot connect to FastAPI

If Streamlit displays:

```text
Cannot connect to FastAPI. Please start the FastAPI server first.
```

start FastAPI:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Then refresh the Streamlit page.

---

## Problem: Groq/API error

Check that:

1. `.env` exists.
2. `GROQ_API_KEY` is present in `.env`.
3. The API key is valid.
4. Your computer has internet access.
5. The Groq service/model configured in `app.py` is available to your account.

Do not put the API key directly into `app.py`.

---

## Problem: `customer_support_tickets.db` does not exist

Run:

```bash
python data_ingestion.py
```

Make sure:

```text
support_tickets.csv
```

is present in the same project directory.

---

## Problem: `support_tickets.csv` cannot be found

Make sure the file is located in the project root:

```text
customer-support-ai/
├── support_tickets.csv
├── app.py
├── data_ingestion.py
└── ...
```

Then run:

```bash
python data_ingestion.py
```

---

## Problem: Streamlit opens but queries fail

Check that both applications are running:

### FastAPI

```text
http://127.0.0.1:8000
```

### Streamlit

Usually:

```text
http://localhost:8501
```

You can also test:

```text
http://127.0.0.1:8000/health
```

If `/health` works, the FastAPI backend is running.

---

# 26. API Usage Examples

## Health Check

### Request

```text
GET http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "ok",
  "message": "Service is up and running"
}
```

---

## Natural-Language Query

### Request

```text
POST http://127.0.0.1:8000/generate
```

Request body:

```json
{
  "prompt": "How many tickets are currently open?"
}
```

The exact response depends on the current contents of `support_tickets.csv`.

---

## Anomaly Detection

### Request

```text
GET http://127.0.0.1:8000/anomalies
```

The response contains:

```json
{
  "count": 0,
  "anomalies": []
}
```

or, when matching records exist:

```json
{
  "count": 2,
  "anomalies": [
    {
      "...": "..."
    }
  ]
}
```

The actual values depend on the dataset.

---

# 27. Security Notes

### Never commit `.env`

The real API key belongs only in:

```text
.env
```

The repository should contain:

```text
.env.example
```

instead.

### Do not hard-code the API key

Keep this configuration:

```python
os.getenv("GROQ_API_KEY")
```

rather than putting the secret directly in the source code.

### Database files

The current `.gitignore` excludes:

```text
*.db
```

so the generated SQLite database should not normally be committed.

The database can be recreated from:

```text
support_tickets.csv
```

using:

```bash
python data_ingestion.py
```
# 28. Quick Start — For Non-Technical Users

If Python and Git are already installed, the simplest workflow is:

### Step 1 — Get the project

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Open the project folder:

```bash
cd <YOUR_REPOSITORY_FOLDER>
```

### Step 2 — Create the environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3 — Install packages

```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env`

Copy:

```text
.env.example
```

to:

```text
.env
```

Then add your Groq API key:

```env
GROQ_API_KEY=YOUR_ACTUAL_GROQ_API_KEY
```

### Step 5 — Make the database

Make sure:

```text
support_tickets.csv
```

is in the project folder.

Then run:

```bash
python data_ingestion.py
```

### Step 6 — Start FastAPI

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Keep this terminal open.

### Step 7 — Start Streamlit

Open another terminal in the same project folder, activate the environment, and run:

```bash
streamlit run customer_streamlit.py
```

### Step 8 — Open the application

Open the Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

### Step 9 — Use the application

Choose one of the features:

```text
Health
NL Query
Anomalies
```

For example, under **NL Query**, type:

```text
How many tickets are currently open?
```

and click:

```text
Submit
```

---

# 29. One-Command Startup

For Windows:

```cmd
run.bat
```

For Linux/macOS:

```bash
./run.sh
```

These scripts automate the database ingestion, FastAPI startup, and Streamlit startup steps.

The assessment requires the system to be startable with a single command, with examples such as `docker-compose up` or `uvicorn main:app`. fileciteturn0file0L126-L132

---

# 30. Assessment Requirements Covered

| Assessment Requirement | Implementation |
|---|---|
| Ingest CSV data | `data_ingestion.py` |
| Make data queryable | SQLite database `customer_support_tickets.db` |
| Natural-language questions | `POST /generate` + Groq LLM |
| Anomaly detection | `GET /anomalies` |
| REST API | FastAPI |
| Minimal UI | Streamlit |
| Health check | `GET /health` |
| LLM integration | Groq `AsyncGroq` |
| Dependencies | `requirements.txt` |
| Setup/documentation | `README.md` |
| Single-command startup | `run.bat` / `run.sh` |


---

## Project Flow — At a Glance

```text
support_tickets.csv
        |
        v
data_ingestion.py
        |
        v
customer_support_tickets.db
        |
        v
      app.py
   (FastAPI backend)
        |
        +----------------------+
        |                      |
        v                      v
   Groq LLM              Anomaly SQL
        |                      |
        v                      v
 Natural Language         Anomaly Results
      Query                    |
        |                      |
        +----------+-----------+
                   |
                   v
          customer_streamlit.py
                   |
                   v
                 User
```

The result is a local customer-support AI assistant that combines structured ticket data, SQLite querying, LLM-based natural-language understanding, anomaly detection, a REST API, and a Streamlit interface.
