from django import forms
from .models import UserInfo, MCQ, Descriptive

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'phone_number']

class MCQForm(forms.ModelForm):
    class Meta:
        model = MCQ
        fields = ['question', 'optionA', 'optionB', 'optionC', 'optionD', 'correct_answer']

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Descriptive
        fields = ['question', 'answer']
