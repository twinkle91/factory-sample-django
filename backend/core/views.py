from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    """Liveness check used by the Factory's health path and smoke checks."""
    return JsonResponse({"status": "ok"})
