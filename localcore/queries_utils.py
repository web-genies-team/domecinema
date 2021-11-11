# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from .models import Country, Province, City, Commune, Address

import sys
import traceback


try:
    DEFAULT_COUNTRY = [] #Country.objects.get(code="DRC")
except Exception:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    DEFAULT_COUNTRY = None


class ModelsQueries:

    @staticmethod
    def get_province_from_id(province_id=None):
        if province_id:
            try:
                province = Province.objects.get(id=int(province_id))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                province = None
        else:
            province = None
        return province

    @staticmethod
    def get_city_from_id(city_id=None):
        if city_id:
            try:
                city = City.objects.get(id=int(city_id))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                city = None
        else:
            city = None
        return city

    @staticmethod
    def get_commune_from_id(commune_id=None):
        if commune_id:
            try:
                commune = Commune.objects.get(id=int(commune_id))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                commune = None
        else:
            commune = None
        return commune

    @staticmethod
    def get_country_from_id(country_id=None):
        if country_id:
            try:
                country = Country.objects.get(id=int(country_id))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                country = None
        else:
            country = None
        return country

    @staticmethod
    def get_country_from_code(country_code=None):
        if country_code:
            try:
                country = Country.objects.get(code=country_code)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                country = None
        else:
            country = None
        return country

    @staticmethod
    def get_countries_for_choices():

        try:
            countries = Country.objects.all().values("code", "english_name")
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            countries = None

        if countries:
            result = [(cntr["code"], cntr["english_name"])
                                                      for cntr in countries]
            return result
        else:
            return None
