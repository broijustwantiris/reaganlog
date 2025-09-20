import subprocess
import time

def generate_warning_logs(count=100, delay=0.01):
    """
    Generates a specified number of log messages containing the word "warning".
    """
    print(f"Starting to generate {count} warning logs...")
    for i in range(1, count + 1):
        message = f"Warning: Test log message {i} from warning generator."
        command = ['logger', '-t', 'test-warning-script', message]
        subprocess.run(command)
        print(f"Logged message {i}")
        time.sleep(delay)
    print("Log generation complete.")

if __name__ == "__main__":
    generate_warning_logs(count=200, delay=0.01)
