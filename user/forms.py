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
            attrs={"class": "form-check-input", "placeholder": "Remember me"}
        ),
        required=False,
        disabled=True,
    )


class RegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Repeat password"}
        )
    )


class ResetPasswordEmail(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
    )


class ResetPassword(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        )
    )


class SettingsProfile(forms.Form):
    user_image = forms.ImageField(
        widget=forms.FileInput(
            attrs={"class": "form-control", "type": "file", "id": "image-input"}
        ),
        required=False,
    )
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nickname"}
        ),
        required=False,
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First name"}
        ),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Second name"}
        ),
        required=False,
    )
    location = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Location"}
        ),
        required=False,
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
        required=False,
        disabled=True,
    )
    phone_number = forms.CharField(
        widget=forms.TelInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone number (+1 123-456-7890)",
            }
        ),
        required=False,
    )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "Birthday", "type": "date"}
        ),
        required=False,
    )


class ChangePassword(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter current password"}
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        )
    )
