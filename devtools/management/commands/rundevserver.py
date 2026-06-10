from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from shutil import which

import sys
import subprocess
import time

import redis

class Command(BaseCommand):
    
    help = "Runs the WoL server and initializes the requirement environment for development tests."

    def redis_running(self):
        try:
            redis.Redis(host="localhost", port=6379).ping()
            return True
        except redis.ConnectionError:
            return False

    def handle(self, *args, **options):
        
        if which('redis-server') is None:
            raise CommandError(
                "Redis server package is required to start the development environment."
            )

        if self.redis_running():
            raise CommandError(
                "Redis server already running in background. Cannot start developement environment."
            )

        
        redis_process = subprocess.Popen(
            ["redis-server", f"{settings.BASE_DIR}/devtools/config/redis.conf"],
            cwd=settings.BASE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        try:
            time.sleep(0.5)

            self.stdout.write(
                self.style.SUCCESS("Redis server started.")
            )

            subprocess.call(
                [sys.executable, "manage.py", "runserver"]
            )

        finally:
            redis_process.terminate()

            try:
                redis_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                redis_process.kill()

        