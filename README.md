# Task Management Backend

## Features

- Create, read, update, and delete tasks and labels.
- Users can only perform CRUD operations on their own tasks and labels.
- Custom filters to display tasks by label in the admin interface.
- JWT authentication for securing API endpoints.

## Setup Instructions

### Prerequisites

- Python 3.x
- Virtualenv (optional but recommended)
- Django 4.2.x
- Django Rest Framework
- SQLite (default database)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AlanPoAlSk/backend-challenge.git
   cd backend-challenge
   ```

2. Create and activate a virtual environment:
   ```bash
   virtualenv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory and add the following:
     ```
     DJANGO_SECRET_KEY=your_secret_key_here
     ```

5. Apply database migrations:
   ```bash
   python3 manage.py migrate
   ```

6. Create superuser and other users (as specified in challenge.md):
   ```bash
   python3 manage.py createsuperuser
   python3 manage.py shell
   ```
   In the shell:
   ```python
   from django.contrib.auth.models import User
   User.objects.create_user('user1', password='your_password_here', is_staff=True).save()
   User.objects.create_user('user2', password='your_password_here', is_staff=True).save()
   ```

