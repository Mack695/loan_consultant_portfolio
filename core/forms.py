import re

from django import forms

from .models import COLLATERAL_CHOICES, LoanRequest

MAX_IMAGES = 5
MAX_IMAGE_MB = 5


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    """Optional multi-image upload; cleans to a list of validated images."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"accept": "image/*", "multiple": True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        data = [f for f in data if f]
        if len(data) > MAX_IMAGES:
            raise forms.ValidationError(f"You can upload up to {MAX_IMAGES} photos.")
        clean_one = super().clean
        files = []
        for f in data:
            if f.size > MAX_IMAGE_MB * 1024 * 1024:
                raise forms.ValidationError(f"'{f.name}' is larger than {MAX_IMAGE_MB}MB.")
            files.append(clean_one(f, initial))
        return files


class LoanRequestForm(forms.ModelForm):
    images = MultipleImageField(
        required=False,
        label="Photos of Your Collateral",
        help_text=f"Optional. Up to {MAX_IMAGES} photos, {MAX_IMAGE_MB}MB each. Clear photos speed up valuation.",
    )

    field_order = [
        "full_name", "email", "whatsapp_number", "loan_amount",
        "collateral_type", "collateral_description", "images",
    ]

    class Meta:
        model = LoanRequest
        fields = ["full_name", "email", "whatsapp_number", "loan_amount", "collateral_type", "collateral_description"]
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "whatsapp_number": "WhatsApp Number",
            "loan_amount": "Loan Amount Needed",
            "collateral_type": "Type of Collateral",
            "collateral_description": "Describe Your Collateral",
        }
        help_texts = {"whatsapp_number": "Include your country code, e.g. +44 7700 900123"}
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "whatsapp_number": forms.TextInput(attrs={"placeholder": "+00 000 000 0000", "autocomplete": "tel", "inputmode": "tel"}),
            "loan_amount": forms.NumberInput(attrs={"placeholder": "5000", "min": "1", "step": "any"}),
            "collateral_description": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Make, model, year, condition, weight, size... (optional)"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["collateral_type"].choices = [("", "Select collateral type")] + COLLATERAL_CHOICES

    def clean_whatsapp_number(self):
        raw = self.cleaned_data["whatsapp_number"].strip()
        digits = re.sub(r"\D", "", raw)
        if raw.startswith("00"):
            digits = digits[2:]
        elif not raw.startswith("+"):
            raise forms.ValidationError("Start with your country code, e.g. +44 7700 900123.")
        if not 8 <= len(digits) <= 15:
            raise forms.ValidationError("Enter a valid WhatsApp number.")
        return "+" + digits

    def clean_loan_amount(self):
        amount = self.cleaned_data["loan_amount"]
        if amount <= 0:
            raise forms.ValidationError("Enter an amount greater than zero.")
        return amount
