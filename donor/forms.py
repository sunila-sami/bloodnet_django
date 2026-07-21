from django import forms

from .models import Donor


class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            "full_name",
            "phone_number",
            "date_of_birth",
            "gender",
            "blood_group",
            "address",
            "city",
            "is_available",
            "last_donation_date",
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
            "is_available": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),
            "last_donation_date": forms.DateInput(
                attrs={"class": "form-input", "type": "date"}
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
