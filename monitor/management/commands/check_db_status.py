import json
import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check the database status and write it to a JSON file'

    def handle(self, *args, **kwargs):
        status = {}
        try:
            # Attempt a simple query to check database connectivity
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            status['status'] = 'running'
        except Exception as e:
            # Handle any exceptions and record the error message
            status['status'] = 'error'
            status['error'] = str(e)
        
        # Determine the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), '../../db_status.json')
        
        # Ensure that the directory exists and create it if necessary
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
        
        # Write the status to the JSON file
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(status, json_file, indent=4)
            self.stdout.write(self.style.SUCCESS('Database status written to db_status.json'))
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'Failed to write to {json_file_path}: {e}'))
