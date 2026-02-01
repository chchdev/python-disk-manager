import os
import time

def main():
    # Needs to be runnning 24-7
    while True:
        try:
            os.system("python src/space.py")
            
            # Run every 30 minutes
            time.sleep(1800)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()