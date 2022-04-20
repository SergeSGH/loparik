from django.shortcuts import render
from django.http import HttpResponse


def index(request):    
    return HttpResponse('Главная страница')

def prizy(request):
    return HttpResponse('Призы аттракциона')

def consult(request):
    return HttpResponse('Заполните форму для обратной связи')