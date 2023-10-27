from django import forms

from .models import Bookappointment


class DateInput(forms.DateInput):
      input_type='date'
    
class BookappointmentForm(forms.ModelForm):
     class Meta:
         model = Bookappointment
         exclude = ['bookingon']
         fields = '__all__'
         
         widgets={
             'bookingdate': DateInput(),
            
         } 
         


          