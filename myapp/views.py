import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_URL = 'https://accra.craigslist.org/search/?query={}'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    post_titles = soup.find_all('a', {'class': 'result-title'})
    print(post_titles[0])

    suff_for_front_end = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', suff_for_front_end)