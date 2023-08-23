import threading
import time

# The shared variable that will be updated by the inner loop
shared_variable = 0

# Create a thread for the inner loop
inner_thread = threading.Thread(target=lambda: None)  # An empty lambda function for now
inner_thread.daemon = True  # Set the thread as daemon so it terminates when the main thread ends
inner_thread.start()

# Time tracking for the inner loop
last_update_time = time.time()

# Outer loop
while True:
    current_time = time.time()
    
    # Check if 1 second has elapsed since the last update in the inner loop
    if current_time - last_update_time >= 1.0:
        shared_variable += 1  # Update the shared variable
        last_update_time = current_time  # Update the last update time
    
    print(f"Shared variable: {shared_variable}")
    time.sleep(0.5)  # Print every 0.5 seconds

    # Add other code for the outer loop if needed
