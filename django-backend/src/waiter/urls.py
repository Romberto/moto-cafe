

from django.urls import path

from waiter.views import WaiterPanel

urlpatterns = [
    path('', WaiterPanel.as_view(), name='waiter-panel'),
    ]