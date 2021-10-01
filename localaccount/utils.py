# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from django.contrib.auth.models import User, AnonymousUser
from django.utils.translation import ugettext_lazy as _

from domeproject.models import ProjectSponsor
from localcore.models import Address
from localcore.queries_utils import DEFAULT_COUNTRY, \
                                    ModelsQueries as CoreModelsQueries

import sys
import traceback


class AbstractNewAccountProcessing(metaclass=ABCMeta):

    def __init__(self, form_fields):
        self.form_fields = form_fields

    @abstractmethod
    def save_address(self):
        pass

    @abstractmethod
    def save_user(self):
        pass

    @abstractmethod
    def save_profile(self):
        pass


class AbstractExistingAccountProcessing(metaclass=ABCMeta):

    def __init__(self, form_fields):
        self.form_fields = form_fields

    @abstractmethod
    def update_address(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def update_profile(self):
        pass


class NewSponsorAccountProcessing(AbstractNewAccountProcessing):

    def save_address(self):
        address_dict = self.form_fields.get("address", {})

        localization = address_dict.get("localization", "")
        if localization == "1":
            country_type = "0"
        elif localization == "2":
            country_type = "1"

        street = address_dict.get("street", "")
        address = Address()
        try:
            address.street = street
            address.country_type = country_type

            if "1" == localization:
                city_id = address_dict.get("city", "")
                city = CoreModelsQueries.get_city_from_id(city_id=city_id)
                commune_id = address_dict.get("commune", "")
                commune = CoreModelsQueries.get_commune_from_id(
                                                        commune_id=commune_id)
                province_id = address_dict.get("province", "")
                province = CoreModelsQueries.get_province_from_id(
                                                       province_id=province_id)
                address.city = city
                address.commune = commune
                address.province = province

            elif "2" == localization:
                country_origin_code = address_dict.get("country_origin", "")
                country_origin = CoreModelsQueries.get_country_from_code(
                                            country_code=country_origin_code)
                city_origin = address_dict.get("city_origin", "")
                address.city_origin = city_origin
                address.country = country_origin
            address.save()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return address

    def save_user(self):
        user_dict = self.form_fields.get("user", {})
        user = User()
        first_name = user_dict.get("first_name", "")
        last_name = user_dict.get("last_name", "")
        email = user_dict.get("email", "")
        username = user_dict.get("username", "")
        if not username:
            username = "{}_{}".format(first_name.strip().capitalize(),
                                        last_name.strip().capitalize())
        password = user_dict.get("password1", "")
        if not email:
            return user
        if not password:
            return user

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.password = password
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        try:
            user.set_password(password)
            user.is_active = True
            user.save()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return user

    def save_profile(self, address=None, user=None):
        sponsor_dict = self.form_fields.get("sponsor", {})
        sponsor = ProjectSponsor()
        middle_name = sponsor_dict.get("middle_name", "")
        sponsor_type = sponsor_dict.get("sponsor_type", "")
        company_name = sponsor_dict.get("company_name", "")
        phone_number_1 = sponsor_dict.get("phone_number_1", "")
        phone_number_2 = sponsor_dict.get("phone_number_2", "")
        company_logo = sponsor_dict.get("company_logo", "")
        if not company_logo:
            company_logo = "good-no-image-available.jpg"

        try:
            sponsor.middle_name = middle_name
            sponsor.sponsor_type = sponsor_type
            sponsor.company_name = company_name
            sponsor.phone_number_1 = phone_number_1
            sponsor.phone_number_2 = phone_number_2
            sponsor.company_logo = company_logo
            sponsor.auth_user = user
            sponsor.address = address
            sponsor.save()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return sponsor

    def create_sponsor(self):
        sponsor_address = self.save_address()
        print("SPONSOR SAVED ADDRESS")
        print(sponsor_address)

        address_id = None
        try:
            address_id = sponsor_address.id
        except Exception:
            pass

        address_error = ""
        if address_id:
            is_created = True
        else:
            is_created = False
            address_error = _("Sponsor's Address not created")

        user_id = None
        if is_created:
            sponsor_user = self.save_user()
            print("SPONSOR SAVED USER")
            print(sponsor_user)

        try:
            user_id = sponsor_user.id
        except Exception:
            pass

        user_error = ""
        if user_id:
            is_created = True
        else:
            is_created = False
            user_error = _("Sponsor's User not created")

        if is_created:
            sponsor_profile = self.save_profile(
                                                address=sponsor_address,
                                                user=sponsor_user)
            print("SPONSOR SAVED PROFILE")
            print(sponsor_profile)

        profile_id = None
        try:
            profile_id = sponsor_profile.id
        except Exception:
            pass

        sponsor_message = ""
        if profile_id:
            sponsor = sponsor_profile
            profile_message = _("Project Sponsor Created")
        else:
            sponsor = ProjectSponsor()
            profile_message = _("Sponsor Profile not created")

        message = ""
        if address_error:
            message = message + " " + address_error + "\n"
        if user_error:
            message = message + " " + user_error + "\n"
        message = message + " " + profile_message

        return {"sponsor": sponsor, "message": message}


class NewProjectInitiatorAccountProcessing(AbstractNewAccountProcessing):

    def save_address(self):
        pass

    def save_user(self):
        pass

    def save_profile(self):
        pass

    def create_project_initiator(self):
        pass


class NewIndependentCineasteAccountProcessing(AbstractNewAccountProcessing):

    def save_address(self):
        pass

    def save_user(self):
        pass

    def save_profile(self):
        pass

    def create_independent_cineaste(self):
        pass


class UpdateSponsorAccountProcessing(AbstractExistingAccountProcessing):

    def update_address(self):
        pass

    def update_user(self):
        pass

    def update_profile(self):
        pass

    def update_sponsor(self):
        pass


class UpdateProjectInitiatorAccountProcessing(
                                        AbstractExistingAccountProcessing):

    def update_address(self):
        pass

    def update_user(self):
        pass

    def update_profile(self):
        pass

    def update_project_initiator(self):
        pass


class UpdateIndependentCineasteAccountProcessing(AbstractNewAccountProcessing):

    def update_address(self):
        pass

    def update_user(self):
        pass

    def update_profile(self):
        pass

    def update_independent_cineaste(self):
        pass


class NewAccountProcessingFactory:

    @classmethod
    def create(cls, name, is_create=True, form_fields={}, *args, **kwargs):
        name = name.lower().strip()

        if is_create:
            if name == "sponsor":
                return NewSponsorAccountProcessing(form_fields)
            elif name == "project_initiator":
                return NewProjectInitiatorAccountProcessing(form_fields)
            elif name == "independent_cineaste":
                return NewIndependentCineasteAccountProcessing(form_fields)
            else:
                return None

        else:
            if name == "sponsor":
                return UpdateSponsorAccountProcessing(form_fields)
            elif name == "project_initiator":
                return UpdateProjectInitiatorAccountProcessing(form_fields)
            elif name == "independent_cineaste":
                return UpdateIndependentCineasteAccountProcessing(form_fields)
            else:
                return None