from django.shortcuts import render
from django.views import View
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.messages import info, error

from .forms import SponsorProfileForm
from .utils import NewAccountProcessingFactory
from domeproject.models import get_sponsors_home_page


class SponsorFormView(View):
    form_class = SponsorProfileForm
    sponsor_form_fields = {"address": {}, "user": {}, "sponsor": {}}

    def _get_form_cleaned_data(self, request):
        sponsor_form = self.form_class(request.POST or None)
        print("PRINTING SPONSOR FORM DATA")
        print(sponsor_form.__dict__)

        if sponsor_form.is_valid():
            self.sponsor_form_fields["address"]["street"] = \
                            sponsor_form.cleaned_data.get("street", "")
            self.sponsor_form_fields["address"]["city"] = \
                            sponsor_form.cleaned_data.get("city", "")
            self.sponsor_form_fields["address"]["commune"] = \
                            sponsor_form.cleaned_data.get("commune", "")
            self.sponsor_form_fields["address"]["province"] = \
                            sponsor_form.cleaned_data.get("province", "")
            self.sponsor_form_fields["address"]["localization"] = \
                            sponsor_form.cleaned_data.get("localization", "")
            self.sponsor_form_fields["address"]["country_origin"] = \
                            sponsor_form.cleaned_data.get("country_origin", "")
            self.sponsor_form_fields["address"]["city_origin"] = \
                            sponsor_form.cleaned_data.get("city_origin", "")
            self.sponsor_form_fields["user"]["first_name"] = \
                            sponsor_form.cleaned_data.get("first_name", "")
            self.sponsor_form_fields["user"]["last_name"] = \
                            sponsor_form.cleaned_data.get("last_name", "")
            self.sponsor_form_fields["user"]["email"] = \
                            sponsor_form.cleaned_data.get("email", "")
            self.sponsor_form_fields["user"]["username"] = \
                            sponsor_form.cleaned_data.get("username", "")
            self.sponsor_form_fields["user"]["password1"] = \
                            sponsor_form.cleaned_data.get("password1", "")
            self.sponsor_form_fields["user"]["password2"] = \
                            sponsor_form.cleaned_data.get("password2", "")
            self.sponsor_form_fields["sponsor"]["middle_name"] = \
                            sponsor_form.cleaned_data.get("middle_name", "")
            self.sponsor_form_fields["sponsor"]["sponsor_type"] = \
                            sponsor_form.cleaned_data.get("sponsor_type", "")
            self.sponsor_form_fields["sponsor"]["company_name"] = \
                            sponsor_form.cleaned_data.get("company_name", "")
            self.sponsor_form_fields["sponsor"]["phone_number_1"] = \
                            sponsor_form.cleaned_data.get("phone_number_1", "")
            self.sponsor_form_fields["sponsor"]["phone_number_2"] = \
                            sponsor_form.cleaned_data.get("phone_number_2", "")
            print("PRINTING SPONSOR FORM FIELDS DICT")
            print(self.sponsor_form_fields)
            return True
        else:
            print("PRINTING SPONSOR FORM IS NOT VALID")
            return False


class CreateSponsorFormView(SponsorFormView):
    template_name = "localaccount/sponsor_signup.html"

    def __init__(self):
        super(CreateSponsorFormView, self).__init__()

    def get(self, request, *args, **kwargs):
        sponsor_form = self.form_class()
        return render(request, self.template_name,
                                        {"sponsor_form": sponsor_form})

    def post(self, request, *args, **kwargs):
        print("IN POST CREATE SPONSOR CLEANED DATA")
        print(self.sponsor_form_fields)
        sponsor_account_processing = None
        if self._get_form_cleaned_data(request):
            print(self.sponsor_form_fields)
            sponsor_factory = NewAccountProcessingFactory()
            sponsor_account_processing = sponsor_factory.create(
                                        'sponsor',
                                        form_fields=self.sponsor_form_fields)
        result = {}
        if sponsor_account_processing:
            result = sponsor_account_processing.create_sponsor()
            print("PRINTING SPONSOR CREATE RESULT")
            print(result)
        if not result:
            error(request, _("Sponsor Account create did not start"))
        else:
            sponsor = result.get("sponsor")
            sponsor_id = None
            try:
                sponsor_id = sponsor.id
            except Exception:
                pass
            if sponsor_id:
                info(request, _(result.get("message")))
            else:
                error(request, _(result.get("message")))
        sponsor_form = self.form_class()
        return render(request, self.template_name,
                                        {"sponsor_form": sponsor_form})


class ProjectSponsorHome(View):
    template_name = "localaccount/sponsors_home.html"

    def get(self, request, *args, **kwargs):
        sponsors_home = get_sponsors_home_page()
        return render(request, self.template_name, {"page": sponsors_home})