from django.core.management.base import BaseCommand
from salon.models import Service, Product


class Command(BaseCommand):
    help = "Seed the database with sample services and products."

    def handle(self, *args, **options):
        services = [
            ("Classic Haircut", "hair", "Wash, cut and style.", 250, 45),
            ("Blow Out", "hair", "Wash and professional blow dry.", 180, 30),
            ("Full Colour", "hair", "Full head colour treatment.", 650, 120),
            ("Gel Manicure", "nails", "Long-lasting gel polish manicure.", 220, 45),
            ("Classic Pedicure", "nails", "Soak, scrub and polish.", 250, 50),
            ("Acrylic Full Set", "nails", "Full set of acrylic extensions.", 400, 90),
            ("Bridal Makeup", "makeup", "Full glam makeup for your big day.", 900, 90),
            ("Everyday Makeup", "makeup", "Natural, everyday makeup look.", 350, 40),
        ]
        for name, cat, desc, price, duration in services:
            Service.objects.get_or_create(
                name=name,
                defaults={"category": cat, "description": desc, "price": price, "duration_minutes": duration},
            )

        products = [
            ("Argan Oil Shampoo", "Nourishing shampoo for dry hair.", 145, 30),
            ("Nail Polish - Ruby Red", "Long-wear glossy nail polish.", 89, 50),
            ("Matte Foundation", "Full coverage matte finish foundation.", 260, 20),
            ("Hydrating Face Mist", "Refreshing rosewater face mist.", 120, 40),
            ("Cuticle Oil", "Nourishing oil for healthy cuticles.", 75, 60),
        ]
        for name, desc, price, stock in products:
            Product.objects.get_or_create(
                name=name, defaults={"description": desc, "price": price, "stock": stock}
            )

        self.stdout.write(self.style.SUCCESS("Sample services and products created."))
