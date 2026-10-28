# Little Lemon Restaurant API

A Django-based restaurant application using Django REST Framework and MySQL. The project includes restaurant booking pages, menu management, booking APIs, authentication, and order-related functionality.

## Requirements

- Python 3.10 or newer
- MySQL Server 8 or newer
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository.
2. Open a terminal in the project directory containing `manage.py`.
3. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a MySQL database named `littlelemon` and configure your database credentials using environment variables.

6. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create an administrator:

```bash
python manage.py createsuperuser
```

8. Start the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## API Endpoints

- `GET /api/menu-items/` — List menu items.
- `POST /api/menu-items/` — Create a menu item with appropriate permissions.
- `GET /api/categories/` — List menu categories.
- `GET /api/bookings/` — List bookings.
- `POST /api/bookings/` — Create a booking.
- `POST /api-token-auth/` — Obtain an authentication token.
- `POST /auth/users/` — Register a user, if configured.

Additional endpoints are documented in the project source.

## Testing

Run the automated tests:

```bash
python manage.py test
```

Use Insomnia or another REST client to test the endpoints.

## Notes

- Configure your own MySQL credentials locally.
- Never commit passwords, secret keys, or authentication tokens.
- Test database migrations, authentication, permissions, and API responses before submitting the project.
