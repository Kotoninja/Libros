from typing import Any
from django import forms
from .models import *


class CreateBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateBookForm, self).__init__(*args, **kwargs)
        self.fields["tags"].required = False

    class Meta:
        model = Book
        fields = ["image", "title", "description", "tags", "price"]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control", "id": "image-input"},

            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "tags": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Tags"}
            ),
            "price": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Price"}
            ),
        }


class AdditionalSearchFilter(forms.Form):
    is_rating_upper = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input my-auto ms-2",
                "style": "cursor: pointer",
                "role": "switch",
                "id": "switchCheckDefault",
                "name": "search",
            }
        ),
        required=False,
    )
    price_from = forms.IntegerField(
        widget=forms.TextInput(attrs={"class": "form-control"}),required=False
    )
    price_to = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control"}),required=False)

