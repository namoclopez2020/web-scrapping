from django.urls import path
from fomento_unit_values.views import get_unit_values
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path(
        route='unit-values',
        view=get_unit_values,
        name='get_unit_values'
    )
]
