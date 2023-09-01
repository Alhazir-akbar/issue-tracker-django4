from django.urls import path
from .views import RegisterView, dashboard
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
