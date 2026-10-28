# Little Lemon Restaurant API

Django + Django REST Framework application based on the existing Little Lemon booking website. Includes HTML booking pages, booking APIs, menu/category APIs, token authentication, role-based access, cart and order workflows.

## Requirements
- Python 3.10+
- MySQL Server 8+
- MySQL development tools if `mysqlclient` needs compilation

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DB_NAME="littlelemon"
$env:DB_USER="root"
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```
Create a MySQL database named `littlelemon`, then:
```powershell
python manage.py makemigrations restaurant
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Main routes
- Website: `/`
- Booking page: `/book/`
- Reservations page: `/reservations/`
- Booking API: `GET/POST /api/bookings/`
- One booking: `/api/bookings/<id>/`
- Categories: `/api/categories/`
- Menu items: `/api/menu-items/`, `/api/menu-items/<id>/`
- Cart: `GET/POST/DELETE /api/cart/menu-items`
- Orders: `GET/POST /api/orders`; details `/api/orders/<id>`
- Manager group users: `/api/groups/manager/users`
- Delivery crew users: `/api/groups/delivery-crew/users`
- Token login: `POST /api-token-auth/` (JSON: `username`, `password`)
- Djoser registration: `POST /auth/users/`

## Authentication
For protected endpoints send `Authorization: Token YOUR_TOKEN`. Create groups named `Manager` and `Delivery Crew` in Django admin. Managers/staff can manage menu items and group membership. Customers can manage their own cart and orders. Delivery crew can see assigned orders and update only status.

## Useful Insomnia examples
Create a menu item (authenticate as a Manager):
`POST http://127.0.0.1:8000/api/menu-items/`
```json
{"title":"Pasta","price":"12.50","featured":false,"category_id":1}
```
Create a booking:
`POST http://127.0.0.1:8000/api/bookings/`
```json
{"first_name":"Asha","reservation_date":"2026-11-01","reservation_slot":12}
```
Login for a token:
`POST http://127.0.0.1:8000/api-token-auth/`
```json
{"username":"your_username","password":"your_password"}
```

## Tests
```powershell
python manage.py test
```

## Notes
- Database credentials should be supplied through environment variables and never committed to GitHub.
- Run migrations after changing models.
- The project ZIP is a starting implementation; run the checks and tests in your local environment and fix any environment-specific database or dependency issues before submission.
