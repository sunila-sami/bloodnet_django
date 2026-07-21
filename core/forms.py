from django import forms
from .models import BloodRequest


class BloodRequestForm(forms.ModelForm):
    CITY_CHOICES = [
        ("", "Select City"),
        ("Karachi", "Karachi"),
        ("Lahore", "Lahore"),
        ("Islamabad", "Islamabad"),
        ("Rawalpindi", "Rawalpindi"),
        ("Peshawar", "Peshawar"),
        ("Faisalabad", "Faisalabad"),
        ("Multan", "Multan"),
        ("Quetta", "Quetta"),
    ]

    AREA_CHOICES = [
        ("", "Select Area"),
        # Karachi areas
        ("Clifton", "Clifton"),
        ("DHA", "DHA"),
        ("Gulshan-e-Iqbal", "Gulshan-e-Iqbal"),
        ("North Nazimabad", "North Nazimabad"),
        ("Saddar", "Saddar"),
        # Lahore areas
        ("Gulberg", "Gulberg"),
        ("Johar Town", "Johar Town"),
        ("DHA Phase 5", "DHA Phase 5"),
        ("Model Town", "Model Town"),
        # Islamabad areas
        ("Blue Area", "Blue Area"),
        ("F-6", "F-6"),
        ("F-7", "F-7"),
        ("G-9", "G-9"),
        ("I-8", "I-8"),
        # Rawalpindi areas
        ("Saddar Rawalpindi", "Saddar (Rawalpindi)"),
        ("Bahria Town", "Bahria Town"),
        # Peshawar areas
        ("Hayatabad", "Hayatabad"),
        ("Peshawar Cantt", "Peshawar Cantt"),
    ]

    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_city"})
    )

    area = forms.ChoiceField(
        choices=AREA_CHOICES,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_area"}),
        required=False
    )

    class Meta:
        model = BloodRequest
        fields = [
            "blood_component",
            "units_required",
            "required_date",
            "urgency_level",
            "hospital_or_blood_bank",
            "city",
            "area",
            "additional_details",
            "medical_document",
        ]
        widgets = {
            "blood_component": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_blood_component"
                }
            ),
            "units_required": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "value": 1,
                    "id": "id_units_required"
                }
            ),
            "required_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "id": "id_required_date"
                }
            ),
            "urgency_level": forms.RadioSelect(
                attrs={
                    "class": "urgency-options",
                    "id": "id_urgency_level"
                }
            ),
            "hospital_or_blood_bank": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. City General Hospital, Trauma Center",
                    "id": "id_hospital_or_blood_bank"
                }
            ),
            "additional_details": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter any specific requirements or instructions here...",
                    "id": "id_additional_details"
                }
            ),
            "medical_document": forms.ClearableFileInput(
                attrs={
                    "class": "file-input",
                    "id": "id_medical_document",
                    "style": "display: none;"  # Hidden because we'll trigger it from custom file upload UI
                }
            ),
        }