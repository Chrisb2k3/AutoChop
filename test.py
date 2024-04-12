import keyboard


# Function to exit the loop
def exit_loop():
    global g_loop
    g_loop = False


# Register the 'q' key to call the exit_loop function
keyboard.add_hotkey('q', exit_loop)

# Example loop
g_loop = True
while g_loop:
    # Your loop code here
    pass

# Loop exited
print("Loop exited.")
