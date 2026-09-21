# Collateral Loan Portfolio (Django)

## Run it
```bash
python -m venv venv
venv\Scripts\activate          # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data --reset   # sample collateral types + testimonials
python manage.py createsuperuser
python manage.py runserver
```
Site: http://127.0.0.1:8000/   Admin (loan requests + uploaded photos): http://127.0.0.1:8000/admin/

Upgrading from the earlier consultation version: `migrate` replaces the old Lead table with LoanRequest / CollateralImage.

## Customise
- Name, licence, phone, WhatsApp number, currency symbol: `SITE_INFO` in `portfolio_project/settings.py`
- Headshot: save as `core/static/images/consultant.jpg`
- Uploaded collateral photos are stored in `media/collateral/`
