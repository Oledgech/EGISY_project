
import requests
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
import json
from django.http import HttpResponse
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from .models import Projects

class ProjectsResource(resources.ModelResource):
    class Meta:
        model = Projects

def index(request):
    print(request)
    search_query=request.GET.get('search','')
    if search_query:
        projects = Projects.objects.filter(Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q(customer__icontains=search_query) | Q(executor__icontains=search_query))

    else:
        projects = Projects.objects.all()
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
        proj=Projects()
        i = 1
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

    return render(request, "pars/home.html",{'projects':projects,'search_query':search_query,'page_obj': page_obj,})

def export(request):
    search_query = request.GET.get('search', '')
    if search_query:
        projects = Projects.objects.filter(Q(name__icontains=search_query) | Q(annotation__icontains=search_query) | Q(
            customer__icontains=search_query) | Q(executor__icontains=search_query))
    else:
            projects = Projects.objects.all()
    person_resource = ProjectsResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'

    return response



