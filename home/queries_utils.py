# -*- coding: utf-8 -*-
#from home.models import HomePage
import sys
import traceback


class ModelsQueries:

    def get_home_page_url(self):
        url = ""

        """
        try:
            page = HomePage.objects.get(slug='home')
        except Exception:
            page = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        if page:
            try:
                url = page.get_url()
            except Exception:
                pass
        """
        return url