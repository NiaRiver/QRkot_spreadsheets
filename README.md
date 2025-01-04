# QRkot_spreadseets

QRKot is a FastAPI-based application for a cat charity foundation that helps manage and track donations for various cat-support projects.

## Description

The QRKot Foundation collects donations for various targeted projects aimed at supporting cats, including:
- Medical services for cats in need
- Setting up cat colonies
- Food for abandoned cats
- Other cat population support initiatives

## Features

### Projects
- Multiple charity projects can be active simultaneously
- Each project has a name, description, and target amount
- Projects are automatically closed once the target amount is reached
- Projects follow FIFO (First In, First Out) principle for receiving donations
- Donations are automatically invested in the earliest opened project

### Donations
- Users can make donations with optional comments
- Donations are not project-specific and go to the common fund
- Donations are automatically distributed to open projects
- Excess donations are held for future projects

### User Roles
- **Anonymous Users**: Can view all projects
- **Registered Users**: Can make donations and view their donation history
- **Administrators**: Can create projects, delete unfunded projects, and modify existing projects

## Technical Stack

- FastAPI
- SQLAlchemy
- FastAPI Users
- Pydantic
- JWT authentication
- AIOGoogle

## Installation
1. Clone the repository:
```bash
git clone git@github.com:NiaRiver/QRkot_spreadsheets.git && \
cd QRkot_spreadsheets
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the root directory with the following variables:
```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=your_secret_key
```

## Running the Application

1. Getting db ready:
```bash
alembic upgrade head
```

2. Start the server:
```bash
uvicorn app.main:app --reload
```

3. Access the API documentation:
- [Swagger UI Documentation](http://localhost:8000/docs)
- [ReDoc Documentation](http://localhost:8000/redoc)

## API Endpoints

### Projects
- `GET /charity_project/` - List all projects
- `POST /charity_project/` - Create new project (admin only)
- `DELETE /charity_project/{project_id}/` - Delete project (admin only)
- `PATCH /charity_project/{project_id}/` - Update project (admin only)

### Donations
- `GET /donation/` - List user's donations
- `GET /donation/my` - List authenticated user's donations
- `POST /donation/` - Make a donation

### GOOGLE Cloud Api Services
- `POST /google` - Create projects completion rate report spreadsheet

### Authentication
- `POST /auth/jwt/login` - Get JWT token
- `POST /auth/register` - Register new user
- `GET /users/me` - Get current user info

## Author

### NIA River

- **Contact the creator**
  - Email: [nianate@yandex.ru](mailto:nianate@yandex.ru)
  - GitHub: github.com/NiaRiver/