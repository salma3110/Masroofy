# Masroofy - Expense Management System

Masroofy is a Django-based expense tracking and management application. It provides secure user authentication with PIN-based login, expense logging, and a dashboard for monitoring financial activities.

## Features

### 🔐 Authentication System
- **User Setup**: Create a single user account with name and PIN
- **PIN-Based Login**: Secure login using name and PIN authentication
- **Account Lockout**: Automatic account lockout after 3 failed login attempts
- **Lockout Timer**: 30-second cooldown before account unlock
- **Comprehensive Logging**: Track login attempts, failed authentications, and account status changes

### 💰 Expense Management
- **Add Expenses**: Log new expenses with category and amount
- **Expense History**: View all recorded expenses with dates and categories
- **Delete Expenses**: Remove expenses from history
- **Category Support**: Organize expenses by predefined categories

### 📊 Dashboard
- **Visual Overview**: Dashboard view for expense monitoring

## Project Structure

```
masroofy/
├── authentication/        # User authentication app
│   ├── models.py         # User model with PIN and lockout tracking
│   ├── views.py          # Login, setup, and lockout views
│   ├── urls.py           # Authentication URL routes
│   ├── templates/        # HTML templates for auth views
│   │   ├── login.html    # Login form (name + PIN)
│   │   ├── setup.html    # Initial user setup
│   │   └── lockout.html  # Account lockout message
│   ├── static/           # CSS and static files
│   └── migrations/       # Database migrations
│
├── expenses/             # Expense tracking app
│   ├── models.py         # Category and Log models
│   ├── views.py          # Expense CRUD operations
│   ├── urls.py           # Expense URL routes
│   ├── templates/        # HTML templates for expenses
│   │   ├── add_expense.html    # Add expense form
│   │   └── history.html        # View expenses
│   └── migrations/       # Database migrations
│
├── dashboard/            # Dashboard app
│   ├── models.py         # Dashboard data models
│   ├── views.py          # Dashboard view
│   ├── urls.py           # Dashboard URL routes
│   ├── templates/        # Dashboard templates
│   │   └── dashboard.html
│   └── migrations/       # Database migrations
│
├── masroofy/             # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Root URL configuration
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
│
├── db.sqlite3            # SQLite database
├── manage.py             # Django management command
└── README.md             # This file
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)

### 2. Clone/Navigate to Project
```bash
cd path/to/Masroofy
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### Initial Setup
1. Navigate to `http://localhost:8000/setup/`
2. Enter your desired username and PIN
3. Submit to create your account

### Login
1. Go to `http://localhost:8000/auth/login/`
2. Enter your username and PIN
3. Click Login
4. **Note**: After 3 failed attempts, your account will be locked for 30 seconds

### Managing Expenses
1. After successful login, you're redirected to `http://localhost:8000/dashboard/dashboard/`
2. **Add Expense**: Click "Add" to log a new expense with amount and category
3. **View History**: Go to "History" to see all recorded expenses
4. **Delete Expense**: Remove any expense from the history view

## URL Routes

| Path | Purpose |
|------|---------|
| `/auth/setup/` | Initial user account creation |
| `/auth/login/` | User login with name and PIN |
| `/auth/lockout/` | Account lockout page |
| `/expenses/add/` | Add new expense |
| `/expenses/history/` | View expense history |
| `/expenses/delete/<id>/` | Delete specific expense |
| `/dashboard/dashboard/` | Main dashboard view |
| `/admin/` | Django admin panel |

## Database Models

### User Model (Authentication)
```python
- name: CharField (max 100 characters)
- pin: CharField (hashed, max 255 characters)
- failed_attempts: IntegerField (tracks login failures)
- is_locked: BooleanField (account lockout status)
- lock_time: DateTimeField (timestamp of lockout)
```

### Category Model (Expenses)
```python
- name: CharField (category name, max 100 characters)
```

### Log Model (Expenses)
```python
- amount: FloatField (expense amount)
- date: DateField (auto-populated with current date)
- category: ForeignKey (linked to Category)
```

## Security Features

- **PIN Hashing**: User PINs are hashed using Django's password hashing algorithm
- **Account Lockout**: Automatic 30-second lockout after 3 failed login attempts
- **CSRF Protection**: Django CSRF tokens on all forms
- **Logging**: Comprehensive authentication and login event logging

## Logging

The application includes detailed logging for authentication events:
- ✅ Successful logins
- ❌ Failed login attempts
- 🔒 Account lockout events
- 🔓 Account unlock events
- 👤 User lookup failures

Logs are written to the console and can be configured in Django settings.

## Admin Panel

Access Django admin at `/admin/` to:
- Manage users and their lockout status
- View and edit expense categories
- Review and delete expense logs
- Access the admin panel (requires superuser account)

### Create Superuser
```bash
python manage.py createsuperuser
```

## Future Enhancements

- [ ] Multiple user support
- [ ] Expense filtering and sorting
- [ ] Monthly/yearly expense reports
- [ ] Export expense data to CSV/PDF
- [ ] Recurring expense templates
- [ ] Budget alerts and limits
- [ ] Mobile-responsive design improvements
- [ ] Two-factor authentication

## Troubleshooting

### Virtual Environment Not Activating (Git Bash)
```bash
# Use this command in Git Bash instead of .bat file
source .venv/Scripts/activate
```

### Database Issues
```bash
# Reset database and migrations
python manage.py migrate authentication zero
python manage.py migrate expenses zero
python manage.py migrate
```

### Port Already in Use
```bash
python manage.py runserver 8001
```

## Contributing

For bug reports or feature requests, please document the issue clearly with steps to reproduce.

## License

This project is for educational purposes.

## Author

Created by JoJo

---

**Last Updated**: May 3, 2026
