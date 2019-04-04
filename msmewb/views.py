from django.shortcuts import render,redirect
import django.core.exceptions
from msmeapp.models import *	
from django.http import HttpResponse,JsonResponse
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import smtplib
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import logout
import requests,json
from .decorators import *

#server_url = "http://10.15.15.62:8080/test"
server_url = "http://localhost:8080/test"

def Logout(request):
	logout(request)
	# del request.session['username']
	return redirect('LoginWB')

@already_loggedin
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
			request.session['username'] = Eid1
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


@cs_not_loggedin
def CustomerDashBoardWB(request):
	request.session['path'] = 'CustomerDashBoardWB'
	if request.method == "POST" and "Edit" in request.POST:
		return redirect('transfer')
	elif request.method == "POST" and "View" in request.POST:
		return redirect('CustomerDisplayApplications')
	elif request.method == "POST" and "Logout" in request.POST:
		return redirect('Logout')
	return render(request,'CustomerDashboardWB.html',{})

@cs_not_loggedin
def CustomerDisplayApplications(request):
	request.session['path'] = 'CustomerDisplayApplications'
	request.session.set_expiry(request.session.get_expiry_age())
	#api call
	#a = Application_Details.objects.exclude(Status='BL')
	if request.method == "POST" and "Edit" in request.POST:
		appln_id = request.POST.get('Edit')
		print("Edit->",appln_id)
		Loan_app = Application_Details.objects.get(Application_ID=appln_id)
		Loan_app.Amount =request.POST.get("Amount")
		Loan_app.Tenure = request.POST.get("Tenure")
		Loan_app.Purpose = request.POST.get("Purpose")
		Loan_app.save()
		bd = Business_Details.objects.get(Application_ID=appln_id)
		bd.B_name = request.POST.get("BusinessName")
		bd.B_PAN = request.POST.get("BPAN")
		bd.B_contact = request.POST.get("Bmobile")
		bad=Business_Addr.objects.get(B_ID=bd.B_ID)
		bad.B_House_No = request.POST.get("HNO")
		bad.B_Street = request.POST.get("street")
		bad.B_Locality = request.POST.get("area")
		bad.B_City = request.POST.get("City")
		bad.B_PINCode = request.POST.get("pincode")
		bad.B_State = request.POST.get("state")
		bad.B_Country = request.POST.get("Country")
		bd.save()
		bad.save()
		cd=Applicant_Details.objects.get(Application_ID=appln_id)
		cd.Applicant_Name = request.POST.get("AName")
		cd.Applicant_Age = request.POST.get("AAge")
		cd.Applicant_Gender = request.POST.get("Agender")
		cd.Applicant_Mobile_No = request.POST.get("Amobile")
		cd.Applicant_Email = request.POST.get("Aemail")
		cad=Applicant_Addr.objects.get(Applicant_ID_id=cd.id)
		cad.A_House_No = request.POST.get("AHNO")
		cad.A_Street = request.POST.get("Astreet")
		cad.A_Locality = request.POST.get("Aarea")
		cad.A_City = request.POST.get("ACity")
		cad.A_PINCode = request.POST.get("Apincode")
		cad.A_State = request.POST.get("Astate")
		cad.A_Country = request.POST.get("Acountry")
		cd.save()
		cad.save()
		return redirect('CustomerDisplayApplications')

	data = {
		"table" : "application_details",
 		"status" : "BL"
	}
	res = requests.post(url = server_url, data = data)
	r = Parse(res.text)
	#print(r.data)
	a = r.data
	for app in a:
		a_detail = Applicant_Details.objects.filter(Application_ID=app['Application_ID']).values()[0]
		b_detail = Business_Details.objects.filter(Application_ID=app['Application_ID']).values('B_ID', 'B_name', 'B_PAN', 'B_contact')[0]
		a_addr = Applicant_Addr.objects.filter(id=a_detail['id']).values()[0]
		b_addr = Business_Addr.objects.filter(B_ID=b_detail['B_ID']).values()[0]
		app['applicant'] = a_detail
		app['business'] = b_detail
		app['a_addr'] = a_addr
		app['b_addr'] = b_addr
	#print(a)
	if request.method == "POST" and "Logout" in request.POST:
		 return redirect('Logout')
	return render(request,'CustomerDisplayApplications.html',{'applications': a})

@cs_not_loggedin
def CustomerDetails(request):
	request.session['path'] = 'CustomerDetails'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method == "POST" and "Logout" in request.POST:
		 return redirect('Logout')
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
		if app_details.Status == "CS" or app_details.Status == "D" or app_details.Status == "D" or app_details.Status[:1] == "E":
			return redirect('AlreadyVerified')
		app_details.Status = "CS"
		app_details.save()
		return redirect('ApplicationVerified')
	return render(request,'CustomerDetails.html',{'Application_Details':app_details,'Applicant_Details':a_detail,'Applicant_Addr':a_addr,'Business_Details':b_detail,'Business_Addr':b_addr})

@cs_not_loggedin
def AlreadyVerified(request):
	request.session['path'] = 'AlreadyVerified'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST":
		return redirect('CustomerDisplayApplications')
	print("hello")
	return render(request,'AlreadyVerified.html',{})

@cs_not_loggedin
def Reject(request):
	request.session['path'] = 'Reject'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CustomerDisplayApplications')
	return render(request,'Reject.html')

@cs_not_loggedin
def ApplicationVerified(request):
	request.session['path'] = 'ApplicationVerified'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CustomerDisplayApplications')
	return render(request,'ApplicationVerified.html')


@staff_not_loggedin
def Staff(request):
	request.session['path'] = 'Staff'
	if request.method == "POST" and "Edit" in request.POST:
		return redirect('transfer')
	elif request.method == "POST" and "View" in request.POST:
		return redirect('CSverifiedApplications')  
	elif request.method == "POST" and "Logout" in request.POST:
		return redirect('Logout')
	return render(request,'Staff.html',{})

@staff_not_loggedin
def CSverifiedApplications(request):
	#a = Application_Details.objects.filter(Status='CS')
	request.session['path'] = 'CSverifiedApplications'
	request.session.set_expiry(request.session.get_expiry_age())
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
	res = requests.post(url = server_url, data = data)
	r = Parse(res.text)
	print(r.data)
	a = r.data		
	return render(request,'CSverifiedApplications.html',{'applications': a})

@staff_not_loggedin
def DocumentsRejected(request):
	request.session['path'] = 'DocumentsRejected'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CSverifiedApplications')
	return render(request,'DocumentsRejected.html')

@staff_not_loggedin
def DocumentsVerified(request):
	request.session['path'] = 'DocumentsVerified'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('CSverifiedApplications')
	return render(request,'DocumentsVerified.html')

@manager_not_logedin
def Manager(request):
	request.session['path'] = 'Manager'
	if request.method == "POST" and "Edit" in request.POST:
		return redirect('transfer')
	elif request.method == "POST" and "View" in request.POST:
		return redirect('ManagerApplications')
	elif request.method == "POST" and "Logout" in request.POST:
		 return redirect('Logout')
	return render(request,'Manager.html',{})

@manager_not_logedin
def ManagerApplications(request):
	request.session['path'] = 'ManagerApplications'
	request.session.set_expiry(request.session.get_expiry_age())
	#api call
	#a = Application_Details.objects.filter(Status='DV')
	data = {
		"table" : "application_details",
 		"status" : "DV"
	}
	res = requests.post(url = server_url, data = data)
	r = Parse(res.text)
	print(r.data)
	a = r.data
	return render(request,'ManagerApplications.html',{'applications':a})

@manager_not_logedin
def ManagerApplicationDetails(request):
	request.session['path'] = 'ManagerApplicationDetails'
	request.session.set_expiry(request.session.get_expiry_age())
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
				t.Inv_ID = il.Inv_ID_id
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

@manager_not_logedin
def LoanApproved(request):
	request.session['path'] = 'LoanApproved'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('ManagerApplications')
	return render(request,'LoanApproved.html')

@manager_not_logedin
def ManagerReject(request):
	request.session['path'] = 'ManagerReject'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('ManagerApplications')
	return render(request,'ManagerReject.html')


@manager_not_logedin
def Blacklist(request):
	request.session['path'] = 'Blacklist'
	request.session.set_expiry(request.session.get_expiry_age())
	if request.method=="POST" and "view_apps" in request.POST:
		return redirect('ManagerApplications')
	return render(request,'Blacklist.html')


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