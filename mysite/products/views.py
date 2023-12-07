from django.shortcuts import render
from products.models import Items
# Create your views here.
from django.db.models import Sum
# Create your views here.
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages




def interview(request):
    context = {}
    return render(request, "interview.html", context)
    #return render(request, "index.html", context)



def summary(request):
    context = {}
    query_results = Items.objects.all()
    return render(request, "summary.html", {'query_results':query_results})
    #return render(request, "index.html", context)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})


def back(request):
    context = {}
    sum = Items.objects.aggregate(Sum('price'))
    return render(request, "back.html", {'sum' : sum})
    #return render(request, "index.html", context)


