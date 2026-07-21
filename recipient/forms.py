import os

from django import forms

from .models import Recipient, RecipientDocument


class RecipientProfileForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = [
            "full_name",
            "phone_number",
            "date_of_birth",
            "gender",
            "blood_group",
            "address",
            "city",
            "medical_condition",
            "hospital",
            "treating_physician",
            "emergency_contact",
            "profile_picture",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter full name"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "+1 (555) 123-4567"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-input", "type": "date"}
            ),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "blood_group": forms.Select(attrs={"class": "form-select"}),
            "address": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter street address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter city"}
            ),
            "medical_condition": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "e.g., Chronic Anemia"}
            ),
            "hospital": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "e.g., Mercy General Hospital"}
            ),
            "treating_physician": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Dr. Robert Miller"}
            ),
            "emergency_contact": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Name & Phone Number (+1 555-987-6543)",
                }
            ),
            "profile_picture": forms.FileInput(
                attrs={"class": "form-file-input", "accept": "image/*"}
            ),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if not full_name or not full_name.strip():
            raise forms.ValidationError("Full name is required.")
        return full_name.strip()

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone or not phone.strip():
            raise forms.ValidationError("Phone number is required.")
        return phone.strip()

    def clean_address(self):
        address = self.cleaned_data.get("address")
        if not address or not address.strip():
            raise forms.ValidationError("Address is required.")
        return address.strip()

    def clean_city(self):
        city = self.cleaned_data.get("city")
        if not city or not city.strip():
            raise forms.ValidationError("City is required.")
        return city.strip()


class RecipientDocumentForm(forms.ModelForm):
    class Meta:
        model = RecipientDocument
        fields = ["document_type", "file"]

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file:
            raise forms.ValidationError("Please select a file to upload.")
        return file
