# 🚗 CarBazar — Full-Stack Django Car Marketplace

A modern, production-ready car marketplace built with Django, PostgreSQL, Bootstrap 5, and Django REST Framework.

---

## 🌟 Features

- **Homepage** — Hero search, featured listings, brand grid, recent cars
- **Browse & Search** — Filter by brand, category, fuel type, transmission, price, year
- **Car Details** — Image carousel, gallery, specs, contact seller modal
- **CRUD** — Create, edit, delete car listings with multi-image upload
- **Dashboard** — Statistics, manage all cars (approve/reject), brands, categories
- **REST API** — Full API at `/api/` with filters and search
- **Django Admin** — Full admin at `/admin/`

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2, Python |
| Database | PostgreSQL (SQLite fallback) |
| API | Django REST Framework |
| Frontend | Bootstrap 5, Vanilla JS, Inter + Outfit fonts |
| Images | Pillow, local MEDIA_ROOT |
| Static | WhiteNoise |

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- PostgreSQL (or SQLite for quick start)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and edit:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://carbazar_user:carbazar_pass@localhost:5432/carbazar_db
```

**For SQLite (quick start)**, set:
```env
DATABASE_URL=sqlite:///db.sqlite3
```

### 4. PostgreSQL Setup (if using PostgreSQL)

```sql
CREATE DATABASE carbazar_db;
CREATE USER carbazar_user WITH PASSWORD 'carbazar_pass';
GRANT ALL PRIVILEGES ON DATABASE carbazar_db TO carbazar_user;
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## 📁 Project Structure

```
carbazar/
├── manage.py
├── .env
├── requirements.txt
├── carbazar/           # Django project config
│   ├── settings.py
│   └── urls.py
├── apps/
│   └── cars/           # Main app (models, views, API)
│       ├── models.py   # Brand, Category, Car, CarImage
│       ├── views.py    # All frontend + dashboard views
│       ├── api_views.py # REST API views
│       ├── serializers.py
│       ├── forms.py
│       └── urls.py / api_urls.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── cars/           # list, detail, create, update, delete
│   └── dashboard/      # index, cars, brands, categories
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## 🔗 URLs

| URL | Description |
|---|---|
| `/` | Homepage |
| `/cars/` | Browse all cars |
| `/cars/<id>/` | Car detail |
| `/cars/new/` | Create listing |
| `/cars/<id>/edit/` | Edit listing |
| `/brand/<slug>/` | Cars by brand |
| `/category/<slug>/` | Cars by category |
| `/dashboard/` | Admin dashboard |
| `/admin/` | Django admin |
| `/api/cars/` | Car API |
| `/api/brands/` | Brand API |
| `/api/categories/` | Category API |
| `/api/stats/` | Site stats API |

---

## 📸 Sample Data

Use Django Admin or the API to add:
1. A few **Brands** (Toyota, Honda, BMW...)
2. A few **Categories** (Sedan, SUV, Hatchback...)
3. **Cars** with images

---

## 🧪 API Examples

```bash
# List available cars
GET /api/cars/

# Filter by fuel type
GET /api/cars/?fuel_type=electric

# Filter by brand slug
GET /api/cars/?brand=toyota

# Search
GET /api/cars/?search=corolla

# Sort by price
GET /api/cars/?ordering=price

# Site stats
GET /api/stats/
```
