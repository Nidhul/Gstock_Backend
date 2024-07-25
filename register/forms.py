# register/forms.py

from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    admin = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ['id','username', 'password', 'admin']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.is_staff = self.cleaned_data['admin']
            user.save()
        return user
