from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LoanRequestForm
from .models import CollateralImage, Service, Testimonial

SUCCESS_MSG = "Thank you! Your loan request has been received. We'll contact you on WhatsApp shortly."


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = LoanRequestForm(request.POST, request.FILES)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if form.is_valid():
            with transaction.atomic():
                loan_request = form.save()
                for img in form.cleaned_data["images"]:
                    CollateralImage.objects.create(loan_request=loan_request, image=img)
            if is_ajax:
                return JsonResponse({"ok": True, "message": SUCCESS_MSG})
            messages.success(request, SUCCESS_MSG)
            return redirect("/#request")
        if is_ajax:
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    else:
        form = LoanRequestForm()

    context = {
        "form": form,
        "services": Service.objects.filter(is_active=True),
        "testimonials": Testimonial.objects.filter(is_active=True),
    }
    return render(request, "core/index.html", context)
