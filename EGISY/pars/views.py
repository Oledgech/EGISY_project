
import requests
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
import os
from django.http import HttpResponse
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from .models import Projects
import xlsxwriter
import csv
import pandas as pd
import time
import threading
import random
from datetime import datetime
import validators
from urllib.parse import urlparse, parse_qs
class ProjectsResource(resources.ModelResource):

    class Meta:
        model = Projects



def index(request):
    print(request)
    year = datetime.now().year
    num = 2016
    ye = []
    while num <= year:
        ye.append(num)
        num += 1
    projects = Projects.objects.all()
    c = Projects.objects.all().distinct().count()
    paginator = Paginator(projects, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if 'delete' in request.GET:
        number = 2016
        while number <= 2023:
            url = 'https://www.rosrid.ru/api/open-data?year=' + str(number) + '&month=all_months&card_type=nioktr'
            response = requests.get(url, verify=False)
            with open(str(number)+'.json', 'wb') as file:
                file.write(response.content)
            number += 1
    if 'button1' in request.POST:
        with open('2020.json', encoding='utf-8') as f:
            my_dict = json.load(f)
        for i in range(len(my_dict["cards"])):
            proj=Projects()
            proj.name=my_dict["cards"][i]['name']
            proj.registration_number = my_dict["cards"][i]['registration_number']
            proj.executor = my_dict["cards"][i]['executor']['short_name']
            proj.okogu = my_dict["cards"][i]['customer']['okogu']
            proj.customer = my_dict["cards"][i]["customer"]['short_name']
            if (my_dict["cards"][i]['budgets']):
                proj.budget_type = my_dict["cards"][i]['budgets'][0]['budget_type']
            else:
                proj.budget_type=''
            proj.nioktr_types= my_dict["cards"][i]['nioktr_types'][0]
            if (my_dict["cards"][i]['priority_directions']):
                proj.priority_directions= my_dict["cards"][i]['priority_directions'][0]
            else:
                proj.priority_directions=''
            if (my_dict["cards"][i]['critical_technologies']):
                proj.critical_technologies= my_dict["cards"][i]['critical_technologies'][0]
            else:
                proj.critical_technologies=''
            if (my_dict["cards"][i]['scientific_technology_priorities']):
                proj.scientific_technology_prioritie= my_dict["cards"][i]['scientific_technology_priorities'][0]
            else:
                proj.scientific_technology_prioritie=''
            proj.annotation = my_dict["cards"][i]['annotation']
            proj.start_date = my_dict["cards"][i]['start_date']
            proj.end_date = my_dict["cards"][i]['end_date']
            if (my_dict["cards"][i]['coexecutors']):
                proj.coexecutors = my_dict["cards"][i]['coexecutors'][0]['description']
            else:
                proj.coexecutors =''
            i += 1
            proj.save()
    return render(request, "pars/home.html",{'projects':projects,'page_obj': page_obj,'ye': ye,'c': c})

def search(request):
    search_query = request.GET.get('search', '')
    option_query = request.GET.get('type')
    string1='year'
    num = 2016
    ye = []
    proj=[]
    yet = []
    while num <= datetime.now().year:
        year_query = request.GET.get(string1+'_'+str(num))
        if(year_query):
            ye.append(year_query)
        yet.append(num)
        num += 1
    c=0
    if len(ye) == 0:
        projects = Projects.objects.filter((Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q(
            customer__icontains=search_query) | Q(executor__icontains=search_query)), Q(nioktr_types__icontains=option_query))
        proj.append(projects)
        paginator = Paginator(projects, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        c = Projects.objects.filter((
                    Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q(
                customer__icontains=search_query) | Q(executor__icontains=search_query)), Q(nioktr_types__icontains=option_query)).distinct().count()
    else:
        for i in ye:
            projects = Projects.objects.filter(Q(
                start_date__icontains=i),(Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q( customer__icontains=search_query) | Q(executor__icontains=search_query)), Q(nioktr_types__icontains=option_query))
            proj.append(projects)
            c+= Projects.objects.filter(Q(start_date__icontains=i),(Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q( customer__icontains=search_query) | Q(executor__icontains=search_query)), Q(nioktr_types__icontains=option_query)).distinct().count()
        xs = [None] * c
        paginator = Paginator( xs, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    template_name = "pars/search.html"
    return render(request, template_name,
                  {'page_obj': page_obj,'proj': proj,'ye':ye ,'c':c,'option_query':option_query,'search_query':search_query})
def export(request):
    search_query= request.GET.get('projects')
    option_projects = request.GET.get('option')
    year_projects = []
    string1 = 'year'
    num = 2016
    while num <= datetime.now().year:
        year_query = request.GET.get(string1 + '_' + str(num))
        if (year_query):
            year_projects.append(year_query)
        print(year_query)
        num += 1
    if len(year_projects) == 0:
        projects = Projects.objects.filter((Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q(
            customer__icontains=search_query) | Q(executor__icontains=search_query)),
                                           Q(nioktr_types__icontains=option_projects))
    else:
        projects = Projects.objects.filter((Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q(
            customer__icontains=search_query) | Q(executor__icontains=search_query)), Q(nioktr_types__icontains = option_projects),(Q(start_date__year__in= year_projects) ))
    person_resource = ProjectsResource()
    dataset = person_resource.export(projects)
    if 'Excel' in request.GET:
        response = HttpResponse(dataset.xls,content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;  filename="persons.xls"'
    if 'JSON' in request.GET:
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="persons.json"'
    if 'YAML' in request.GET:
        response = HttpResponse(dataset.yaml, content_type='application/yaml')
        response['Content-Disposition'] = 'attachment; filename="persons.yaml"'
    if 'CSV' in request.GET:
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response

def full(request):
    id_query = request.GET.get('id')

    projects = Projects.objects.filter(Q(id=id_query) )
    return render(request, "pars/full_display.html", {'projects': projects})
def year(request):
    year_query = request.GET.get('year')

    projects = Projects.objects.filter(Q(start_date__icontains=year_query) )
    paginator = Paginator(projects, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "pars/home.html", {'page_obj': page_obj, "year_query":year_query})

delay = 10 #время между вызовами функции в секундах, в данном примере - сутки

def do_something(): #вызываемая в отдельном потоке функция в ней и производим действия из следующего шага
    number = datetime.now().year
    if os.path.isfile(str(number) + '.json'):
        print("Файл существует")
    else:
        url = 'https://www.rosrid.ru/api/open-data?year=' + str(number) + '&month=all_months&card_type=nioktr'
        if os.path.isfile(url):
            response = requests.get(url, verify=False)
            with open(str(number) + '.json', 'wb') as file:
                    file.write(response.content)
            with open(str(number) + '.json', encoding='utf-8') as f:
                my_dict = json.load(f)
            for i in range(len(my_dict["cards"])):
                proj = Projects()
                proj.name = my_dict["cards"][i]['name']
                proj.registration_number = my_dict["cards"][i]['registration_number']
                proj.executor = my_dict["cards"][i]['executor']['short_name']
                proj.okogu = my_dict["cards"][i]['customer']['okogu']
                proj.customer = my_dict["cards"][i]["customer"]['short_name']
                if (my_dict["cards"][i]['budgets']):
                    proj.budget_type = my_dict["cards"][i]['budgets'][0]['budget_type']
                else:
                    proj.budget_type = ''
                proj.nioktr_types = my_dict["cards"][i]['nioktr_types'][0]
                if (my_dict["cards"][i]['priority_directions']):
                    proj.priority_directions = my_dict["cards"][i]['priority_directions'][0]
                else:
                    proj.priority_directions = ''
                if (my_dict["cards"][i]['critical_technologies']):
                    proj.critical_technologies = my_dict["cards"][i]['critical_technologies'][0]
                else:
                    proj.critical_technologies = ''
                if (my_dict["cards"][i]['scientific_technology_priorities']):
                    proj.scientific_technology_prioritie = my_dict["cards"][i]['scientific_technology_priorities'][0]
                else:
                    proj.scientific_technology_prioritie = ''
                proj.annotation = my_dict["cards"][i]['annotation']
                proj.start_date = my_dict["cards"][i]['start_date']
                proj.end_date = my_dict["cards"][i]['end_date']
                if (my_dict["cards"][i]['coexecutors']):
                    proj.coexecutors = my_dict["cards"][i]['coexecutors'][0]['description']
                else:
                    proj.coexecutors = ''
                i += 1
                proj.save()
        else:
            print("Файл не существует")
s=0
while True:
    time.sleep(delay)
    thread = threading.Thread(target=do_something)
    thread.start()
    s+=1
    if s==1:
        s=0
        break
