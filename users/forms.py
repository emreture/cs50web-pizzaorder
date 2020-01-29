from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput)
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match!", code="confirm_error")
        values = {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        }
        return values
