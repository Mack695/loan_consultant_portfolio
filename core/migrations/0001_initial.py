from django.db import migrations, models

LOAN_TYPES = [
    ("refinance", "Mortgage Refinance"),
    ("business", "Small Business Loans"),
    ("commercial", "Commercial Real Estate"),
    ("debt", "Personal Debt Consolidation"),
]


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("category", models.CharField(choices=LOAN_TYPES, max_length=20)),
                ("description", models.TextField()),
                ("icon", models.CharField(default="🏠", help_text="Emoji shown on the card", max_length=8)),
                ("rate_from", models.CharField(blank=True, help_text='e.g. "From 5.9% APR"', max_length=40)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("client_name", models.CharField(max_length=100)),
                ("client_role", models.CharField(blank=True, max_length=120)),
                ("quote", models.TextField()),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=30)),
                ("loan_amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("loan_type", models.CharField(choices=LOAN_TYPES, max_length=20)),
                ("preferred_datetime", models.DateTimeField()),
                ("message", models.TextField(blank=True)),
                ("is_contacted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
