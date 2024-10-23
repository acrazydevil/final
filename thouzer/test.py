import subprocess

def get_window_id(window_name):
    try:
        return subprocess.check_output(["xdotool", "search", "--name", window_name]).decode().strip().split()
    except subprocess.CalledProcessError:
        return None
def focus_window(window_id):
    subprocess.run(["xdotool", "windowactivate", window_id])
    
def send_key(window_id, key):
    subprocess.run(["xdotool", "key", "--window", window_id, key])

def click_mouse(window_id, button):
    subprocess.run(["xdotool", "click", "--window", window_id, str(button)])
def main():
    window_name = "RViz"
    window_ids = get_window_id(window_name)
    if window_ids:
        for window_id in window_ids:
            print(f"Found window with ID: {window_id}")
            focus_window(window_id)
            send_super_up(window_id)
            # send_key(window_id, 'Super + Up')  # Fullscreen toggle
            click_mouse(window_id, 1)  # Left click
    else:
        print(f"No window found with name: {window_name}")
def send_super_up(window_id):
    subprocess.run(["xdotool", "keydown", "--window", window_id, "Super_L"])
    subprocess.run(["xdotool", "key", "--window", window_id, "Up"])
    subprocess.run(["xdotool", "keyup", "--window", window_id, "Super_L"])
if __name__ == "__main__":
    main()
