
from csv import field_size_limit
from datetime import date
#to display the content when u click on notes 
from django import forms
from httpcore import request
from . models import *
from django.contrib.auth.forms import UserCreationForm #inbuilt form for registration

class NotesForm(forms.ModelForm):  #This from inherit ModelForms
    class Meta:
        model = Notes #here model conatins 3 column of Notes ie title ,des,user7u
        fields = ['title','description'] #field is nothing but what to display on page
        # and in view files import this form page by writing -> from . forms import Notes
""""
class DateInput(forms.DateInput):
    input_type: 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':forms.DateInput()}
        fields = ['subject','title','description','due','is_finished']
        """

class DashboardForm(forms.Form):
    
    text = forms.CharField(max_length=100,label="ENTER YOUR SEARCH : ")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]     #CHOICES for choice act as radio button has 2 options 
    measurement= forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):   #form for length when radiobitton is Length
    CHOICES = [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    ) 


class ConversionMassForm(forms.Form):   #form for mass when radiobotton is Mass
    CHOICES = [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )

class UserRegistrationForm(UserCreationForm):  #here UserRegistrationForm inherit from serCreationForm
    class Meta:
        model = User
        fields = ['username','password1','password2']
        