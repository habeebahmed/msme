from django.db import models
# Create your models here.
from django.forms import forms
from datetime import datetime

#Main (Applicant_ID(PK), Application_ID (FK) , B_ID (FK))
#class Main(models.Model):
#	Applicant_ID = models.AutoField(primary_key=True)
#	Application_ID = models.ForeignKey(Application_Details, on_delete=models.CASCADE)
#	B_ID = models.ForeignKey(Business_Details,on_delete=models.CASCADE)

#Application_Details (Application_ID (PK), Applicant_ID (FK), Amount, Tenure, Date_Application, purpose, frequency,status) #Loan Details
class Application_Details(models.Model):#Loan
    Application_ID = models.CharField(primary_key=True,max_length=10)
    #Applicant_ID=models.ForeignKey(Applicant_Details, on_delete=models.CASCADE)
    Amount=models.FloatField(default=None)
    Tenure=models.IntegerField(default=0)
    Date_Application=models.DateTimeField(default=datetime.now)
    Purpose = models.TextField(max_length=1)
    Frequency=models.IntegerField(default=0)
    Status=models.CharField(max_length=3)
    
#Business_Details ( B_ID (PK), Applicant_ID(FK), B_Type, B_name,B_PAN, B_contact, B_Addr, B_Estb,  )
class Business_Details(models.Model):
	B_ID = models.CharField(primary_key=True,max_length=10)
	Application_ID = models.ForeignKey(Application_Details, on_delete=models.CASCADE)
	B_Type = models.CharField(max_length=20)
	B_name = models.TextField(max_length=30)
	B_PAN = models.CharField(max_length=10)
	B_contact = models.BigIntegerField(default=0)
	#B_Addr = models.TextField()
	B_Estb = models.DateField(default=datetime.now)

#Applicant_Details (Applicant_ID(PK), Applicant_Name, Applicant_Age, Applicant_Gender, Applicant_Mobile_No., Applicant_Email ID, Applicant_PAN, A_Addr)
class Applicant_Details(models.Model):
	Applicant_ID = models.CharField(max_length=10)
	Application_ID=models.ForeignKey(Application_Details, on_delete=models.CASCADE)
	B_ID=models.ForeignKey(Business_Details, on_delete=models.CASCADE)
	Applicant_Name = models.CharField(max_length=30)
	Applicant_Age = models.IntegerField(default=0)
	Applicant_Gender = models.CharField(max_length=1)
	Applicant_Mobile_No = models.BigIntegerField(default=0)
	Applicant_Email = models.EmailField(default=None)
	Applicant_PAN = models.CharField(max_length=10)
    #Applicant_addr = models.TextField()


#Applicant_Addr (Applicant_Addr_ID (PK), Applicant_ID (FK), A_House_No., A_Street, A_Locality, A_City, A_PINCode, A_State, A_Country)
class Applicant_Addr(models.Model):
	Applicant_ID = models.ForeignKey(Applicant_Details, on_delete=models.CASCADE)
	A_House_No = models.CharField(max_length=10, default='0000')
	A_Street = models.CharField(max_length=15, default='0000')
	A_Locality = models.CharField(max_length=15, default='0000')
	A_City = models.CharField(max_length=15)
	A_PINCode = models.IntegerField(default= 000000)
	A_State = models.CharField(max_length=15)
	A_Country = models.CharField(max_length=15)

#Business_addr (Business_Addr_ID (PK), Applicant_ID (FK), B_House_No., B_Street, B_Locality, B_City, B_PINCode, B_State, B_Country)
class Business_Addr(models.Model):
	B_ID = models.ForeignKey(Business_Details,on_delete=models.CASCADE)
	B_House_No = models.CharField(max_length=10,default='0000')
	B_Street = models.CharField(max_length=15, default='0000')
	B_Locality = models.CharField(max_length=15, default='0000')
	B_City = models.CharField(max_length=15)
	B_PINCode = models.IntegerField(default=0000)
	B_State = models.CharField(max_length=15)
	B_Country = models.CharField(max_length=15)



class Approved_Appln(models.Model):
    Application_ID=models.ForeignKey(Application_Details, on_delete=models.CASCADE)
    Amount=models.FloatField(default=0)
    Tenure=models.IntegerField(default=0)
    Status=models.CharField(max_length=2)
    DueDate=models.DateField(default=datetime.now)
    #Approved_appl (Application_ID (FK),Amount,Tenure, Status, DueDate)    


class Assets(models.Model):
    Assets_ID=models.CharField(max_length=10,primary_key=True)
    #Financial_ID=models.ForeignKey(Financials, on_delete=models.CASCADE)
    Fixed_Assets=models.FloatField(default=0)
    Intangible_Assets=models.FloatField(default=0)
    Current_Assets=models.FloatField(default=0)
    Non_Current_Assets=models.FloatField(default=0)
    #10)    Assets (Asset_ID (PK), Financial_ID(FK), Fixed_Assets, Intangible_Assets, Non_Current_Assets, Current_Assets)
	
#11) Capital(Capital_ID(PK),Financial_ID(FK), Issued_Capital, Paid_Up_Capital)
class Capital(models.Model):
    Capital_ID = models.CharField(max_length=10,primary_key=True)
    #Financial_ID = models.ForeignKey(Financials, on_delete=models.CASCADE)
    Issued_Capital = models.FloatField(default=0)
    Paid_Up_Capital = models.FloatField(default=0)

#12) Liabilities (Liabilities_ID(PK), Financial_ID(FK), Term_Liabilities, Current_Liabilities)
class Liabilities(models.Model):
    Liabilities_ID = models.CharField(max_length=10,primary_key=True)
    #Financial_ID = models.ForeignKey(Financials, on_delete=models.CASCADE)
    Term_Liabilities = models.FloatField(default=0)
    Current_Liabilities = models.FloatField(default=0)

#13) Cash_Flows (Cash_Flows_ID(PK), Financial_ID(FK), Operations_Activities, Investing_Activities, Financing_Activities)
class Cash_Flows(models.Model):
    Cash_Flows_ID = models.CharField(max_length=10,primary_key=True)
    #Financial_ID = models.ForeignKey(Financials, on_delete=models.CASCADE)
    Operations_Activities = models.FloatField(default=0)
    Investing_Activities = models.FloatField(default=0)
    Financing_Activities = models.FloatField(default=0)

#14) Reserves (Reserves_ID(PK), Financial_ID(FK), Subsidy_Gov, General_Reserves)
class Reserves(models.Model):
    Reserves_ID = models.CharField(max_length=10,primary_key=True)
    #Financial_ID = models.ForeignKey(Financials, on_delete=models.CASCADE)
    Subsidy_Gov = models.FloatField(default=0)
    General_Reserves = models.FloatField(default=0)

class Financials(models.Model):
    Financial_ID=models.CharField(max_length=10,primary_key=True)
    B_ID=models.ForeignKey(Business_Details, on_delete=models.CASCADE)
    Application_ID=models.ForeignKey(Application_Details, on_delete=models.CASCADE)
    Assets_ID=models.ForeignKey(Assets, on_delete=models.CASCADE)
    Capital_ID=models.ForeignKey(Capital, on_delete=models.CASCADE)
    Liabilities_ID=models.ForeignKey(Liabilities, on_delete=models.CASCADE)
    Cash_Flows_ID=models.ForeignKey(Cash_Flows, on_delete=models.CASCADE)
    Reserves_ID=models.ForeignKey(Reserves, on_delete=models.CASCADE)
#Financials ( Financial_Id (PK), B_ID (FK), Application_Id (FK))



#15) Blacklisted (Applicant_ID (FK), B_ID (FK), )
class Blacklisted(models.Model):
    Applicant_ID = models.CharField(max_length=10)
    B_ID = models.ForeignKey(Business_Details, on_delete=models.CASCADE)

class Documents(models.Model):
    Applicant_ID =models.ForeignKey(Applicant_Details , on_delete=models.CASCADE)
    Application_ID =models.ForeignKey(Application_Details , on_delete=models.CASCADE)
    KTP = models.TextField(default=None)
    Family_Card = models.TextField(default=None)
    Company_Estb_Details = models.TextField(default=None)
    NPWP = models.TextField(default=None)
    Bank_Statement = models.TextField(default=None)

#Reject_reason ( Reason_code(PK), Reason)
class Reject_reason(models.Model):
    Reason_code = models.CharField(primary_key=True, max_length=1)
    Reason = models.TextField()

class App_Rejected(models.Model):
    Application_ID=models.ForeignKey(Application_Details, on_delete=models.CASCADE)
    B_ID=models.ForeignKey(Business_Details, on_delete=models.CASCADE)
    Reason_code = models.ForeignKey(Reject_reason, on_delete=models.CASCADE)
#App_Rejected (Application_ID(FK), B_ID (FK), Reason_code)

#Investor_main (Inv_ID(PK), Amount_Invested, Date_Investment_Initial, Date_Last_Cumulative)
class Investor_main(models.Model):
    Inv_ID = models.CharField(primary_key=True,max_length=10)
    Amount_Invested = models.FloatField()
    Date_Investment_Initial = models.DateTimeField(default=datetime.now)
    Date_Last_Cumulative = models.DateTimeField(default=datetime.now)

#Investor_lending (Inv_ID(PK), Amount_available, Amount_deducted, Corresponding_Appl_ID), mapping table
class Investor_lending(models.Model):
    Inv_ID = models.ForeignKey(Investor_main, on_delete=models.CASCADE)
    Amount_available = models.FloatField(default=0)
    Last_Update = models.DateTimeField(default=datetime.now)

#Disbursed_appl (Application_ID(FK), Amount, Disbursed_date, Due_date, S_Interest, Current_date)
class Disbursed_appl(models.Model):
    Application_ID = models.ForeignKey(Application_Details , on_delete=models.CASCADE)
    Amount = models.FloatField(default=0)
    Disbursed_date = models.DateField(default=datetime.now)
    Due_date = models.DateField(default=datetime.now)
    S_Interest = models.FloatField(default=0)
    Due_Amount = models.FloatField(default=0)

#Investor_earnings (Inv_ID(PK), earnings)
class Investor_earnings(models.Model):
    Inv_ID = models.ForeignKey(Investor_main , on_delete=models.CASCADE)
    earnings = models.FloatField(default=0)

#UTEmployee (Emp_ID(PK), password)
class UTEmployee(models.Model):
    Emp_ID = models.CharField(primary_key=True,max_length=10)
    password = models.CharField(max_length=15)

#Transactions (Application_ID(FK), Inv_ID(FK))
class Transactions(models.Model):
    Application_ID = models.ForeignKey(Application_Details, on_delete=models.CASCADE)
    Inv_ID = models.CharField(max_length=10)

#User_Credentials (User_ID(pk), Password)
class User_Credentials(models.Model):
    User_ID = models.CharField(primary_key=True,max_length=10)
    Password = models.CharField(max_length=10)
#Installments
class Installments(models.Model):
   Application_ID = models.ForeignKey(Application_Details , on_delete=models.CASCADE)
   DueDate = models.DateField(default=datetime.now)
   Payment_Date = models.DateField(blank=True, null=True)
   Base_Amount = models.FloatField(default=0)
   S_Interest = models.FloatField(default=0)
   Total_Amount = models.FloatField(default=0)
   Link=models.BooleanField(default=False,blank=True)
   Link_Time = models.DateTimeField(null=True,blank=True)