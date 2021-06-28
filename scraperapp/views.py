from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import *
from django.http import HttpResponseRedirect
import ssl
from urllib.request import urlopen
from django.db import connection, transaction

# Create your views here.
def scrape(request):
    if request.method == "POST":
        context = ssl._create_unverified_context()
        site = request.POST.get('site', '')

        res = urlopen(site,
                      context=context)
        # page = requests.get(res)
        soup = BeautifulSoup(res, 'html.parser') # page.text

        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            Link.objects.create(address=link_address, name=link_text)
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()

    return render(request, 'myapp/result.html',{'data':data})

def clear(request):
    Link.objects.all().delete()
    cursor = connection.cursor()
    # cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='scraperapp_link';")
    return render(request,'myapp/result.html')
