import subprocess
import time
import random

def generate_cron_error_logs(count=100, delay=0.01):
    """
    Generates a specified number of log messages containing a 'cron' error.
    """
    commands = ['/usr/bin/python3 /path/to/script.py', '/usr/bin/backup-job.sh', '/bin/sync-files.pl']
    users = ['root', 'admin', 'user']

    print(f"Starting to generate {count} cron error logs...")
    for i in range(1, count + 1):
        pid = random.randint(1000, 9999)
        user = random.choice(users)
        command = random.choice(commands)

        message = f"CRON[{pid}]: ({user}) CMD ({command}) FAILED to run"
        log_command = ['logger', '-t', 'test-cron-errors', message]
        subprocess.run(log_command)

        print(f"Logged message {i}")
        time.sleep(delay)
    print("Log generation complete.")

if __name__ == "__main__":
    generate_cron_error_logs(count=200, delay=0.01)
