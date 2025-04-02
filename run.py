import time
import signal
import sys
from app.controller import Controller

def main():
    Controller()

    def handle_signal(signum, frame):
        print("\nReceived shutdown signal. Cleaning up...")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handle_signal(None, None)

if __name__ == "__main__":
    main()
