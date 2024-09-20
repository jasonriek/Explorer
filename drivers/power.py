import subprocess
import time

def check_power_status():
    result = subprocess.run(['vcgencmd', 'get_throttled'], stdout=subprocess.PIPE)
    status = result.stdout.decode('utf-8').strip()

    if status == 'throttled=0x0':
        print("No power issues detected.")
    else:
        print(f"Power issues detected: {status}")
        if '0x50000' in status:
            print("Under-voltage warning!")
        if '0x20000' in status:
            print("Currently throttled due to under-voltage.")
        if '0x40000' in status:
            print("Frequency capped due to low voltage.")

# Continuously monitor every 10 seconds
while True:
    check_power_status()
    time.sleep(10)  # Check every 10 seconds
