from django import forms

class CreateAccountForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=16)
    ship_address = forms.CharField(max_length=100)
    ship_city = forms.CharField(max_length=100)
    ship_postal_code = forms.CharField(max_length=16)
    ship_country = forms.CharField(max_length=100)
    buyer_rating = forms.FloatField(widget=forms.HiddenInput, initial=100.0)
    seller_rating = forms.FloatField(widget=forms.HiddenInput, initial=100.0)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)