________________________________________
Loan Eligibility API – README
________________________________________
Overview

This project demonstrates a loan eligibility service built with Django – a common web framework for python programming language. It accepts loan applications, calls mock Salary Verification and Credit Bureau APIs, applies eligibility rules, and returns structured JSON decisions. A simple UI shows both a guided form and a raw JSON playground.
________________________________________
Tech Stack

For this assessment, Django was chosen for its speed, robustness, and security. It enables rapid deployment with built‑in scaffolding, ORM, and an admin interface that reduces development time significantly. Common security concerns are guaranteed in CSRF, XSS, and SQL injection protections are default, making it suitable for sensitive financial workflows. Its MTV architecture enforces clean separation of concerns, ensuring maintainability and scalability. With strong hosting support and migration tools, Django provides a fast, secure, and enterprise‑ready framework for building and deploying APIs like loan eligibility systems.

________________________________________
Architecture

•	Core API: Django views exposing JSON endpoints.

•	Mock services: Salary Verification and Credit Bureau implemented as separate endpoints, backed by mock_data.py.

•	UI demo: Index page with a centered form; JSON input and response displayed side by side.

•	Error handling: Explicit 404s for unknown IDs; JSON only responses for frontend reliability.
________________________________________
Endpoints

•	POST /api/loan/ → Submit loan application, returns eligibility decision.

•	GET /api/salary/{national_id} → Mock salary verification.

•	GET /api/credit/{national_id} → Mock credit bureau.

•	GET /clients/ → Dashboard showing mock datasets.
________________________________________
Eligibility Rules

•	Monthly salary ≥ 3 × monthly repayment.

•	Credit score ≥ 600.

•	No active defaults.

•	Maximum of 3 active loans.

•	Declined applications include reasons.
________________________________________

Loan Approval Logic

The system only approves loan applications for clients whose National ID is already registered in the system.

•	When a user submits an application, the backend checks the provided National ID against the mock salary and credit bureau records.

•	If the ID is not found, the application is automatically rejected.

•	To view the list of supported IDs, navigate to the Clients tab (/clients), which displays all mock records currently available for testing.
________________________________________
Running Locally
1.	Clone the repo: git clone https://github.com/TafadzwaZW/loan-eligibility-api.git
2.	cd loan-eligibility-api
3.	Create a virtual environment:	python -m venv .venv
4.	Activate the virtual environment: 	source .venv/bin/activate   # macOS/Linux
										.venv\Scripts\activate      # Windows
5.	Install dependencies:pip install -r requirements.txt
6.	Run migrations :	python manage.py migrate
7. 	Start server:		python manage.py runserver
8.	Open: → http://localhost:8000
________________________________________
Usage Examples
Sample JSON request:
{
  "national_id": "63-1552926G09",
  "loan_amount": 12000,
  "term_months": 18
}
curl example:
curl -X POST http://localhost:8000/api/loan/ \
  -H "Content-Type: application/json" \
  -d '{"national_id":"63-1552926G09","loan_amount":1200,"term_months":12}'
________________________________________
Improvements with More Time

•	Stronger validation (pydantic/Django forms).

•	Authentication and audit logging.

•	Resilience (timeouts, retries, circuit breakers).

•	Observability (structured logs, metrics).

•	Use a proper secure database not rely on mock data.

•	Unit/integration tests.

•	OpenAPI/Swagger documentation.

•	Nicer and responsive dashboard.

________________________________________
