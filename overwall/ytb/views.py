from django.http.response import HttpResponse
from django.shortcuts import render
import requests
# Create your views here.

  


def index(request):
    headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    url='https://www.baidu.com'
    r=requests.get(url=url,headers=headers)
    return HttpResponse(r.text)

