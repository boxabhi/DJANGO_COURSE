from django import forms
from home.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['student_bio', 'age']


