from django import forms
from django.conf import settings


class PublishDataForm(forms.Form):
    """
    This is a Django form to control and validate user input fields.

    https://docs.djangoproject.com/en/4.2/topics/forms/

    Typically this would go into its own forms.py class, but it's added here for simplicity.
    """

    title = forms.CharField(
        initial="My New Publication Title",
        max_length=256,
        help_text="A title to use for this search entry",
    )
    label = forms.CharField(
        initial="An example run started via DGPF",
        max_length=256,
        help_text="A nice label to add context to this flow",
    )
    tags = forms.CharField(
        label="Tags",
        max_length=256,
        help_text="Tags help categorize many runs over time. You can use a comma separated list here.",
    )
