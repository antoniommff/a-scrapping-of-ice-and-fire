from django import forms

from .models import CustomUser


class LoginForm(forms.Form):
    email_username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'example@mail.com',
                'class': 'form-control'
            }
        ),
        label="Email o nombre de usuario"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '1234',
                                          'type': 'password',
                                          'class': 'form-control'}),
        label="Contraseña"
    )


class RegisterForm(forms.Form):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            print(CustomUser.objects.filter(email=email).exists())
            raise forms.ValidationError(
                "Este correo electrónico ya está en uso."
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Este nombre de usuario ya está en uso."
            )
        return username

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre',
                'class': 'form-control'
            }
        ),
        label="Nombre"
    )
    surname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Apellidos',
                'class': 'form-control'
            }
        ),
        label="Apellidos"
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo electrónico',
                'class': 'form-control'
            }
        ),
        label="Correo electrónico"
    )
    username = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }
        ),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                          'type': 'password',
                                          'class': 'form-control'}),
        label="Fecha de nacimiento"
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña',
                                          'type': 'password',
                                          'class': 'form-control'}),
        label="Confirmar contraseña"
    )

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirmation


class UpdateProfileForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Nueva contraseña"
    )
    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar nueva contraseña"
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'email', 'username']
        labels = {
            'name': 'Nombre',
            'surname': 'Apellidos',
            'email': 'Correo electrónico',
            'username': 'Nombre de usuario',
        }

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirmation

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
