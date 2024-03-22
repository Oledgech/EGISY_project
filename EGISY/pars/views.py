from django.http import HttpResponse
import requests

def index(request):
    print(request)
    if request.GET:
        number = 2016
        while number <= 2023:
            url = 'https://www.rosrid.ru/api/open-data?year=' + str(number) + '&month=all_months&card_type=nioktr'
            response = requests.get(url, verify=False)
            with open(str(number)+'.json', 'wb') as file:
                file.write(response.content)
            number += 1

    data={
        'title':'Тест',
    }
    return render(request, "pars/home.html",data)


from django.shortcuts import render

# Create your views here.
