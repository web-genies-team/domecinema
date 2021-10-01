# -*- coding: utf-8 -*-
from domeproject.models import SponsorPage, get_site_root_page
from django.utils.text import slugify

import sys
import traceback


class ModelsQueries:

    @staticmethod
    def get_singleton_sponsor_home():
        is_exist_sponsor_home = True
        sponsor_home = None
        try:
            sponsor_home = SponsorPage.objects.get(is_home_page=True)
            print("FOUND SPONSORS HOME PAGE")
            print(sponsor_home.__dict__)
        except SponsorPage.DoesNotExist:
            print("SPONSORS PAGE NOT EXIST")
            is_exist_sponsor_home = False
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        if sponsor_home and is_exist_sponsor_home:
            print("RETURNED SPONSORS PAGE")
            print(sponsor_home)
            return sponsor_home
        else:
            is_exist_sponsor_home = False

        site_root = get_site_root_page()

        if not is_exist_sponsor_home and site_root:
            try:
                site_root.add_child(
                        title="Sponsors' Space",
                        slug=slugify("Sponsors' Space"),
                        url_path = "{}/".format(slugify("Sponsors' Space")),
                        is_home_page=True,
                        use_home_template=True
                )
                print("SAVED SPONSORS HOME")
                print(site_root.get_first_child())
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        return sponsor_home