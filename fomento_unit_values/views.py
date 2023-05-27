from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Create your views here.
@api_view(['GET'])
def get_unit_values(request):
    fecha_str = request.GET.get('fecha')
    fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
    
    year = fecha.year
    month = fecha.month
    day = str(fecha.day).lstrip("0")

    url = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'
    headers = {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)

    month_name = get_month_name(month)

    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find("div", id=f"mes_{month_name}").find('table')
 
    fomento_unit_values = {}
    rows = table.find_all('tr')
    rows.pop(0)
    for row in rows:
        strong_elements = row.find_all('strong')

        for strong_element in strong_elements:
            unit_value_day = strong_element.text.strip()
            unit_value = strong_element.parent.find_next_sibling()

            if(unit_value):
                fomento_unit_values[unit_value_day] = unit_value.text
        
    return Response(fomento_unit_values[day])

def get_month_name(month):
    if month < 1 or month > 12:
        return "Número de mes inválido"
    
    month_names = [
        "enero", 
        "febrero", 
        "marzo", 
        "abril", 
        "mayo", 
        "junio",
        "julio", 
        "agosto", 
        "septiembre", 
        "octubre", 
        "noviembre", 
        "diciembre"
    ]
    
    return month_names[month - 1]