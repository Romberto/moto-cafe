from django.urls import path
from .views import MyLoginView, MyLogoutView, ResetPassword

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('resetpassword/<int:pk>', ResetPassword.as_view(), name='resetpassword')

]
