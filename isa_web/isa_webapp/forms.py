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

class CreateListingForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=200)
    price = forms.FloatField(min_value=0.01)
    stock = forms.IntegerField(min_value=1, max_value=99, initial=1)
    sold = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)

    def __init__(self, categories, conditions, auth, *args, **kwargs):
        super(CreateListingForm, self).__init__(*args, **kwargs)
        self.fields["category"] = forms.ChoiceField(categories)
        self.fields["condition"] = forms.ChoiceField(conditions)
        self.fields["seller"] = forms.CharField(widget=forms.HiddenInput, initial=auth)


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100)