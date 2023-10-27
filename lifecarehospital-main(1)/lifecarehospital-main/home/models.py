from django.db import models


# Create your models here.
class Department(models.Model):
# each class variable represents a database i.e. table field in the model
    depname = models.CharField(max_length=200)
    depdescription = models.TextField()
    
    def __str__(self):
        return self.depname  
        
        
class Doctors(models.Model):
# each class variable represents a database i.e. table field in the model
    docname = models.CharField(max_length=200)
    depname = models.ForeignKey(Department,on_delete=models.CASCADE)
    qualification = models.CharField(max_length=200)
    docimage= models.ImageField(upload_to='docimage/', blank=True, null=True)
    
    def __str__(self):
        return self.docname
        
class Bookappointment(models.Model):
# each class variable represents a database i.e. table field in the model
    pname = models.CharField(max_length=200)
    paddress = models.CharField(max_length=600) 
    pphone = models.CharField(max_length=10)
    pemail = models.EmailField()
    depname = models.ForeignKey(Department,on_delete=models.CASCADE)
    docname =models.ForeignKey(Doctors,on_delete=models.CASCADE)
    bookingdate = models.DateField()
    bookingon = models.DateField(auto_now=True)
    
    
    
    