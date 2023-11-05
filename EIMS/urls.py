from django.urls import path
from . import views
from .views import ExpenditureinDetail, CreateExp, UpdateExp

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('specific-expenditure/<str:pk>/', ExpenditureinDetail.as_view(), name = 'exp-details'),
    path('update-expenditure/<str:pk>/', UpdateExp.as_view(), name = 'update-exp'),
    path('create-expenditure/<str:pk>/', CreateExp.as_view(), name = 'create-exp'),
    path('all-expenditure-records', views.allExpRecords, name='allexp'),
    path('signout', views.signout, name='signout'),
    path('allExp-records', views.allExpRecords, name='allExp-records'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),    

    #change password
    path('change-password/', PasswordsChangeView.as_view(template_name='accounts/change-password.html'), name='change-password'),
    #forgot password / resetting security key
    #1
    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name='accounts/email_input_reset_password.html'), 
    name='reset_password'),
    #2
    path('password_reset_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), 
    name='password_reset_done'),
    #3
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
    name='password_reset_confirm'),
    #4
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
    name='password_reset_complete'),
]