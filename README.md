# Bella Beauty Studio

A simple Django app for a beauty salon (hair, nails, makeup) where clients can:
- Browse services and book appointments
- Browse and buy retail products
- View their appointment and order history

Staff manage everything (services, products, appointment statuses, orders) through the built-in Django admin.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # create a staff/admin login
python manage.py seed_salon        # optional: adds sample services & products

python manage.py runserver
```

Visit http://127.0.0.1:8000/

- Public site: browse services & products, sign up, book appointments, buy products
- Admin panel: http://127.0.0.1:8000/admin/ — manage services, products, appointment statuses, and orders

## Project structure

- `salon/models.py` — Service, Product, Appointment, Order, OrderItem
- `salon/views.py` — booking, purchasing, and account views
- `salon/templates/` — all HTML templates (pink/cream salon theme, no external CSS framework needed)
- `salon/management/commands/seed_salon.py` — sample data loader

## Notes on scope

This is intentionally minimal:
- "Buy Now" creates an order immediately (no cart or payment gateway) — plug in a payment processor like Stripe or PayFast for real payments.
- Appointments are requested by clients and left as "Pending" until staff confirm them in the admin.
- No email notifications are wired up yet, but Django's email backend makes that straightforward to add later.
