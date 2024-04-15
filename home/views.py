from django.http import Http404
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import render
from datetime import datetime
import boto3

from .models import Department
from .models import Doctors
from .models import Bookappointment
from .forms import BookappointmentForm


# Create your views here.


def index(request):
    # Get the last doctor's image URL
    last_doctor = Doctors.objects.last()
    doctor_image_url = last_doctor.docimage.url if last_doctor else None
    
    context = {
        'doctor_image_url': doctor_image_url,
        'user_authenticated': request.user.is_authenticated
    }
    return render(request, 'home/index.html', context)

    

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
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        activity_level = request.POST.get('activity_level')
        goal = request.POST.get('goal')

        # Payload
        payload = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'activity_level': activity_level,
            'goal': goal
        }

        # AWS Lambda endpoint
        api_url = "https://529k6hcwv3.execute-api.eu-west-1.amazonaws.com/dev"
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            data = response.json()
            calorie_intake = data.get('calorie_intake')
            
            # Example of normal rate chart
            normal_rate_chart = {
                'sedentary': {
                    'lose_weight': (1500, 1800),
                    'gain_weight': (2000, 2500)
                },
                'lightly_active': {
                    'lose_weight': (1700, 2000),
                    'gain_weight': (2200, 2700)
                },
                'moderately_active': {
                    'lose_weight': (2000, 2300),
                    'gain_weight': (2500, 3000)
                },
                'very_active': {
                    'lose_weight': (2200, 2500),
                    'gain_weight': (2700, 3200)
                }
            }

            normal_rate = normal_rate_chart.get(activity_level, {}).get(goal)
            return render(request, 'home/calorie_calculator.html', {'calorie_intake': calorie_intake, 'normal_rate': normal_rate})
        else:
            error_message = "Failed to calculate calorie intake."
            return render(request, 'home/calorie_calculator.html', {'error_message': error_message})
    else:
        return render(request, 'home/calorie_calculator.html')

        
        
def bmi_calculator(request):
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height')) / 100  # Convert height to meters
        # Send data to the API Gateway endpoint
        api_gateway_endpoint = "https://d56f0ty1zb.execute-api.us-east-2.amazonaws.com/dev"  
        payload = {
            'weight': weight,
            'height': height,
            'weight_unit': 'kg',
            'height_unit': 'm',
        }
         
        try:
            response = requests.post(api_gateway_endpoint, json=payload)
            response_data = response.json()
            print("response_data = ", response_data)
            bmi = response_data.get('bmi')
            category = response_data.get('category')
            print("bmi = ", bmi)
            print("category = ", category)
        except Exception as e:
            # Handle API request error
            messages.error(request, f"Error fetching BMI: {str(e)}")
            bmi = None
            category = None
        return render(request, 'home/bmi.html', {'bmi': bmi, 'bmi_category': category})
    else:
        return render(request, 'home/bmi.html')

def calorieintakeguidelines(request):
    # View logic goes here
    return render(request, 'home/calorieintakeguidelines.html')


def submitfeedback(request):
    if request.method == 'POST':
        username = request.user.username
        feedback = request.POST.get('feedback')
        # Get current time
        time = datetime.now().isoformat()
        
        # Validation
        if not (username and feedback):
            return HttpResponse("Username and feedback are required fields.")
        
        payload = {
            'username': username,
            'feedback': feedback,
            'time': time
        }
        
        api_endpoint = 'https://1qtshriut7.execute-api.eu-west-1.amazonaws.com/dev/'
        
        response = requests.post(api_endpoint, json=payload)
        
        if response.status_code == 200:
            # Redirect to a confirmation page
            return redirect('home:index')
        else:
            return HttpResponse("Failed to submit feedback. Please try again later.")
    
    return render(request, 'home/submitfeedback.html')

def viewfeedback(request):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('x23108568_lifecarehospitalfeedback')  # Replace with your DynamoDB table name

    # Get all feedback items from DynamoDB table
    response = table.scan()
    feedback_items = response.get('Items', [])

    # Pass feedback items to the template
    context = {
        'feedback_items': feedback_items
    }

    return render(request, 'home/viewfeedback.html', context)
    

def showhospitalmap(request):
    # Fetch hospital locations from your Google Maps API endpoint
    api_endpoint = "https://20pceoqvmc.execute-api.eu-west-1.amazonaws.com/dev1"
    response = requests.get(api_endpoint)
    locations = response.json()

    # Pass the hospital locations to the template
    context = {'locations': locations}
    return render(request, 'home/hospitalmap.html', context)