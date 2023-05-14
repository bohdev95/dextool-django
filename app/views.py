from .utils import *
from django.db.models import F
from django.db.models import Subquery
from django.shortcuts import render
import csv
from django.utils.timezone import make_aware
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view



def index(request):

    project_list = Projects.objects.filter(status=1).values()

    return render(request, 'index.html', {'projects': project_list})
@api_view(['POST'])
def add_project(request):
    name = request.data['name']
    file_name = request.data['file_name']
    download_url = request.data['download_url']
    status = 1

    processed_data = Projects.objects.create(
        name = name,
        file_name = file_name,
        download_url = download_url,
        status = 1
    )
    processed_data.save()

    id = Projects.objects.latest('id').id

    return Response({"id":id})

@api_view(['POST'])
def get_project(request):
    project_id = request.data['project_id']
    latest_timestamp = Data.objects.filter(project_id=project_id).latest('timestamp').timestamp
    data = Data.objects.filter(timestamp=latest_timestamp, project_id=project_id).values()

    prev_date = datetime.datetime.now() - datetime.timedelta(1)
    prev_ttt = prev_date.strftime("%Y-%m-%d")
    prev_data = Data.objects.filter(timestamp=prev_ttt, project_id=project_id).values()

    print(latest_timestamp)
    print(prev_ttt)

    return Response({'data':data, 'prev_data': prev_data})


