from django.shortcuts import render,redirect
import django.core.exceptions
# Create your views here.
from msmeapp.models import *	
from django.http import HttpResponse
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import smtplib
from django.core.mail import EmailMessage,send_mail
import requests,json

def CustomerDashBoardWB(request):
	if request.method == "POST" and "Edit" in request.POST:
		return redirect('transfer')
	elif request.method == "POST" and "View" in request.POST:
		return redirect('CustomerDisplayApplications')
	return render(request,'CustomerDashboardWB.html',{})


def LoginWB(request):
	if request.method=="POST":
		Eid1 = request.POST.get("eid")
		try:    
			euid = UTEmployee.objects.get(Emp_ID=Eid1)
		except UTEmployee.DoesNotExist:
			return HttpResponse(Eid1+" does not exist")
		pass1 = request.POST.get("password")
		t=1
		for e in UTEmployee.objects.all():
			if(e.Emp_ID==Eid1 and e.password==pass1):
				t=0
				break
		if(t==0):
			if euid.Emp_ID[:2] == 'CS':
				return redirect('CustomerDashBoardWB')
			elif euid.Emp_ID[:2] == 'ST':
				return redirect('Staff')
			elif euid.Emp_ID[:2] == 'MG':
				return redirect('Manager')
			else:
				return HttpResponse("invalid username and password")
		else:
			return HttpResponse("invalid username and password")

	else:
		return render(request,'LoginWB.html',{})

def Staff(request):
	if request.method == "POST" and "Edit" in request.POST:
		return redirect('transfer')
	elif request.method == "POST" and "View" in request.POST:
		return redirect('CSverifiedApplications')    
	return render(request,'Staff.html',{})

def CSverifiedApplications(request):
	#a = Application_Details.objects.filter(Status='CS')
	if request.method=="POST" and "DocumentVerification" in request.POST:
		appln_id = request.POST.get('DocumentVerification')
		app_details = Application_Details.objects.get(Application_ID=appln_id)
		app_details.Status = "DV"
		app_details.save()
		return render(request,'DocumentsVerified.html',{})
	if request.method=="POST" and "Reject" in request.POST:
		appln_id = request.POST.get('Reject')
		app_details = Application_Details.objects.get(Application_ID=appln_id) 
		app_details.Status = "R"
		app_details.save()
		ar = App_Rejected()
		b_detail = Business_Details.objects.get(Application_ID=appln_id)
		ar.Application_ID = app_details
		ar.B_ID = b_detail
		ar.Reason_code = Reject_reason.objects.get(Reason_code='C')
		ar.save()
		applicant = Applicant_Details.objects.get(Application_ID=appln_id)
		mail_subject = 'Application Rejected'
		message = 'Hello, '+applicant.Applicant_Name+'. We are sorry to inform you that your loan application has been Rejected. Thank you.'
		a_email1 = applicant.Applicant_Email
		send_mail(mail_subject,message,'',[a_email1],fail_silently=False)
		return render(request,'DocumentsRejected.html',{})
	if request.method=="POST" and "DocumentsAwaiting" in request.POST:
		appln_id = request.POST.get('DocumentsAwaiting')
		app_details = Application_Details.objects.get(Application_ID=appln_id) 
		app_details.Status = "DW"
		app_details.save()
		applicant = Applicant_Details.objects.get(Application_ID=appln_id)
		mail_subject = 'Documents Awaiting'
		message = 'Hello, '+applicant.Applicant_Name+'. Your application is missing important Documents. Kindly submit them as soon as possible for fast processing of your loan Application. Thank you.'
		a_email1 = applicant.Applicant_Email
		send_mail(mail_subject,message,'',[a_email1],fail_silently=False)
	#api call
	data = {
		"table" : "application_details",
 		"status" : "CS"
	}
	res = requests.post(url = "http://localhost:8080/test", data = data)
	r = Parse(res.text)
	print(r.data)
	a = r.data		
	return render(request,'CSverifiedApplications.html',{'applications': a})

def DocumentsRejected(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CSverifiedApplications')
	return render(request,'DocumentsRejected.html')

def DocumentsVerified(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CSverifiedApplications')
	return render(request,'DocumentsVerified.html')

def Manager(request):
	if request.method == "POST" and "Edit" in request.POST:
		return redirect('transfer')
	elif request.method == "POST" and "View" in request.POST:
		return redirect('ManagerApplications')    
	return render(request,'Manager.html',{})

def ManagerApplications(request):
	#api call
	#a = Application_Details.objects.filter(Status='DV')
	data = {
		"table" : "application_details",
 		"status" : "DV"
	}
	res = requests.post(url = "http://localhost:8080/test", data = data)
	r = Parse(res.text)
	print(r.data)
	a = r.data
	return render(request,'ManagerApplications.html',{'applications':a})

def ManagerApplicationDetails(request):
	if request.method=="POST" and "Back" in request.POST:
		return redirect('ManagerApplications')
	print("In manager Details")
	appln_id = request.GET.get('appln_id')
	app_details = Application_Details.objects.get(Application_ID=appln_id)
	a_detail = Applicant_Details.objects.get(Application_ID=appln_id)
	b_detail = Business_Details.objects.get(Application_ID=appln_id)
	a_addr = Applicant_Addr.objects.get(id=a_detail.id)
	b_addr = Business_Addr.objects.get(B_ID=b_detail.B_ID)
	f_obj = Financials.objects.get(Application_ID=appln_id)
	asset_info = f_obj.Assets_ID
	capital_info = f_obj.Capital_ID
	liabilities_info = f_obj.Liabilities_ID
	cashflow_info = f_obj.Cash_Flows_ID
	reserves_info = f_obj.Reserves_ID
	if request.method=="POST" and "Approve" in request.POST:
		print("In approve")
		ill = Investor_lending.objects.order_by('Last_Update')
		appln_id = request.GET.get('appln_id')
		app_details = Application_Details.objects.get(Application_ID=appln_id)
		for il in ill:
			if il.Amount_available is not None and app_details.Amount <= il.Amount_available:
				il.Amount_available -= app_details.Amount
				il.Last_Update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				il.save()
				app_details.Status = 'D'
				app_details.save()
				da = Disbursed_appl()
				da.Application_ID = Application_Details.objects.get(Application_ID=app_details.Application_ID)
				da.Amount = app_details.Amount
				da.Disbursed_date = date.today()
				da.Due_date = da.Disbursed_date + relativedelta(months=+app_details.Tenure)
				p = app_details.Amount
				r = 0.07
				da.S_Interest = (p*r)
				da.Due_Amount = app_details.Amount + da.S_Interest
				da.save()
				t = Transactions()
				t.Application_ID = Application_Details.objects.get(Application_ID=app_details.Application_ID)
				t.Inv_ID_id = il.Inv_ID_id
				t.save()
				for i in range(1,app_details.Tenure+1):
					ins = Installments()
					ins.Application_ID = app_details
					ins.DueDate = getDueDate(i)
					ins.Base_Amount = app_details.Amount/app_details.Tenure
					ins.S_Interest = (app_details.Amount/app_details.Tenure) * 0.07
					ins.Total_Amount = (app_details.Amount/app_details.Tenure)+((app_details.Amount/app_details.Tenure)*0.07)
					ins.save()
				applicant = Applicant_Details.objects.get(Application_ID=appln_id)
				print(applicant.Applicant_ID)
				try:
					u = User_Credentials.objects.get(User_ID=applicant.Applicant_ID)
					u_name = u.User_ID
					pw = u.Password
				except User_Credentials.DoesNotExist:
					u_name = applicant.Applicant_ID
					pw = applicant.Applicant_ID + 'pass'
					uc_new = User_Credentials()
					uc_new.User_ID = u_name
					uc_new.Password = pw
					uc_new.save()
					print(u_name)
				mail_subject = 'Loan Approved'
				message = 'Hello, '+applicant.Applicant_Name+'. Your loan application is successfully Approved, the amount has been disbursed.Your login credentials are.\nUsername : '+u_name+'\n Password : '+pw+'\n\nUse these to login to your page to repay the loan.\nThank you.'
				a_email1 = applicant.Applicant_Email
				send_mail(mail_subject,message,'',[a_email1],fail_silently=False)
				print(a_email1)
				return redirect('LoanApproved')
				break
			else:
				continue
	if request.method=="POST" and "Reject" in request.POST:
		appln_id = request.GET.get('appln_id')
		app_details = Application_Details.objects.get(Application_ID=appln_id)
		app_details.Status = "R"
		app_details.save()
		ar = App_Rejected()
		ar.Application_ID = app_details
		ar.B_ID = b_detail
		ar.Reason_code = Reject_reason.objects.get(Reason_code=request.POST.get("reason1"))
		ar.save()
		applicant = Applicant_Details.objects.get(Application_ID=appln_id)
		mail_subject = 'Application Rejected'
		message = 'Hello, '+applicant.Applicant_Name+'. Your loan application has been rejected. Thank you.'
		a_email1 = applicant.Applicant_Email
		send_mail(mail_subject,message,'',[a_email1],fail_silently=False)	
		return redirect('ManagerReject')
	if request.method=="POST" and "Blacklist" in request.POST:
		bl = Blacklisted()
		bl.Applicant_ID = a_detail.Applicant_ID
		bl.B_ID = b_detail
		bl.save()
		appln_id = request.GET.get('appln_id')
		app_details = Application_Details.objects.get(Application_ID=appln_id)
		app_details.Status = "BL"
		app_details.save()
		applicant = Applicant_Details.objects.get(Application_ID=appln_id)
		mail_subject = 'Application Rejected'
		message = 'Hello, '+applicant.Applicant_Name+'. Your loan application has been rejected. Thank you.'
		a_email1 = applicant.Applicant_Email
		send_mail(mail_subject,message,'',[a_email1],fail_silently=False)
		return redirect('Blacklist')
	return render(request,'ManagerApplicationDetails.html',{'Application_Details':app_details,'Applicant_Details':a_detail,'Applicant_Addr':a_addr,'Business_Details':b_detail,'Business_Addr':b_addr,'a':asset_info,'c':capital_info,'l':liabilities_info,'cf':cashflow_info,'r':reserves_info})

def getDueDate(tenure):
	return 	date.today() + relativedelta(months=+tenure)

def LoanApproved(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('ManagerApplications')
	return render(request,'LoanApproved.html')

def ManagerReject(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('ManagerApplications')
	return render(request,'ManagerReject.html')

def CustomerDisplayApplications(request):
	#api call
	#a = Application_Details.objects.exclude(Status='BL')
	data = {
		"table" : "application_details",
 		"status" : "BL"
	}
	res = requests.post(url = "http://localhost:8080/test", data = data)
	r = Parse(res.text)
	print(r.data)
	a = r.data
	return render(request,'CustomerDisplayApplications.html',{'applications': a})

def CustomerDetails(request):
	if request.method=="POST" and "Back" in request.POST:
		return redirect('CustomerDisplayApplications')
	appln_id = request.GET.get('appln_id')
	app_details = Application_Details.objects.get(Application_ID=appln_id)
	a_detail = Applicant_Details.objects.get(Application_ID=appln_id)
	b_detail = Business_Details.objects.get(Application_ID=appln_id)
	a_addr = Applicant_Addr.objects.get(id=a_detail.id)
	b_addr = Business_Addr.objects.get(B_ID=b_detail.B_ID)
	if request.method=="POST" and "Reject" in request.POST:
		appln_id = request.GET.get('appln_id')
		app_details = Application_Details.objects.get(Application_ID=appln_id)
		app_details.Status = "R"
		app_details.save()
		ar = App_Rejected()
		ar.Application_ID = app_details
		ar.B_ID = b_detail
		ar.Reason_code = Reject_reason.objects.get(Reason_code='D')
		ar.save()
		mail_subject = 'Application Rejected'
		message = 'Hello, '+a_detail.Applicant_Name+'. We are sorry to inform you that your loan application has been Rejected. Thank you.'
		a_email1 = a_detail.Applicant_Email
		send_mail(mail_subject,message,'',[a_email1],fail_silently=False)
		return redirect('Reject')
	if request.method=="POST" and "VerifyApplication" in request.POST:
		appln_id = request.GET.get('appln_id')
		app_details = Application_Details.objects.get(Application_ID=appln_id)
		app_details.Status = "CS"
		app_details.save()
		return redirect('ApplicationVerified')
	return render(request,'CustomerDetails.html',{'Application_Details':app_details,'Applicant_Details':a_detail,'Applicant_Addr':a_addr,'Business_Details':b_detail,'Business_Addr':b_addr})
def Reject(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CustomerDisplayApplications')
	return render(request,'Reject.html')
def Blacklist(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('ManagerApplications')
	return render(request,'Blacklist.html')

def ApplicationVerified(request):
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CustomerDisplayApplications')
	return render(request,'ApplicationVerified.html')
#Repayment phase
# def Payment(request):
# 	if request.GET.get('appln_id') and request.method !="POST" :
# 		appln_id = request.GET.get('appln_id')
# 		da1 = Disbursed_appl.objects.get(Application_ID=appln_id)
# 		da = Disbursed_appl.objects.get(Application_ID=da1.Application_ID)
# 		d_cur = date.today() + relativedelta(days=+3)
# 		if d_cur <= da.Due_date:
# 			print('before due')
# 		else:
# 			print('after due')

class Parse(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)