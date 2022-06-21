from django.http import HttpResponse

# Create your views here.

def url_shortener(request, slug):
    return HttpResponse(f'Hello {slug}')