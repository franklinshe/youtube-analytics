from django.urls import path
from .views import home, charts, table

app_name = 'watch_history'

urlpatterns = [
    path('', home, name='home'),
    path('charts/', charts, name='charts'),
    path('table/', table, name='table')
]
