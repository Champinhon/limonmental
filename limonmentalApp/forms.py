# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment, Psychologist

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User  # Asegúrate de importar User desde django.contrib.auth.models
        fields = ['username', 'password']


class PsychologistForm(forms.ModelForm):
    precio = forms.CharField(max_length=20)  # Cambiar el campo precio a CharField
    correo = forms.CharField(max_length=100, label='Instagram')  # Cambiar el campo correo a CharField y cambiar el label a 'Instagram'

    class Meta:
        model = Psychologist
        fields = ['name', 'description', 'tipo_consulta', 'especialidad', 'precio', 'correo', 'numero', 'photo']