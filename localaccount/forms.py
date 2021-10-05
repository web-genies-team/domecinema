# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from domeproject.models import ProjectSponsor
from localcore.queries_utils import ModelsQueries as CoreQueries


User = get_user_model()
WORLD_COUNTRY_CHOICES = [] #CoreQueries.get_countries_for_choices()


class ChoiceFieldCustomValidation(forms.ChoiceField):
    def validate(self, value):
        pass

    def run_validators(self, value):
        pass

    def clean(self, value):
        return value


class SponsorProfileForm(forms.Form):
    street = forms.CharField(label=_("Street"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Enter the business street and number"))
    city = ChoiceFieldCustomValidation(label=_("City"),
                    widget=forms.Select(attrs={"id": "city_choice",
                                        "data-toggle": "tooltip",
                                        "title": "Sélectionez la Ville"
                                        " pour généner la list des Communes"}),
                    choices=(("", "Choisissez la ville"),),
                    required = False,
                    help_text=_("Entrez le nom de la ville"))
    commune = ChoiceFieldCustomValidation(label=_("Commune"),
                    widget=forms.Select(attrs={"id": "commune_choice"}),
                    choices=(("", "Choisissez la commune"),),
                    required = False,
                    help_text=_("Entrez le nom de la commune"))
    province = ChoiceFieldCustomValidation(label=_("Province"),
                    widget=forms.Select(attrs={"id": "province_choice",
                                        "data-toggle": "tooltip",
                                        "title": "Sélectionez la Province"
                                        " pour généner la list des Villes"}),
                    choices=(("", "Choisissez la province"),),
                    required=False,
                    help_text=_("Choisissez la province"))
    localization = forms.ChoiceField(
                    label=_("Are you in D.R. Congo?"),
                    required=True,
                    widget=forms.RadioSelect(),
                    choices=(("1", "Yes"), ("2", "No")))
    country_origin = forms.ChoiceField(label=_("Country"),
                    widget=forms.Select(attrs={"id": "world_country_choice"}),
                    choices=WORLD_COUNTRY_CHOICES,
                    required=False,
                    help_text=_("Choose the country you live in"))
    city_origin = forms.CharField(label=_("City and/or State(Province)"),
                    widget=forms.TextInput(),
                    required=False,
                    help_text=_("Enter the city(state)"))
    first_name = forms.CharField(label=_("First Name"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Enter your first name"))
    middle_name = forms.CharField(label=_("Middle Name"),
                    widget=forms.TextInput(),
                    required=False,
                    help_text=_("Enter your middle name"))
    last_name = forms.CharField(label=_("Last Name"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Enter your last name"))
    username = forms.CharField(label=_('Username'),
                    widget=forms.TextInput(attrs={"disabled": "disabled"}),
                    required=False,
                    help_text=_("This is generated automatically"))
    email = forms.EmailField(label=_('Email'),
                    required=False,
                    help_text=_("Enter email address"))
    sponsor_type = forms.ChoiceField(
                    label=_("Type of Sponsor"),
                    widget=forms.Select(),
                    choices=(("0", "Business"), ("1", "Individual")),
                    required=True,
                    help_text=_("Is this a Business or a person?"))
    company_name = forms.CharField(label=_("Company Name"),
                    widget=forms.TextInput(),
                    required=False,
                    help_text=_("Enter your company name"))
    phone_number_1 = PhoneNumberField(
                    label=_("Primary Phone"),
                    widget=forms.TextInput(),
                    required=True)
    phone_number_2 = PhoneNumberField(
                    label=_("Secondary Phone"),
                    widget=forms.TextInput(),
                    required=False)
    password1 = forms.CharField(label=_("Password"),
                    widget=forms.PasswordInput(render_value=False),
                    required=False,
                    help_text=_("Enter your passowrd."))
    password2 = forms.CharField(label=_("Repeat the Password"),
                    widget=forms.PasswordInput(render_value=False),
                    required=False,
                    help_text=_("Enter again the same passowrd."))


