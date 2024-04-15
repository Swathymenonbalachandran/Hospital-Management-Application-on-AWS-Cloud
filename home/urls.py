from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('department/', views.department, name='department'),
    path('doctors/', views.doctors, name='doctors'),
    path('bookappointment/', views.bookappointment, name='bookappointment'),
    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contactus'),
    path('showappointments/', views.showappointments, name='showappointments'),
    path('updateappointment/<int:bookappointment_id>/', views.updateappointment, name='updateappointment'),
    path('deleteappointment/<int:bookappointment_id>/', views.deleteappointment, name='deleteappointment'),
    path('bmi_calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('calorie_calculator/', views.calorie_calculator, name='calorie_calculator'),
    path('calorieintakeguidelines/', views.calorieintakeguidelines, name='calorieintakeguidelines'),
    path('feedback/', views.submitfeedback, name='submitfeedback'),
    path('viewfeedback/', views.viewfeedback, name='viewfeedback'),
    path('hospitalmap/', views.showhospitalmap, name='hospitalmap'),
   # path('userportal/', views.userportal, name='userportal'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)