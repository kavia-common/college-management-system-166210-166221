# college-management-system-166210-166221

Backend (Flask) for College Management System

- Run locally:
  - python -m venv venv && source venv/bin/activate
  - pip install -r college_management_backend/requirements.txt
  - cd college_management_backend
  - cp .env.example .env  # set env vars as needed
  - python run.py

- API Docs:
  - After running, visit /docs on the backend URL to see Swagger UI.

- OpenAPI JSON:
  - python college_management_backend/generate_openapi.py
  - Output: college_management_backend/interfaces/openapi.json