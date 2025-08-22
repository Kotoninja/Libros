from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "placeholder": "username"}
        ),
        required=False,
    )
