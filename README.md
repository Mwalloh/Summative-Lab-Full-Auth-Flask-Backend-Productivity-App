# Summative-Lab-Full-Auth-Flask-Backend-Productivity-App

## Overview

This project demonstrates authentication and session management in Flask using both traditional session-based and JWT (JSON Web Token) authentication approaches.

## Features

- JWT token generation and validation
- Client authentication patterns
- User management

## Usage

1. Fork and clone the repo

```bash
git clone git@github.com:Mwalloh/Summative-Lab-Full-Auth-Flask-Backend-Productivity-App.git
```

2. Install dependencies

```bash
pipenv install 
```
3. Activate virtual environment

```python
pipenv shell
```

4. Set up the database

```bash
flask db init
flask db migrate
flask db upgrade head
```
5. Seed the database

```bash
python3 server/seed.py
```

6. Activate server

```bash
python3 server/app.py
```

7. Use a HTTP client like **Postman** or **curl** to interact with the API at the localhost: **_localhost:5555_**.

## API endpoints

1. `GET /entries` -> Get all journal_entries.
2. `POST /entries` -> Create a journal_entry.
3. `PATCH /entries/<id>` -> Update a certain journal_entry by id.
4. `DELETE /entries/<id>` -> Delete a journal_entry by id.

## Project Structure

```
├── 📁 server
│   ├── 📁 migrations
│   │   ├── 📁 versions
│   │   │   └── 🐍 1359bc779684_initial_migration.py
│   │   ├── 📄 README
│   │   ├── ⚙️ alembic.ini
│   │   ├── 🐍 env.py
│   │   └── 📄 script.py.mako
│   ├── 🐍 app.py
│   ├── 🐍 models.py
│   └── 🐍 seed.py
├── ⚙️ .gitignore
├── 📄 Pipfile
└── 📝 README.md
```

## Technologies

- **Flask**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **Flask-Bcrypt**
- **Flask-JWT-Extended**
- **Marshmallow**

## License

**MIT License**