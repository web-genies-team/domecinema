# -*- coding: utf-8 -*-
from django import template
from ..queries_utils import ModelsQueries

import sys
import traceback


register = template.Library()


@register.simple_tag
def get_home_url():
    url = ""
    try:
        url = ModelsQueries.get_home_url()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)

    return url