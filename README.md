# Autonomous AI Code Review & Security Audit Platform

An AI-powered code review platform that analyzes Python code, identifies potential bugs and security risks, generates suggested fixes, and stores review history in MySQL.

## Features

- **AI Code Analysis:** Analyzes code purpose, logic, and potential bugs.
- **AI Security Audit:** Reviews code for potential security vulnerabilities.
- **AI Fix Suggestions:** Generates improved code suggestions and explains changes.
- **Multi-Agent Workflow:** Coordinates four AI agents using LangGraph.
- **Static Analysis:** Uses Ruff to detect code quality issues.
- **REST API:** Built with FastAPI.
- **Database Integration:** Stores code reviews and review history in MySQL.
- **Interactive API Documentation:** Tests endpoints through Swagger UI.

## Tech Stack

- Python
- FastAPI
- LangGraph
- LangChain
- Google Gemini API
- MySQL
- SQLAlchemy
- Ruff
- Pydantic

## AI Agents

1. **Code Analyzer Agent** — analyzes code and potential logic issues.
2. **Security Auditor Agent** — identifies potential security risks.
3. **Fix Generator Agent** — suggests corrected code.
4. **Review Reporter Agent** — generates the final review report.

## Project Structure

```text
Autonomous AI Code Review & Security Audit Platform/
├── main.py
├── agent_workflow.py
├── schemas.py
├── database.py
├── models.py
├── requirements.txt
├── .env
├── .env.example
└── README.md
```

*The structure above describes the main files; your actual project may contain additional files.*

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd "Autonomous AI Code Review & Security Audit Platform"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost:3306/code_review_db
```

Replace the placeholders with your actual credentials. Ensure the MySQL database `code_review_db` exists.

**Security:** Never commit `.env` or expose your API key or database password publicly.

### 5. Run the application

```bash
python -m uvicorn main:app --reload
```

### 6. Open API documentation

Visit:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check application status |
| GET | `/health` | Health check |
| POST | `/reviews` | Submit code for AI review |
| GET | `/reviews` | List saved reviews |
| GET | `/reviews/{review_id}` | Retrieve a specific review |

## Example Request

Submit a review using `POST /reviews`:

```json
{
  "filename": "test.py",
  "code": "import os\ndef read_file(path):\n    return open(path).read()\n"
}
```

The API returns a review containing findings, an AI-generated report, and suggested fixes.

## Limitations

- AI-generated findings and fixes may be inaccurate and require human verification.
- Static analysis does not detect every possible vulnerability.
- Suggested fixes are not automatically applied or guaranteed to be tested.
- Gemini API access and usage limits depend on the configured account.

## Future Improvements

- GitHub repository and pull request integration.
- Automated unit testing of suggested fixes.
- Authentication and user-specific review history.
- A web-based dashboard for reviewing findings.

## License

This project is intended for educational and portfolio purposes.
