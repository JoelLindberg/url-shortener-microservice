from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from django.core.validators import URLValidator

import json

from .models import ShortUrl


# Create your views here.

def developer(request, slug):
    """Development API. Used for managing sqlite db. Written in a more temporary fashion as I would have preferred using a db tool instead (the project was written on replit.com where the dbshell tool doesn't work out of the box).
    :Show all urls: /api/developer
    :Delete url with ID: /api/developer/delete?id=1
    :Get specific url with ID: /api/developer/get?id=1"""
    if slug == 'all':
        d = serializers.serialize('json', ShortUrl.objects.all())
    elif slug == 'delete':
        id = request.GET
        id = id.get('id', default=None)
        try:
            id = int(id)
        except:
            id = None
            d = json.dumps({"error": "A number is required"})
        if id != None:
            ShortUrl.objects.filter(pk=id).delete()
            d = json.dumps({"deleted_url_with_id": id})
    elif slug == 'get':
        id = request.GET
        id = id.get('id', default=None)
        try:
            id = int(id)
        except:
            id = None
            d = json.dumps({"error": "A number is required"})
        if id != None:
            d = ShortUrl.objects.filter(pk=id)
            d = serializers.serialize('json', d)
            json.dumps(d)
    
    return HttpResponse(d, content_type='application/json')


def url_shortener(request):
    # Check incoming POST data
    if request.method == 'POST':
        post_data = request.POST
        post_data = post_data.get('url', default=None)
        if post_data == None:
            return HttpResponse(json.dumps({ "error": "No data received"}), content_type='application/json')
        
        # Validate the URL
        validator_http_only = URLValidator(schemes=['http', 'https'])
        try:
            validator_http_only(post_data)
        except:
            return HttpResponse(json.dumps({ "error": "invalid url"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({ "error": "Only POST is accepted"}), content_type='application/json')

    # Save the object to the DB
    url = ShortUrl(original_url=post_data)
    url.save()
    print(type(url))
    print(url.pk)
    #print(f'url after save: {url.objects.all()}')
    #ShortUrl.objects.select_related('short').select_for_update()

    # Fetch the object from the DB
    #d = serializers.serialize('json', ShortUrl.objects.all())
    #d = json.loads(d)
    #print(d)

    # create return object
    d = {
        "original_url": post_data,
        "short_url": url.pk
    }

    return HttpResponse(json.dumps(d), content_type='application/json')


def short_url_redirect(request, id):
    """Redirect to the original url for a given short url ID"""
    if request.method == 'GET':
        url = ShortUrl.objects.filter(pk=id)
        url = url[0].original_url
    
    return HttpResponseRedirect(url)