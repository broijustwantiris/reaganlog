import subprocess
import time

def generate_logs(count=1000, tag='test-flood', delay=0.001):
    """
    Generates a specified number of log messages with a short delay.

    Args:
        count (int): The number of log messages to generate.
        tag (str): The tag to associate with the log messages.
        delay (float): The delay in seconds between each message.
    """
    print(f"Starting to generate {count} log messages tagged '{tag}'...")
    for i in range(1, count + 1):
        message = f"Test log message {i} from the Python log flooder."
        command = ['logger', '-t', tag, message]
        subprocess.run(command)
        time.sleep(delay)
    print("Log generation complete.")

if __name__ == "__main__":
    # Example usage: Generate 1000 messages with a short delay
    generate_logs()
