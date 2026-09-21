from django.contrib import admin
from django.utils.html import format_html

from .models import CollateralImage, LoanRequest, Service, Testimonial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "rate_from", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "client_role", "rating", "is_active", "created_at")
    list_editable = ("is_active",)


class CollateralImageInline(admin.TabularInline):
    model = CollateralImage
    extra = 0
    readonly_fields = ("preview",)
    fields = ("preview", "image")

    @admin.display(description="Preview")
    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="height:110px;border-radius:6px"></a>', obj.image.url
            )
        return "-"


@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "collateral_type", "loan_amount", "whatsapp_link", "email", "photos", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "collateral_type")
    search_fields = ("full_name", "email", "whatsapp_number")
    readonly_fields = ("created_at",)
    inlines = [CollateralImageInline]

    @admin.display(description="WhatsApp")
    def whatsapp_link(self, obj):
        digits = "".join(ch for ch in obj.whatsapp_number if ch.isdigit())
        return format_html('<a href="https://wa.me/{}" target="_blank">{}</a>', digits, obj.whatsapp_number)

    @admin.display(description="Photos")
    def photos(self, obj):
        return obj.images.count()
