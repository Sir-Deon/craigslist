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

    post_listings = soup.find_all('li', {'class':'result-row'})

   
    final_post = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text


    print(post_title)
    print(post_url)
    print(post_price)

    suff_for_front_end = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', suff_for_front_end)