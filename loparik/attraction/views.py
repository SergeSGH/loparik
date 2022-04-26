from django.shortcuts import render
from django.http import HttpResponse

def index(request):    
    template = 'attraction/index3.html'
    return render(request, template)

def prizy(request):
    return HttpResponse('Призы аттракциона')

def consult(request):
    return HttpResponse('Заполните форму для обратной связи')
