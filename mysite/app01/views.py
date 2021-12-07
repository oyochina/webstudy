from django.shortcuts import render,HttpResponse,redirect
from django.urls import resolvers
from django.urls.base import reverse
# Create your views here.

#def index(request):
    #return HttpResponse('index in app01')

def index(request):
    name=request.POST.get('name1')
    #if name=='aaa':
    #    print(name)
    #    return redirect('/app01/new/')
    #print(name)
    return render(request,'app01/templates/index.html')

def new(request,id):
    
    return HttpResponse('指向：'+reverse('app_01:thenew',args=(id,)))