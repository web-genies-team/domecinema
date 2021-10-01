# -*- coding: utf-8 -*-
from .models import Country
import sys
import traceback
import csv


def load_countries_from_csv_to_model(csv_name=""):
    countries_input = open('countries.csv')
    countries_dict_reader = csv.DictReader(countries_input,
                ["english_name", "french_name", "code", "continent", "region"])

    for row in countries_dict_reader:
        try:
            country = Country()
            country.english_name = row["english_name"]
            country.french_name = row["french_name"]
            country.code = row["code"]
            country.region = row["region"]
            country.continent = row["continent"]
            country.save()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    countries_input.close()
