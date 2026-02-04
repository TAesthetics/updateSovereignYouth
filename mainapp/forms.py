from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import YouthOrganization, YouthMember

class YouthOrganizationForm(forms.ModelForm):
    class Meta:
        model = YouthOrganization
        fields = ['name', 'description', 'founded_date', 'location', 'website', 'logo', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_founded_date(self):
        founded_date = self.cleaned_data.get('founded_date')
        if founded_date and founded_date > timezone.now().date():
            raise ValidationError("Founded date cannot be in the future.")
        return founded_date


class YouthMemberForm(forms.ModelForm):
    class Meta:
        model = YouthMember
        fields = [
            'organization', 'date_of_birth', 'gender', 'phone_number', 
            'address', 'city', 'postal_code', 'country', 'school', 'grade',
            'parent_guardian_name', 'parent_guardian_phone', 'parent_guardian_email',
            'emergency_contact_name', 'emergency_contact_phone', 
            'emergency_contact_relation', 'skills', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'List any skills or interests relevant to the organization'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active organizations in the dropdown
        self.fields['organization'].queryset = YouthOrganization.objects.filter(is_active=True)
        
        # Make organization field required only for new members
        if not self.instance.pk:
            self.fields['organization'].required = True
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
        return date_of_birth
    
    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade is not None and (grade < 1 or grade > 13):
            raise ValidationError("Grade must be between 1 and 13.")
        return grade
