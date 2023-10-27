from django.contrib import admin
from django.urls import path, include
from globus_portal_framework.urls import register_custom_index
from gdss.views import publish_data_flow


app_name = 'gdss'
register_custom_index('gdss_index', ['gdss'])


urlpatterns = [
    path('<gdss_index:index>/publish-data/', publish_data_flow, name='publish-data'),
    path("", include("globus_portal_framework.urls")),
    path("", include("social_django.urls", namespace="social")),
]
