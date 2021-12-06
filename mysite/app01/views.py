from django.shortcuts import render,HttpResponse,redirect

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

def new(request):
    return HttpResponse('thr new html')