import os
import json
from datetime import datetime, timedelta
from django.http import JsonResponse

def get_db_status(request):
    json_file_path = os.path.join(os.path.dirname(__file__), 'db_status.json')

    frame = request.GET.get('frame', None)

    now = datetime.now()
    if frame == '24H':
        start_time = now - timedelta(hours=24)
    elif frame == '1WK':
        start_time = now - timedelta(weeks=1)
    elif frame == '1MO':
        start_time = now - timedelta(days=30)
    else:
        return JsonResponse({"error": "Invalid time frame"}, status=400)

    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            if not isinstance(data, list):
                data = []  # Reset if not a list
    except (IOError, json.JSONDecodeError) as e:
        return JsonResponse({"status": "Error reading database status", "error": str(e)}, status=500)

    filtered_data = [entry for entry in data if datetime.fromisoformat(entry['timestamp'][:-1]) >= start_time]

    response_data = {
        "T": frame,
        "data": filtered_data
    }

    return JsonResponse(response_data, safe=False)
