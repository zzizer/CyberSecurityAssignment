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
]