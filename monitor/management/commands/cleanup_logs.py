import os
import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Clean up old log entries from db_status.json'

    def handle(self, *args, **kwargs):
        # Define the log retention period (3 months)
        retention_period = timedelta(days=90)  # 3 months
        now = datetime.now()
        three_months_ago = now - retention_period

        # Determine the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), '../../db_status.json')

        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.WARNING('No db_status.json file found to clean up.'))
            return

        try:
            # Load the existing data from the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                if not isinstance(data, list):
                    self.stdout.write(self.style.WARNING('Invalid data format in db_status.json'))
                    return

            # Filter out log entries older than 3 months
            filtered_data = []
            for entry in data:
                try:
                    entry_time = datetime.strptime(entry['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
                    if entry_time > three_months_ago:
                        filtered_data.append(entry)
                except KeyError:
                    self.stdout.write(self.style.WARNING(f'Missing "timestamp" key in entry: {entry}'))
                except ValueError:
                    self.stdout.write(self.style.WARNING(f'Invalid timestamp format in entry: {entry}'))

            # Write the filtered data back to the JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(filtered_data, json_file, indent=4)

            self.stdout.write(self.style.SUCCESS(f'Cleaned up old log entries in {json_file_path}'))

        except (IOError, json.JSONDecodeError) as e:
            self.stdout.write(self.style.ERROR(f'Failed to clean up logs: {e}'))
