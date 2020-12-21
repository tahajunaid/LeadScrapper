from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests,sys,os
from subprocess import run,PIPE
def home(request):
    return render(request,'companies/dashboard.html')

def LinkedIn(request):
    return render(request,'companies/linkedIn.html')

def Crunchbase(request):
    return render(request,'companies/crunchbase.html')

def Tracxn(request):

    comp = request.POST.get('company','')

    return render(request,'companies/tracxn.html',{'company_name':comp})

def resultscrunchbase(request):
    inp = request.POST.get('company')
    #change the location to the backend scripts
    out = run([sys.executable,'..leadscrappers//backend scripts//crunchbase.py',inp],shell=True,stdout=PIPE)
    print(out)
    return render(request,'companies/resultscrunchbase.html',{'data':out.stdout})

def resultslinkedIn(request):
    inp1 = request.POST.get('skills')
    inp2 = request.POST.get('location')
    #change the location to the backend scripts
    out = run([sys.executable,'..leadscrappers//backend scripts//linkedin.py',inp1,inp2],shell=True,stdout=PIPE)
    print(out)
    return render(request,'companies/resultslinkedIn.html',{'data':out.stdout})

def resultstracxn(request):
    inp = request.POST.get('company')
    #change the location to the backend scripts
    out = run([sys.executable,'..leadscrappers//backend scripts//tracxn.py',inp],shell=True,stdout=PIPE)
    print(out)
    return render(request,'companies/resultstracxn.html',{'data':out.stdout})

