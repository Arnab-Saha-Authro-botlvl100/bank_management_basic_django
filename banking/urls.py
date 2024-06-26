# banking/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='banking/login.html'), name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Ensure correct configuration
    path('create-account/', views.create_account, name='create_account'),  # Add this line
    path('money_transfer/<int:account_id>/', views.money_transfer, name='money_transfer'),  # Add this line
    path('account/edit/<int:account_id>/', views.edit_account, name='edit_account'),  # New URL pattern
    path('get_account_details/', views.get_account_details, name='get_account_details'),
    # path('self_tresfer/', views.self_tresfer, name='self_tresfer'),

]
