from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

def diff_dates(date1, date2):
    return abs(date2-date1).days

def home(request):
    return render(request, 'home.html')

def settled(request):
    return render(request, 'settled.html')

def calculator(request):
    Settled = False
    Amount_At_Issue = float(request.GET['Amount'])
    Date_Original = request.GET['Date Summons and Complaint Filed']
    Date_Original = Date_Original.split('-')
    Date_Original = [int(x) for x in Date_Original]
    DSCF = date(Date_Original[0],Date_Original[1],Date_Original[2])
    if 'Date Settled' in request.GET:
        Date_Settled = request.GET['Date Settled']
        Date_Settled = Date_Settled.split('-')
        Date_Settled = [int(x) for x in Date_Settled]
        Date_Settled = date(Date_Settled[0],Date_Settled[1],Date_Settled[2])
        Settled = True


    #Terms of Settlement
    Principal = float(request.GET['Principal'])/100
    Interest = float(request.GET['Interest'])/100
    #Variables
    Var = 0.02/30
    if Settled:
        DiffDates = diff_dates(Date_Settled,DSCF)
    else:
        DiffDates = diff_dates(date.today(),DSCF)
    #If Calculated from Settled
    PrincipalOut = round(Principal * Amount_At_Issue,2)
    InterestSettledAmount = round((DiffDates * Var * PrincipalOut) * Interest,2)
    Attorney_Fee_Settled =  round((PrincipalOut + InterestSettledAmount)/5,2)
    #Costs = Ask PLaintiff

    #Calculated from Amount at Issue
    InterestAmountAtIssue = round((DiffDates * Var * Amount_At_Issue) * Interest,2)
    Attorney_Fee_AAI = round((Amount_At_Issue + InterestAmountAtIssue)/5,2)

    return render(request, 'calculator.html', {'PrincipalOut':PrincipalOut, 'InterestSettledAmount':InterestSettledAmount, 
        'Attorney_Fee_Settled': Attorney_Fee_Settled, 'InterestAmountAtIssue':InterestAmountAtIssue, 
        'Attorney_Fee_AAI':Attorney_Fee_AAI})

def about(request):
    return render(request, 'about.html')
   