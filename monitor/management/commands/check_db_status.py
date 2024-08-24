
import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Check the database status and write it to a JSON file'

    def handle(self, *args, **kwargs):
        status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'startup_status': 'unknown',
            'db_mode': 'unknown',
            'last_query_time': 'unknown',
            'error': None,
            'color_code': '#6c757d'  # Default gray color for unknown status
        }

        try:
            # Attempt a simple query to check database connectivity
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                status['status'] = 'running'
                status['last_query_time'] = datetime.now().isoformat()
                status['color_code'] = '#28a745'  # Green for running

            # Additional checks
            status['db_mode'] = self.check_db_mode()

        except Exception as e:
            # Handle any exceptions and record the error message
            status['status'] = 'error'
            status['error'] = str(e)
            status['startup_status'] = 'failed'
            status['color_code'] = '#dc3545'  # Red for error

        # Add the current date and time
        status['timestamp'] = datetime.now().isoformat()

        # Determine the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), '../../db_status.json')

        # Ensure that the directory exists and create it if necessary
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

        # Read existing data from the JSON file if it exists
        data = []
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    if not isinstance(data, list):
                        data = []  # Reset if not a list
                except json.JSONDecodeError:
                    data = []

        # Append the new status with timestamp and color code
        data.append(status)

        # Write the updated data back to the JSON file
        try:
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            self.stdout.write(self.style.SUCCESS('Database status appended to db_status.json'))
        except IOError as e:
            self.stdout.write(self.style.ERROR(f'Failed to write to {json_file_path}: {e}'))

    def check_db_mode(self):
        # Example function to determine read/write status
        # This is a placeholder and should be replaced with actual logic
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_is_in_recovery()")
                is_in_recovery = cursor.fetchone()[0]
                return 'read-only' if is_in_recovery else 'read/write'
        except Exception:
            return 'unknown'
