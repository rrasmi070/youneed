from django import forms
from .models import *
from crispy_forms.helper import FormHelper

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["order_by","mobile","email","pin_code","shiping_address","payment_method"]

        widgets = {
            'order_by': forms.TextInput(attrs = {'class':'form-contol','placeholder': '1234 Main St'}),
            'mobile': forms.TextInput(attrs = {'class':'form-contol','placeholder': 'Phone No.'}),
            'email': forms.EmailInput(attrs = {'class':'form-contol','placeholder': 'example@xyz.com'}),
            'pin_code': forms.TextInput(attrs = {'class':'form-contol','placeholder': 'zip code.......'}),
            'shiping_address': forms.Textarea(attrs = {'class':'form-contol','placeholder': 'Ente delivery address.......'}),            
        }

# Seller Form----------------------------------
class SellerForm(forms.ModelForm):
    more_images = forms.FileField(required=False,widget=forms.FileInput(attrs={
        "class" : "form-control",
        "multiple" : True
    }))
    class Meta:
        model = Product
        fields = ["Product_name","category","Price","brand","Description","image"]
        widgets = {
            "Product_name" : forms.TextInput(
                attrs={
                    "class" : "form-control",
                    "placeholder": "Enter The products name here......"
                }),
            "category" : forms.Select(
                attrs = {
                    "class" : "form-control",
                    # "placeholder": "Enter The products name here......"
            }),
            "Price" : forms.TextInput(
                attrs={
                    "class" : "form-control",
                    "placeholder": "Enter The products name here......"
                }),
            "brand" : forms.TextInput(
                attrs={
                    "class" : "form-control",
                    "placeholder": "Enter The products name here......"
                }),
            "Description" : forms.Textarea(
                attrs={
                    "class" : "form-control",
                    "placeholder": "Enter The products name here......"
                }),
            "image" : forms.FileInput(
                attrs={
                    "class" : "form-control",
                    "placeholder": "Enter The products name here......"
                }),
        }