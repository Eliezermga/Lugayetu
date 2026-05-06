from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Language, LegalPage
from django.utils.translation import gettext_lazy as _

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={'placeholder': '••••••', 'class': 'form-input'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        label=_("Confirmer le mot de passe"),
        widget=forms.PasswordInput(attrs={'placeholder': '••••••', 'class': 'form-input'})
    )
    accept_terms = forms.BooleanField(
        required=True,
        label=_("J'accepte les conditions d'utilisation et la politique de confidentialité")
    )

    class Meta:
        model = User
        fields = [
            'last_name', 'first_name', 'email', 'age', 'sexe', 
            'mother_tongue', 'province', 'city_village'
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder': _('Ex: Mununga'), 'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'placeholder': _('Ex: Eliezer'), 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': _('votre@email.com'), 'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'min': 13, 'max': 120, 'class': 'form-input', 'placeholder': '18'}),
            'sexe': forms.Select(attrs={'class': 'form-input'}),
            'mother_tongue': forms.Select(attrs={'class': 'form-input'}),
            'province': forms.Select(attrs={'class': 'form-input'}),
            'city_village': forms.TextInput(attrs={'placeholder': _('Ex: Kolwezi'), 'class': 'form-input'}),
        }
        labels = {
            'last_name': _("Nom"),
            'first_name': _("Prénom"),
            'email': _("Adresse email"),
            'age': _("Âge"),
            'sexe': _("Sexe"),
            'mother_tongue': _("Langue maternelle"),
            'province': _("Province"),
            'city_village': _("Ville / Village"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make choice fields required
        if 'sexe' in self.fields:
            self.fields['sexe'].required = True
            choices = list(self.fields['sexe'].choices)
            if choices and (choices[0][0] is None or choices[0][0] == ''):
                choices[0] = ('', _('Select'))
            else:
                choices.insert(0, ('', _('Select')))
            self.fields['sexe'].choices = choices

        if 'province' in self.fields:
            self.fields['province'].required = True
            choices = list(self.fields['province'].choices)
            if choices and (choices[0][0] is None or choices[0][0] == ''):
                choices[0] = ('', _('Select'))
            else:
                choices.insert(0, ('', _('Select')))
            self.fields['province'].choices = choices
            self.fields['province'].initial = 'lualaba'
        
        if 'mother_tongue' in self.fields:
            self.fields['mother_tongue'].required = True
            self.fields['mother_tongue'].empty_label = _('Select')
            # Try to set Ruund as default
            try:
                ruund = Language.objects.filter(models.Q(code__iexact='ruund') | models.Q(name__iexact='ruund')).first()
                if ruund:
                    self.fields['mother_tongue'].initial = ruund
            except:
                pass

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _("Les mots de passe ne correspondent pas."))
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Set username to email since we use email login
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'placeholder': 'votre@email.com', 'class': 'form-input'}))
    password = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput(attrs={'placeholder': '••••••', 'class': 'form-input'}))
