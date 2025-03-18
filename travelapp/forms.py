# from django import forms
# from .models import Test

class testform(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name','email','location','review'] 

# from django import forms
# from .models import TourPreference

# class TourPreferenceForm(forms.ModelForm):
#     class Meta:
#         model = TourPreference
#         fields = '__all__'


# forms.py
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
