from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control me-2", "placeholder": "Search"}
        ),
    )
