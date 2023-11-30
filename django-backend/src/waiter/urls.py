
from django.urls import path


from waiter.views import WaitersView, EditWaiterView, DeleteWaiterView, CreateWaiter

urlpatterns = [
   path('', WaitersView.as_view(), name='all_waiters'),
   path('edit/<int:pk>', EditWaiterView.as_view(), name="edit_waiters"),
   path('delete_waiter/<int:pk>', DeleteWaiterView.as_view(), name="delete_waiter"),
   path('add_waiter', CreateWaiter.as_view(), name="add_waiter")
]
