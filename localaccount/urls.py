# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include, path

from .views import CreateSponsorFormView, ProjectSponsorHome, \
                    ProjectSponsorPage


app_name = "localaccount"

urlpatterns = [
    path('project-investors', CreateSponsorFormView.as_view(),
                                            name="create_project_sponsor"),
    path('project-investors-home', ProjectSponsorHome.as_view(),
                                            name="project_sponsor_home"),
    path(r'^(?P<slug>[A-Za-z0-9\-]*)/projet-investor-page/$',
                ProjectSponsorPage.as_view(), name="projet-investor-page"),
]

