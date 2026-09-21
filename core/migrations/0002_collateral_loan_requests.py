import django.db.models.deletion
from django.db import migrations, models

COLLATERAL = [
    ("vehicle", "Vehicle (Car, Truck, Motorbike)"),
    ("property", "Land / Property"),
    ("jewelry", "Gold & Jewelry"),
    ("electronics", "Electronics"),
    ("equipment", "Machinery & Equipment"),
    ("other", "Other Valuable Asset"),
]
STATUS = [
    ("new", "New"),
    ("reviewing", "Under Review"),
    ("approved", "Approved"),
    ("declined", "Declined"),
    ("funded", "Funded"),
]


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.DeleteModel(name="Lead"),
        migrations.AlterField(
            model_name="service",
            name="category",
            field=models.CharField(choices=COLLATERAL, max_length=20),
        ),
        migrations.AlterField(
            model_name="service",
            name="icon",
            field=models.CharField(default="🚗", help_text="Emoji shown on the card", max_length=8),
        ),
        migrations.AlterField(
            model_name="service",
            name="rate_from",
            field=models.CharField(blank=True, help_text='Short highlight, e.g. "Same-day valuation"', max_length=40),
        ),
        migrations.CreateModel(
            name="LoanRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("whatsapp_number", models.CharField(max_length=30)),
                ("loan_amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("collateral_type", models.CharField(choices=COLLATERAL, max_length=20)),
                ("collateral_description", models.TextField(blank=True)),
                ("status", models.CharField(choices=STATUS, default="new", max_length=12)),
                ("admin_notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="CollateralImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="collateral/%Y/%m/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("loan_request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="core.loanrequest")),
            ],
        ),
    ]
