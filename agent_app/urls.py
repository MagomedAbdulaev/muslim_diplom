from django.urls import path
from .views import *

app_name = 'agent_app'

urlpatterns = [
  path('', home, name='home'),
  path('get_suppliers/', get_suppliers, name='get_suppliers'),
]
