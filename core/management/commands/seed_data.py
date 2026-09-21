from django.core.management.base import BaseCommand

from core.models import Service, Testimonial

SERVICES = [
    ("Vehicles", "vehicle", "🚗", "Cars, trucks and motorbikes. You keep the paperwork safe with us while the loan runs.", "Fast valuation"),
    ("Land & Property", "property", "🏡", "Use title deeds for land or buildings to unlock larger loan amounts.", "Higher loan limits"),
    ("Gold & Jewelry", "jewelry", "💍", "Gold, diamonds and fine jewelry appraised on the spot.", "Same-day appraisal"),
    ("Electronics", "electronics", "💻", "Laptops, phones, cameras and other high-value devices.", "Quick approval"),
    ("Machinery & Equipment", "equipment", "🛠️", "Generators, tools and work equipment with clear proof of ownership.", "Flexible terms"),
    ("Other Valuable Assets", "other", "📦", "Have something else of value? Send us photos and details for a review.", "Case-by-case"),
]

TESTIMONIALS = [
    ("Mark T.", "Borrowed against a vehicle", "I needed cash quickly for a family emergency. I sent photos on WhatsApp and had an offer the same day.", 5),
    ("Sara A.", "Borrowed against jewelry", "Honest valuation and no pressure. I got my jewelry back the day I repaid.", 5),
    ("David O.", "Borrowed against equipment", "Simple process and clear terms. Everything was explained before I signed.", 5),
    ("Priya N.", "Borrowed against a laptop", "The request form took two minutes and they replied fast. Very professional.", 5),
]


class Command(BaseCommand):
    help = "Load sample collateral types and testimonials (sample text, replace with your own)"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete existing services and testimonials first")

    def handle(self, *args, **options):
        if options["reset"]:
            Service.objects.all().delete()
            Testimonial.objects.all().delete()
        if not Service.objects.exists():
            for i, (title, cat, icon, desc, note) in enumerate(SERVICES):
                Service.objects.create(title=title, category=cat, icon=icon, description=desc, rate_from=note, order=i)
        if not Testimonial.objects.exists():
            for name, role, quote, rating in TESTIMONIALS:
                Testimonial.objects.create(client_name=name, client_role=role, quote=quote, rating=rating)
        self.stdout.write(self.style.SUCCESS("Sample data loaded."))
