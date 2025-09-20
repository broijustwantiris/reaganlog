import subprocess
import time

def generate_error_logs(count=100, delay=0.01):
    """
    Generates a specified number of log messages containing the word "error".
    """
    print(f"Starting to generate {count} error logs...")
    for i in range(1, count + 1):
        message = f"Error: Test log message {i} from error generator."
        command = ['logger', '-t', 'test-error-script', message]
        subprocess.run(command)
        print(f"Logged message {i}")
        time.sleep(delay)
    print("Log generation complete.")

if __name__ == "__main__":
    generate_error_logs(count=200, delay=0.01)
