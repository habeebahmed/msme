from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('Financial', views.Financial, name='Financial'),
    path('Loan',views.Loan, name='Loan'),
    path('Business',views.Business, name='Business'),
    path('Contact',views.Contact, name='Contact'),
    path('Documents',views.Documents, name='Documents'),
    path('LoginUser',views.LoginUser,name='LoginUser'),
    path('DashBoard1',views.DashBoard1,name='DashBoard1'),
    path('Payment',views.Payment,name='Payment')
]