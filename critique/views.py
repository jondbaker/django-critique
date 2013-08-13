from django.http import Http404, HttpResponse

from .forms import CritiqueForm


def create(request):
    """Validates input and then creates a Critique record."""
    if request.method != "POST" and not request.is_ajax():
        raise Http404()

    form = CritiqueForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.url = request.META["HTTP_REFERER"]
        obj.user_agent = request.META["HTTP_USER_AGENT"]
        obj.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("ERROR")
