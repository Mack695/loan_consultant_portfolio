from django.conf import settings


def site_info(request):
    return {"SITE": settings.SITE_INFO}
