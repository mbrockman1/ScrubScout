# ScrubScout 🚀

[![Django](https://img.shields.io/badge/Django-4.2+-blue)](https://www.djangoproject.com/) [![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org/) [![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple)](https://getbootstrap.com/)

ScrubScout is a **Minimum Viable Product (MVP)** web application built with Django for healthcare travel professionals (e.g., nurses, doctors) to discover, review, and rate facilities like hospitals, clinics, and travel agencies. Inspired by Yelp but tailored for the healthcare industry, it allows users to search for places, share verified experiences (e.g., staffing, pay, housing), and moderate content for trust and safety.

This project focuses on core features: user authentication, place search/listings, review creation/editing, and basic moderation. It's designed for scalability—start local, deploy to production easily.

## Features (MVP)
- **User Authentication**: Signup, login, logout, and profile (with display name for reviews).
- **Search & Discovery**: Google/Yelp-style homepage with hero search bar. Results page with filters (tags, sort by rating/reviews), listings, and navigation.
- **Place Management**: Add/view places (hospitals, clinics) with details like category, address, tags (e.g., "ER, PT"), and aggregated ratings/reviews.
- **Reviews**: Create, edit (owner-only), and view reviews with ratings (1-5 stars), titles, and body text. Auto-updates place averages/counts via signals.
- **Moderation**: Users report reviews; staff approve/reject via Django admin dashboard.
- **Responsive UI**: Bootstrap 5 for mobile-friendly design. Consistent navbar across pages.
- **Admin Tools**: Seed data (e.g., sample places), manage users/places/reviews/reports.
- **Security Basics**: CSRF protection, duplicate review prevention, staff-only moderation.

Future expansions (see [TODO](#todo)) include advanced search, maps integration, and user verification.

## Tech Stack
- **Backend**: Django 4.2+ (ORM, auth, admin), Python 3.10+.
- **Database**: SQLite (local dev); PostgreSQL recommended for production.
- **Frontend**: HTML/CSS/JS with Bootstrap 5 (CDN for MVP; staticfiles ready).
- **Images/Media**: Pillow for avatars (optional uploads).
- **Other**: `python-dotenv` for env vars, Django signals for rating calculations.
- **Dependencies**: See `requirements.txt` (e.g., Django, Pillow, python-dotenv, dj-database-url).

No JavaScript frameworks (vanilla JS for simple interactions like sort dropdowns).

## Local Setup
Follow these steps to get ScrubScout running on your machine (tested on macOS with Python 3.13).

### Prerequisites
- Python 3.10+ (install via [pyenv](https://github.com/pyenv/pyenv) or Homebrew: `brew install python`).
- Git (for cloning).
- A code editor (e.g., VS Code).

### Step 1: Clone and Install
```bash
git clone https://github.com/yourusername/scrubscout.git  # Replace with your repo URL
cd scrubscout
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (on Windows: venv\Scripts\activate)
pip install -r requirements.txt  # Install dependencies
```

### Step 2: Configure Environment
- Copy the example env file:
  ```bash
  cp .env.example .env  # If .env.example exists; otherwise create .env manually
  ```
- Edit `.env` (in your editor) and fill in values:
  ```
  # Django Secret Key (generate: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
  SECRET_KEY=your-super-secret-random-key-here

  # Development Settings
  DEBUG=True
  ALLOWED_HOSTS=localhost,127.0.0.1

  # Database (SQLite for local; change to postgres://... for prod)
  DATABASE_URL=sqlite:///db.sqlite3
  ```
- **Security Note**: Never commit `.env` (it's in `.gitignore`). For production, use server env vars.

### Step 3: Database and Migrations
```bash
python manage.py makemigrations  # Create migration files (if changes)
python manage.py migrate  # Apply migrations (creates tables)
python manage.py createsuperuser  # Create admin user (e.g., username: admin, email: admin@example.com, password: yourchoice)
```

### Step 4: Seed Sample Data (Optional but Recommended)
- Run the custom management command to add test places (e.g., "City Hospital"):
  ```bash
  python manage.py seed_places  # Assumes you have this command in places/management/commands/
  ```
- Or use Django admin (`/admin/` after running the server) to add places manually:
  - Login as superuser.
  - Add Places (e.g., Name: "City Hospital", Slug: "city-hospital", Category: "Hospital", Address: "123 Main St", Tags: "ER,PT").

### Step 5: Run the Server
```bash
python manage.py runserver
```
- Visit `http://127.0.0.1:8000/` (homepage).
- Test flows:
  - Signup/Login at `/accounts/signup/` or `/accounts/login/`.
  - Search for "hospital" → View results at `/search/?q=hospital`.
  - Click a place → Detail at `/places/city-hospital/` → Add review (if logged in).
  - Admin: `/admin/` for moderation (e.g., view reports).

### Troubleshooting
- **Migration Errors**: Run `python manage.py showmigrations` to check status; reset with `python manage.py migrate --fake-initial` if needed.
- **Static Files Missing**: `python manage.py collectstatic --noinput` (for production).
- **No Places Show**: Seed data or check `places/models.py`.
- **Env Issues**: Ensure `load_dotenv()` is in `settings.py`. Restart server after `.env` changes.
- **Mac-Specific**: If `.DS_Store` files appear, they're ignored by `.gitignore`.

## Project Structure
```
scrubscout/
├── manage.py                 # Django entrypoint
├── requirements.txt          # Python dependencies
├── .gitignore               # Ignores venv, db.sqlite3, .env, etc.
├── .env.example             # Template for env vars (commit this)
├── README.md                # This file
├── scrubscout/              # Main project (settings, URLs)
│   ├── settings.py          # Config (load .env, INSTALLED_APPS, etc.)
│   ├── urls.py              # Root URLs (includes app URLs)
│   └── wsgi.py              # Production server entry
├── accounts/                # User auth (models: CustomUser, views: login/signup, templates/)
├── core/                    # Shared (base.html, home view/URLs for landing)
├── places/                  # Places (models: Place with reviews FK, views: detail, templates: place_detail.html)
├── reviews/                 # Reviews (models: Review, views: create/edit, signals for ratings)
├── search/                  # Search (views: search_results, templates: results.html with filters)
├── moderation/              # Reports (models: ReviewReport, admin integration)
├── static/                  # CSS/JS/images (source; collectstatic builds to staticfiles/)
└── templates/               # App-specific (e.g., search/results.html; core/base.html extends)
    └── admin/               # Django admin customizations (optional)
```

## Deployment
For quick production (e.g., Heroku, Render, or Railway):
1. **Database**: Switch to PostgreSQL in `.env` (e.g., `DATABASE_URL=postgres://user:pass@host/db`).
2. **Static/Media**: Set `DEBUG=False`, run `collectstatic`. Use WhiteNoise (`pip install whitenoise`) for static serving.
3. **Heroku Example**:
   - Install Heroku CLI, create app: `heroku create scrubscout-app`.
   - Set env vars: `heroku config:set SECRET_KEY=... DEBUG=False`.
   - Push: `git push heroku main`.
   - Run migrations: `heroku run python manage.py migrate`.
   - Open: `heroku open` (visits your live site).
4. **Env Vars**: Use platform dashboard to set `SECRET_KEY`, `DATABASE_URL`, etc. (no `.env` file in prod).
5. **Media Storage**: For user uploads (avatars), integrate Cloudinary/AWS S3 later.

See `settings/production.py` (if you add it) for prod-specific configs.

## Contributing
1. Fork the repo and clone locally.
2. Create a branch: `git checkout -b feature/new-feature`.
3. Make changes, test locally (`python manage.py test` if tests added).
4. Commit: `git commit -m "Add new feature"`.
5. Push and PR: `git push origin feature/new-feature`.

Follow PEP 8 for Python code. Add tests for new features. Questions? Open an issue!

## License
MIT License (or your choice—add a `LICENSE` file).

## TODO
Here's a prioritized TODO list to evolve the MVP into a full app. Categorized by effort/impact.

### Core Features (High Priority, 1-2 Days)
- [ ] **Complete Review Flows**: Implement `reviews/views.py` for create/edit forms (use Django forms, e.g., `ReviewForm`). Add URLs like `/reviews/places/<slug>/new/` (name: 'create_review') and `/reviews/<id>/edit/`.
- [ ] **User Profiles**: Flesh out `accounts/views.py` for profile view/edit (update `display_name`, avatar upload via `MEDIA_ROOT`). Add URL: `/accounts/profile/` (name: 'profile').
- [ ] **Report Handling**: Add staff views in `moderation/` to approve/reject reports (e.g., auto-hide reported reviews until moderated).
- [ ] **Pagination**: Add to search results (`/search/`) and place reviews (use `django.core.paginator.Paginator`; e.g., `?page=2`).
- [ ] **Category Filtering**: Make search sidebar checkboxes functional (e.g., `places = places.filter(category__icontains=request.GET.get('category'))`).

### UX/Polish (Medium Priority, 2-3 Days)
- [ ] **Advanced Search**: Full-text search with Haystack/Elasticsearch or Postgres `tsvector`. Add autocomplete to search bar (via htmx or JS).
- [ ] **Maps Integration**: Embed Google Maps in place detail (use `GOOGLE_MAPS_API_KEY` from `.env`; geocode address).
- [ ] **Stars/Ratings UI**: Use a JS library (e.g., Font Awesome stars) for interactive ratings in review forms.
- [ ] **Email Notifications**: Send emails for review approvals, reports, or password resets (use Django's `send_mail`; configure SMTP in `.env`).
- [ ] **Breadcrumbs & SEO**: Add navigation breadcrumbs (e.g., Home > Search > Place) and meta tags.
- [ ] **Tests**: Write unit/integration tests (e.g., `python manage.py test`) for views, models, and auth flows.

### Security & Performance (Medium Priority, 1 Day)
- [ ] **User Verification**: Add email confirmation on signup (Django's `User` with `is_active=False` until verified).
- [ ] **Rate Limiting**: Prevent spam reviews (e.g., django-ratelimit on review creation).
- [ ] **CSRF & Permissions**: Audit for custom permissions (e.g., `@staff_member_required` for moderation).
- [ ] **Caching**: Add Redis/Memcached for search results (django-redis).

### Deployment & Scaling (Low Priority, 1-2 Days)
- [ ] **Production Settings**: Create `settings/production.py` (DEBUG=False, secure cookies, logging). Use `gunicorn` + `Procfile` for Heroku.
- [ ] **CI/CD**: Set up GitHub Actions for tests/migrations on push.
- [ ] **Monitoring**: Integrate Sentry for error tracking or Google Analytics.
- [ ] **API Layer**: Add Django REST Framework for mobile app (e.g., `/api/places/` endpoints).

### Nice-to-Haves (Future, 3+ Days)
- [ ] **Agencies/Locations Models**: Expand beyond `Place` (e.g., separate models for agencies with pay/stipend fields).
- [ ] **Social Features**: Follow users, threaded comments on reviews.
- [ ] **Mobile App**: React Native frontend consuming DRF API.
- [ ] **Monetization**: Affiliate links for travel agencies or premium features.