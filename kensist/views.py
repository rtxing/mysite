from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from kensist.models import *
import json
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from rest_framework import viewsets, status
# Create your views here.



def home(request):
  template = loader.get_template('kenhome.html')
  return HttpResponse(template.render())



def get_project(request, project):
  p = Project.objects.filter(name= project)[0]
  print(p)
  data = {'project': json.dumps(model_to_dict(p)), 'status':status.HTTP_200_OK }
  return JsonResponse(data)



def xing(request):
  template = loader.get_template('xing.html')
  return HttpResponse(template.render())