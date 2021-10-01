# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include, path

from .views import CreateSponsorFormView, ProjectSponsorHome


app_name = "localaccount"

urlpatterns = [
    path('create-project-sponsor', CreateSponsorFormView.as_view(),
                                            name="create_project_sponsor"),
    path('project-sponsor-home', ProjectSponsorHome.as_view(),
                                            name="project_sponsor_home"),
]

