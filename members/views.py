from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def home(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())


def milk(request):
  template = loader.get_template('milk.html')
  return HttpResponse(template.render())


def milk2(request):
  template = loader.get_template('milk2.html')
  return HttpResponse(template.render())


def hubio(request):
  template = loader.get_template('hubio.html')
  return HttpResponse(template.render())



def nearones(request):
  template = loader.get_template('Vlava/index.html')
  return HttpResponse(template.render())



def nearones2(request):
  template = loader.get_template('Vlava/nearonesi.html')
  return HttpResponse(template.render())



def nearhome(request):
  template = loader.get_template('nearhome.html')
  return HttpResponse(template.render())
