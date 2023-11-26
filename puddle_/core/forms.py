from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Obligatorio. Ingresa una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')  # Remueve 'username' y usa 'email'

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']
