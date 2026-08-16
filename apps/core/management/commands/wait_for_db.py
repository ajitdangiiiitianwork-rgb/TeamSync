# apps/core/management/commands/wait_for_db.py
import time
import os
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that waits for the specific database to be available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        
        db_name = os.getenv('DB_NAME', 'teamsync')
        attempts = 0
        max_attempts = 30

        while attempts < max_attempts:
            try:
                # Try to connect and query the SPECIFIC database
                connection = connections['default']
                connection.ensure_connection()
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS(f'Database "{db_name}" is ready!'))
                return
            except OperationalError as e:
                self.stdout.write(f'Waiting for database "{db_name}"... ({e})')
                time.sleep(1)
                attempts += 1

        self.stdout.write(self.style.ERROR(f'Database "{db_name}" failed to connect after {max_attempts} attempts'))
        exit(1)