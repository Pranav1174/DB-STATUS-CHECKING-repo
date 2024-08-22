from django.http import JsonResponse
import os
import json

def get_db_status(request):
    json_file_path = os.path.join(os.path.dirname(__file__), '../db_status.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    return JsonResponse(data)
