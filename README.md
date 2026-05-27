<<<<<<< HEAD
# Plant Tracker

A Django + PostgreSQL web app to track plants, care activities, lifecycle status, and analytics.

## Features

- Plant CRUD with details:
  - Biological name
  - Local name
  - English name
  - Family/build name
  - Care notes
  - Image upload
  - Planted date and status
- Care activity logs per plant (watering, fertilizer, pruning, repotting, other)
- Lifecycle management:
  - Mark as removed (soft delete)
  - Permanent delete
- Dashboard chart:
  - Plants added over time
  - Date range filter

## Setup

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Configure PostgreSQL env vars from `.env.example`.
3. Run migrations:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
4. Create admin user (optional):
   - `python manage.py createsuperuser`
5. Start server:
   - `python manage.py runserver`

## Local SQLite fallback

For quick local runs without PostgreSQL:

- PowerShell: `$env:DB_ENGINE="sqlite"`
- Then run migrations and start server normally.
=======
# planter
>>>>>>> 94f57b7876c8d1eeaac3862362d6b3d4d3398587
