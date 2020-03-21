import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_URL = 'https://accra.craigslist.org/search/?query={}'
BASE_URL_IMAGE ='https://images.craigslist.org/{}_300x300.jpg'
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

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_URL_IMAGE.format(post_image_id)

        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_post.append((post_title, post_url, post_price, post_image_url))

    suff_for_front_end = {
        'search': search,
        'final_posts': final_post,
    }
    return render(request, 'my_app/new_search.html', suff_for_front_end)