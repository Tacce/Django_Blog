from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_image')

    def save(self, commit=True):
        user = super().save(commit=False)
        # if self.cleaned_data['remove_profile_image']:
        #    user.remove_profile_image()
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields['password'].widget = forms.HiddenInput()
            self.fields['password'].label = ''
            self.fields['password'].help_text = ''
