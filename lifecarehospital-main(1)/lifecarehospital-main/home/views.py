from django.http import Http404
from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    
#def userportal(request):
    # Your view logic here
   # return render(request, 'home/userportal.html')  
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
    # You can add any context data you want to pass to the template
    context = {
        'aboutus': 'About Us',
        'page_title': 'aboutus',
    }
    
    return render(request, 'home/about.html', context)
@login_required 
def showmyappointments(request):
    myappointments = Bookappointment.objects.all().order_by('-bookingon')
    return render(request, 'home/myappointment.html', {'myappointments': myappointments}) 
    
def updateappointment(request, appointment_id):
    updateappointment = get_object_or_404(Bookappointment, pk=appointment_id)
    if request.method == 'POST':
        form = BookappointmentForm(request.POST, instance=updateappointment)
        if form.is_valid():
            form.save()
            return redirect('home:showmyappointments', appointment_id=bookappointment.id)
    else:
        form = BookappointmentForm(instance=updateappointment)
    return render(request, 'home/updateappointment.html', {'form': form, 'updateappointment': updateappointment})