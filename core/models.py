from django.db import models

COLLATERAL_CHOICES = [
    ("vehicle", "Vehicle (Car, Truck, Motorbike)"),
    ("property", "Land / Property"),
    ("jewelry", "Gold & Jewelry"),
    ("electronics", "Electronics"),
    ("equipment", "Machinery & Equipment"),
    ("other", "Other Valuable Asset"),
]


class Service(models.Model):
    """A type of collateral shown on the landing page."""
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=COLLATERAL_CHOICES)
    description = models.TextField()
    icon = models.CharField(max_length=8, default="🚗", help_text="Emoji shown on the card")
    rate_from = models.CharField(max_length=40, blank=True, help_text='Short highlight, e.g. "Same-day valuation"')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} ({self.rating}/5)"


class LoanRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Under Review"),
        ("approved", "Approved"),
        ("declined", "Declined"),
        ("funded", "Funded"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=30)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    collateral_type = models.CharField(max_length=20, choices=COLLATERAL_CHOICES)
    collateral_description = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="new")
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.get_collateral_type_display()}"


class CollateralImage(models.Model):
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="collateral/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.loan_request}"
