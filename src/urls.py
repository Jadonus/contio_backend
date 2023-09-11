from django.urls import path
from .views import SubmitFormView

from .views import YourNewView
urlpatterns = [
    path('submit/', SubmitFormView.as_view(), name='submit-form'),

    path('submit/new', YourNewView.as_view(), name='submit-form'),
]
