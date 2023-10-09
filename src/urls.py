from django.urls import path
from .views import SubmitFormView
from .views import Admin
from .views import YourNewView
urlpatterns = [
    path('submit/', SubmitFormView.as_view(), name='submit-form'),
    path('admin/', Admin.as_view(), name="admin"),
    path('submit/new', YourNewView.as_view(), name='submit-form'),
]
