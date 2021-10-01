# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = "home/home_page.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)