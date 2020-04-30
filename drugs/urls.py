from django.urls import path
from drugs.views import DrugsListView


urlpatterns = [
    path('', DrugsListView.as_view(), name='drugs'),
]
