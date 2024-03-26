from django.http import Http404
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render

from .models import Department
from .models import Doctors
from .models import Bookappointment
from .forms import BookappointmentForm

# Create your views here.

def index(request):
    user_authenticated = request.user.is_authenticated
    return render(request, 'home/index.html', {'user_authenticated': user_authenticated})
    

def department(request):
    context = {
        'dept': Department.objects.all()
    }
    return render(request,'home/department.html', context)
    
    
    
def doctors(request):
    context = {
        'doc': Doctors.objects.all()
    }
    return render(request,'home/doctors.html', context)
    
 
@login_required
def bookappointment(request):
    if request.method == 'POST':
        form = BookappointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:showappointments')
    else:
        form = BookappointmentForm()

    return render(request, 'home/bookappointment.html', {'form': form})
    
def aboutus(request):
   
    context = {
        'aboutus': 'About Us',
        'page_title': 'aboutus',
    }
    
    return render(request, 'home/about.html', context)
    
def contactus(request):
   
    context = {
        'contactus': 'Contact Us',
        'page_title': 'contactus',
    }
    return render(request, 'home/contactus.html', context)   
    
@login_required 
def showappointments(request):
    myappointments = Bookappointment.objects.all().order_by('-bookingon')
    return render(request, 'home/myappointment.html', {'myappointments': myappointments}) 
    
@login_required
def updateappointment(request, bookappointment_id):
    updateappointment = get_object_or_404(Bookappointment, pk=bookappointment_id)
    
    if request.method == 'POST':
        form = BookappointmentForm(request.POST, instance=updateappointment)
        if form.is_valid():
            form.save()
            return redirect('home:showappointments')  
    else:
        form = BookappointmentForm(instance=updateappointment)
    
    return render(request, 'home/updateappointment.html', {'form': form, 'updateappointment': updateappointment})
    
def deleteappointment(request, bookappointment_id):
    deleteappointment = get_object_or_404(Bookappointment, pk=bookappointment_id)

    if request.method == 'POST':
        deleteappointment.delete()
        return redirect('home:showappointments')   

    return render(request, 'home/deleteappointment.html', {'deleteappointment': deleteappointment})

def calorie_calculator(request):
    if request.method == 'POST':
        # Get form data
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        activity_level = request.POST.get('activity_level')
        goal = request.POST.get('goal')

        # Prepare payload for the API request
        payload = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'activity_level': activity_level,
            'goal': goal
        }

        # Make a POST request to the AWS Lambda endpoint
        api_url = "https://529k6hcwv3.execute-api.eu-west-1.amazonaws.com/dev"
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            data = response.json()
            calorie_intake = data.get('calorie_intake')
            return render(request, 'home/calorie_calculator.html', {'calorie_intake': calorie_intake})
        else:
            error_message = "Failed to calculate calorie intake."
            return render(request, 'home/calorie_calculator.html', {'error_message': error_message})
    else:
        return render(request, 'home/calorie_calculator.html')
def bmi_calculator(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height')) / 100  # Convert height to meters
        bmi = weight / (height * height)
        return render(request, 'home/bmi.html', {'bmi': bmi})
    else:
        return render(request, 'home/bmi.html')
