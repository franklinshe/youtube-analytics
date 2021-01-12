from django.urls import path
from .views import home, charts

app_name = 'watch_history'

urlpatterns = [
    path('', home, name='home'),
    path('charts/', charts, name='charts')
]
