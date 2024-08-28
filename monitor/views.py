import os
import json
from datetime import datetime, timedelta
from django.http import JsonResponse

def get_db_status(request):
    # Correct path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'db_status.json')

    # Retrieve the frame from the query parameters
    frame = request.GET.get('frame', None)

    # Determine the time range based on the frame
    now = datetime.now()
    if frame == '24H':
        start_time = now - timedelta(hours=24)
    elif frame == '1WK':
        start_time = now - timedelta(weeks=1)
    elif frame == '1MO':
        start_time = now - timedelta(days=30)
    else:
        return JsonResponse({"error": "Invalid time frame"}, status=400)

    # Read the database status from the JSON file
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            if not isinstance(data, list):
                data = []  # Reset if not a list
    except (IOError, json.JSONDecodeError) as e:
        # Handle errors (e.g., file not found or invalid JSON)
        return JsonResponse({"status": "Error reading database status", "error": str(e)}, status=500)

    # Filter data based on the time range
    filtered_data = [entry for entry in data if datetime.fromisoformat(entry['timestamp'][:-1]) >= start_time]

    response_data = {
        "T": frame,
        "data": filtered_data
    }

    # Return the database status as a JSON response
    return JsonResponse(response_data, safe=False)
