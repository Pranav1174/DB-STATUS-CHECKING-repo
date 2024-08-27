from django.http import JsonResponse
import os
import json

def get_db_status(request):
    # Determine the path to the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), '../db_status.json')

    try:
        # Read the database status from the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except (IOError, json.JSONDecodeError) as e:
        # Handle errors (e.g., file not found or invalid JSON)
        data = {"status": "Error reading database status", "error": str(e)}

    # Return the database status as a JSON response
    return JsonResponse(data, safe=False)
