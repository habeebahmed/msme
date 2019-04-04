from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
	path('Login', views.LoginWB, name='LoginWB'),
	path('CustomerDashBoardWB', views.CustomerDashBoardWB, name='CustomerDashBoardWB'),
	path('CustomerDisplayApplications', views.CustomerDisplayApplications, name='CustomerDisplayApplications'),
    path('Logout', views.Logout, name='Logout'),
	path('CustomerDetails', views.CustomerDetails, name='CustomerDetails'),
	path('Reject',views.Reject,name='Reject'),
	path('Blacklist',views.Blacklist,name='Blacklist'),
	path('ApplicationVerified',views.ApplicationVerified,name='ApplicationVerified'),
    path('AlreadyVerified',views.AlreadyVerified,name='AlreadyVerified'),
    path('Staff',views.Staff,name='Staff'),
    path('CSverifiedApplications',views.CSverifiedApplications,name='CSverifiedApplications'),
    path('Manager',views.Manager,name='Manager'),
    path('DocumentsVerified',views.DocumentsVerified,name='DocumentsVerified'),
    path('DocumentsRejected',views.DocumentsRejected,name='DocumentsRejected'),
    path('ManagerApplications',views.ManagerApplications,name='ManagerApplications'),
    path('ManagerApplicationDetails',views.ManagerApplicationDetails,name='ManagerApplicationDetails'),
    path('ManagerReject',views.ManagerReject,name='ManagerReject'),
    path('LoanApproved',views.LoanApproved,name='LoanApproved')
]