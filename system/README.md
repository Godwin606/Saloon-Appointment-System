# Salon Booking System

The salon system now runs with:

- Django Framework
- Django Templates for the frontend
- SQLite database

## Run The System

```powershell
cd backend
python manage.py runserver 127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000
```

## Contact

```text
0785468022
```

## Demo Accounts

Customer accounts can only view and book their own appointments:

- `godwin` / `customer123`
- `christian` / `customer123`
- `matia` / `customer123`
- `angel` / `customer123`

The barber account can view and manage all appointments:

- `barber` / `barber123`

## Pages

- `/` - customer and barber sign-in choices
- `/customer-login/` - customer sign-in
- `/barber-login/` - barber sign-in
- `/appointments/` - appointments dashboard
- `/book/` - customer booking form
- `/feedback/` - feedback form
