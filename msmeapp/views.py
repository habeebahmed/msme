from django.shortcuts import render,redirect
import random
import requests
import json
from datetime import datetime
# Create your views here.
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import smtplib
from django.core.mail import EmailMessage,send_mail
from .models import *
from django.template.loader import render_to_string, get_template
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from .decorator import *
template_html = '../templates/email.html'

#Application_Details
def Loan(request):
	if request.method=="POST":
		# for key, value in request.POST.items():
   		# 	print('Key: %s' % (key) ) 
   		# 	# print(f'Key: {key}') in Python >= 3.7
   		# 	print('Value %s' % (value) )
		Loan_app = Application_Details()
		app = "APP"+str(random.randint(0,100))
		Loan_app.Application_ID = app
		Loan_app.Amount =request.POST.get("Amount")
		Loan_app.Tenure = request.POST.get("Tenure")
		Loan_app.Date_Application = datetime.now()
		Loan_app.Purpose = request.POST.get("Purpose")
		Loan_app.Frequency = request.POST.get("Frequency")
		Loan_app.Status = "IP"
		request.session['Loan'] = {
			'amt': request.POST.get("Amount"),
			'tenure': request.POST.get("Tenure"),
			'purpose': request.POST.get("Purpose"),
			'frequency': request.POST.get("Frequency")
		}
		Loan_app.Pages = 1
		Loan_app.save()
		request.session['app'] = app
		request.session['page'] = [1]
		return redirect('Business')
	if 'Loan' in request.session:
		Loan = request.session['Loan']
		return render(request,'LoanDetails.html',{'Loan':Loan})
	Loan= {
		'amt': '30000',
		'tenure': '12',
		'purpose': 'A',
		'frequency': '3'
	}
	return render(request,'LoanDetails.html',{'Loan':Loan})

#Business_Details
@user_progress(current_page=2)
def Business(request):
	if request.method=="POST":
		bd=Business_Details()
		bid = "BUS"+str(random.randint(0,100))
		bd.B_ID = bid
		app_id = Application_Details.objects.get(Application_ID=request.session['app'])
		bd.Application_ID = app_id
		bd.B_Type = request.POST.get("BusinessType")
		bd.B_name = request.POST.get("BusinessName")
		bd.B_PAN = request.POST.get("BPAN")
		bd.B_contact = request.POST.get("Bmobile")
		bd.B_Estb = request.POST.get("B_est")
		request.session['bid'] = bid
		bad=Business_Addr()
		bad.B_ID = bd
		bad.B_House_No = request.POST.get("HNO")
		bad.B_Street = request.POST.get("street")
		bad.B_Locality = request.POST.get("area")
		bad.B_City = request.POST.get("City")
		bad.B_PINCode = request.POST.get("pincode")
		bad.B_State = request.POST.get("state")
		bad.B_Country = request.POST.get("Country")
		request.session['business'] = {
			'B_Type':request.POST.get("BusinessType"),
			'B_name':request.POST.get("BusinessName"),
			'B_PAN':request.POST.get("BPAN"),
			'B_contact':request.POST.get("Bmobile"),
			'B_Estb':request.POST.get("B_est"),
			'B_House_No':request.POST.get("HNO"),
			'B_Street':request.POST.get("street"),
			'B_Locality':request.POST.get("area"),
			'B_City':request.POST.get("City"),
			'B_PINCode':request.POST.get("pincode"),
			'B_State':request.POST.get("state"),
			'B_Country':request.POST.get("Country")
		}
		app_id.Pages = 2
		app_id.save()
		bd.save()
		bad.save()
		request.session['page'] += [2]
		return redirect('Contact')
	if 'business' in request.session:
		business = request.session['business']
		print(business)
		return render(request,'BusinessDetails.html',{'business':business})
	return render(request,'BusinessDetails.html',{})

#Applicant_Details
@user_progress(current_page=3)
def Contact(request):
	if request.method=="POST":
		cd=Applicant_Details()
		pan1 = request.POST.get("pan")
		pan2 = Applicant_Details.objects.filter(Applicant_PAN=pan1)
		if pan2:
			cd.Applicant_ID = pan2[0].Applicant_ID
			app_id = pan2[0].Applicant_ID
		else:
			app_id = "APP"+str(random.randint(100,999))
			cd.Applicant_ID = app_id
		
		app_id = Application_Details.objects.get(Application_ID=request.session['app'])
		cd.Application_ID = app_id
		cd.B_ID = Business_Details.objects.get(B_ID=request.session['bid'])
		n = request.POST.get("Name")
		cd.Applicant_Name = n
		cd.Applicant_Age = request.POST.get("Age")
		cd.Applicant_Gender = request.POST.get("gender")
		cd.Applicant_Mobile_No = request.POST.get("mobile")
		a_email = request.POST.get("email")
		cd.Applicant_Email = a_email
		cd.Applicant_PAN = pan1
		cd.save()
		cad=Applicant_Addr()
		cad.Applicant_ID = cd
		cad.A_House_No = request.POST.get("HNO")
		cad.A_Street = request.POST.get("street")
		cad.A_Locality = request.POST.get("area")
		cad.A_City = request.POST.get("City")
		cad.A_PINCode = request.POST.get("pincode")
		cad.A_State = request.POST.get("state")
		cad.A_Country = request.POST.get("country")
		cad.save()
		request.session['app_id']=app_id.Application_ID
		request.session['email']=a_email
		request.session['name']=n
		request.session['page'] += [3]
		app_id.Pages = 3
		app_id.save()
		return redirect('Financial')
	return render(request,'ContactDetails.html',{})

#Financials
@user_progress(current_page=4)
def Financial(request):
	if request.method=="POST":
		a = Assets()
		a.Assets_ID = "A"+str(random.randint(100,999))
		a.Fixed_Assets = request.POST.get("Fixed_Assets")
		a.Intangible_Assets = request.POST.get("Intangible_Assets")
		a.Current_Assets = request.POST.get("Current_Assets")
		a.Non_Current_Assets = request.POST.get("Non_Current_Assets")
		a.save()

		c = Capital()
		c.Capital_ID = "C"+str(random.randint(100,999))
		c.Issued_Capital = request.POST.get("Issued_Capital")
		c.Paid_Up_Capital = request.POST.get("Paid_Up_Capital")
		c.save()


		l = Liabilities()
		l.Liabilities_ID = "L"+str(random.randint(100,999))
		l.Term_Liabilities = request.POST.get("Term_Liabilities")
		l.Current_Liabilities = request.POST.get("Current_Liabilities")
		l.save()

		cf = Cash_Flows()
		cf.Cash_Flows_ID = "CF"+str(random.randint(100,999))
		cf.Operations_Activities = request.POST.get("Operations_Activities")
		cf.Investing_Activities = request.POST.get("Investing_Activities")
		cf.Financing_Activities = request.POST.get("Financing_Activities")
		cf.save()


		r = Reserves()
		r.Reserves_ID = "R"+str(random.randint(100,999))
		r.Subsidy_Gov = request.POST.get("Subsidy_Gov")
		r.General_Reserves = request.POST.get("General_Reserves")
		r.save()


		fin = Financials()
		fin.Financial_ID = "fin"+str(random.randint(100,999))
		fin.B_ID = Business_Details.objects.get(B_ID=request.session['bid'])
		appln_id2 =  Application_Details.objects.get(Application_ID=request.session['app'])
		fin.Application_ID = appln_id2
		fin.Assets_ID = a
		fin.Capital_ID = c
		fin.Liabilities_ID = l
		fin.Cash_Flows_ID = cf
		fin.Reserves_ID = r
		fin.save()

		app_id = request.session['app_id']
		x=[]
		app = request.session['app']
		appln = Applicant_Details.objects.filter(Applicant_ID=app_id)
		for ap in appln:
			x.append(ap.Application_ID.Application_ID)
		flag=0
		x.remove(app)
		for i in x:
			appln_id = Application_Details.objects.get(Application_ID=i)
			if appln_id.Status != 'RP':
				flag = 1
				break
			else:
				continue
		if flag != 0:
			return HttpResponse("Your previous loan applications are payment due. Kindly retry after paying your due amounts.")
		else:
			pass
		blacklist = Blacklisted.objects.filter(Applicant_ID=app_id)
		if blacklist:
			app = request.session['app']
			a = Application_Details.objects.get(Application_ID=app)
			a.Status = 'BL'
			a.save()
			return HttpResponse("Your Application has been Blacklisted")
		else:
			app_id2.Pages = 4
			app_id2.save()
			request.session['page'] += [4]
			return redirect('Documents')
		
	else:
		return render(request,'FinancialDetails.html',{}) 

@user_progress(current_page=5)
def Documents(request):
	if request.method=="POST":
		fs = FileSystemStorage()
		KTP = request.FILES['KTP']
		fs.save(KTP.name,KTP)
		FamilyCard = request.FILES['Family_Card']
		fs.save(FamilyCard.name,FamilyCard)
		NPWP = request.FILES['NPWP']
		fs.save(NPWP.name,NPWP)
		bs = request.FILES['Bank_Statment']
		fs.save(bs.name,bs)
		appln_id =  Application_Details.objects.get(Application_ID=request.session['app'])
		a_email1 = request.session['email']
		n = request.session['name']
		app = request.session['app']
		mail_subject="Loan Application Received"
		message="Hello" + n + ". We have received your loan application. It is forwarded to our manual verification team and you can expect a decision within 3 working days. Your application ID is "+app+". Keep this ID for reference.     Thank you."
		email=send_mail(mail_subject,message,'',[a_email1],fail_silently=False)
		request.session['page'] += [5]
		print(request.session['page'])
		del request.session['page']
		app_id.Pages = 5
		app_id.save()
		return render(request,'Appln_submission_success.html',{})
	return render(request,'Documents.html',{})

def LoginUser(request):
	if request.method=="POST":
		Aid1 = request.POST.get("aid")
		try:	
			auid = User_Credentials.objects.get(User_ID=Aid1)
		except User_Credentials.DoesNotExist:
			return HttpResponse(Aid1+" does not exist")
		pass1 = request.POST.get("password")
		t=1
		for u in User_Credentials.objects.all():
			if(u.User_ID==Aid1 and u.Password==pass1):
				t=0
				break
		if(t==0):
			request.session['a']=Aid1
			return redirect('DashBoard1')
		else:
			return HttpResponse("invalid username and password")

	else:
		return render(request,'LoginUser.html',{})

@user_not_loggedin
def DashBoard1(request):
	# if request.method == "POST":
	# 	applicant = Applicant_Details.objects.filter(Applicant_ID=Aid1)
	# if request.method == "POST":
	if request.method=="POST" and "Logout" in request.POST:
		request.session.clear()
		print("Loggedout")
		return redirect('LoginUser')
	Aid1 = request.session['a']
	application = []
	details = []
	#notdisbursed = []
	#disbursed = []
	#total =[]
	appl = Applicant_Details.objects.filter(Applicant_ID=Aid1)
	for i in appl:
		print(i)
		try:
			db = Disbursed_appl.objects.get(Application_ID_id=i.Application_ID_id)
			application.append(db)
			install = Installments.objects.filter(Application_ID=i.Application_ID_id,Payment_Date=None).order_by('DueDate').first()
		except:
			pass
	print(application)
	if request.method=="POST" and "Pay" in request.POST:
		appln_id = request.POST.get('appln_id')
		amt = 0
		b=0
		si=0
		if request.POST.get('paytype') == 'A':
			install = Installments.objects.filter(Application_ID=appln_id,Payment_Date=None).order_by('DueDate')
			install2 = install.first()
			install2.Link = True
			install2.Link_Time = datetime.now()
			for inst in install:
				amt += inst.Total_Amount
				b += inst.Base_Amount
				si += inst.S_Interest
			install2.Base_Amount = b
			install2.S_Interest = si
			install2.Total_Amount = amt 
			install2.save()
			Installments.objects.filter(Application_ID=appln_id,Payment_Date=None,Link=0).delete()

			html_content = render_to_string(template_html, {"link": 'http://127.0.0.1:8000/Payment?appln_id='+appln_id, "amount":amt})
		#emi
		elif request.POST.get('paytype') == 'B':
			install = Installments.objects.filter(Application_ID=appln_id,Payment_Date=None).order_by('DueDate').first()
			install.Link = True
			install.Link_Time = datetime.now()
			amt = install.Total_Amount	
			install.save()
			html_content = render_to_string(template_html, {"link": 'http://127.0.0.1:8000/Payment?appln_id='+appln_id, "amount":amt})
	#update DB based on payment method selection in installments table and send a mail with link to payment portal
	#database code
	# install = Installments.objects.filter(Application_ID=appln_id).order_by('DueDate')
	# install2 = install.filter(Payment_Date=None).first()
	# install2.Link = True
	# install2.Link_Time = timezone.localtime(timezone.now())	
	# install2.save()
		applicant = Applicant_Details.objects.get(Application_ID=appln_id)
		print(applicant.Applicant_Email)
		send_mail(
			'Payment Link',
			'Click the link to go to Payment portal',
			'',
			[applicant.Applicant_Email],
			fail_silently=False,
			html_message=html_content
		)
		return HttpResponse("Payment Link has been sent to your mail "+appln_id)
	

	return render(request,'DashBoard1.html',{"application": application})

@user_not_loggedin
def Payment(request):
	if request.GET.get('appln_id') and request.method !="POST" :
		print("In GET")
		#payment portal
		# appln_id = request.POST.get('appln_id')
		# approve = Approved_Appln.objects.get(Application_ID=appln_id)
		appln_id = request.GET.get('appln_id')
		install = Installments.objects.filter(Application_ID=appln_id).order_by('DueDate')
		install2 = install.filter(Payment_Date=None).first()
		if(install2.Link_Time == False):
			return HttpResponse('Invalid Link')
		y = install2.Link_Time
		#x = timezone.localtime(timezone.now())
		x = datetime.now()
		z = x-y
		a = install2.DueDate
		b = date.today()-a
		# print(x)
		# print(y)
		print(z)
		if(z.days >= 1 ):
			install2.Link = False
			install2.save()
			return HttpResponse('Invalid Link')
		elif(b.days<=3):
			return render(request,'Payment.html',{'application': install2,'Total_Amount':install2.Total_Amount})
		elif(b.days>3):
			# c = ((1.07185903129)**((b.days)/365))*(install2.Base_Amount)
			print(b.days)
			d = b.days-3
			p=(1+(0.01/365))
			p=p**(365*(d*0.00273973))
			ci = p*install2.Total_Amount
			t = ci + install2.Total_Amount + 100
			# c = install2.Total_Amount + ( install2.Total_Amount * ( (b.days-3)/100 ) )
			return render(request,'Payment.html',{'application': install2,'Total_Amount': t})
		else:
			return HttpResponse('Technical Issue!!!')
	if request.method=="POST" and "Pay" in request.POST:
		appln_id = request.POST.get('application')
		install = Installments.objects.filter(Application_ID=appln_id,Payment_Date=None).order_by('DueDate').first()
		install.Payment_Date = date.today()
		Base = install.Base_Amount
		Trans = Transactions.objects.get(Application_ID_id=appln_id)
		in_id = Trans.Inv_ID
		investor = Investor_lending.objects.get(Inv_ID_id=in_id)
		investor.Amount_available += Base
		amount = (install.Total_Amount-Base)*0.3
		inv_earning = Investor_earnings.objects.filter(Inv_ID_id=in_id).first()
		if inv_earning is not None:
			inv_earning.earnings += amount
		else:
			inv_earning = Investor_earnings()
			inv_earning.earnings = amount
			inv_earning.Inv_ID_id = in_id
		inv_earning.save()
		investor.Amount_available += amount
		investor.save()
		install.save()
		install2 = Installments.objects.filter(Application_ID=appln_id,Payment_Date=None).order_by('DueDate')
		if len(install2) == 0:
			Disbursed_appl.objects.filter(Application_ID=appln_id).delete()
			a = Application_Details.objects.get(Application_ID=appln_id)
			a.Status = 'RP'
			a.save()
		else:
			install = Installments.objects.filter(Application_ID=appln_id)
			install2 = install.exclude(Payment_Date=None)
			s = 'E'+str(len(install2))
			aa = Application_Details.objects.get(Application_ID=appln_id)
			aa.Status = s
			aa.save()
		return HttpResponse('Payment Successfull')