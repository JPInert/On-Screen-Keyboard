import tkinter as tk
import pygetwindow as gw
import pyautogui
import threading
import time
import string

# Initialize caps lock and shift state
is_caps_lock = False
is_shifted = False

def insert_letter(letter):
    if last_focused_window:
        last_focused_window.activate()
        if is_caps_lock or is_shifted and letter in string.ascii_letters:
            letter = letter.upper()
        elif is_caps_lock or is_shifted and letter in string.punctuation:
            # Handle symbol keys when caps lock is enabled
            symbols = {'-': '_', '=': '+', '[': '{', ']': '}', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'}

            letter = symbols.get(letter, letter)
        if letter.isdigit() and is_caps_lock or is_shifted :
            # Convert the digit to the corresponding symbol when caps lock is enabled
            symbols = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')'}
            letter = symbols.get(letter, letter)
        # Directly send the key press event
        pyautogui.press(letter)
        if is_shifted:
            toggle_shift()  # Call toggle_shift() after pressing the letter

def toggle_caps_lock():
    global is_caps_lock
    is_caps_lock = not is_caps_lock
    update_keyboard_layout()

def toggle_shift():
    global is_shifted
    is_shifted = not is_shifted
    update_keyboard_layout()

def backspace():
        if last_focused_window:
            last_focused_window.activate()
            pyautogui.press('backspace')

def backslash():
        if last_focused_window:
            last_focused_window.activate()
            if is_caps_lock or is_shifted:
                pyautogui.press('|')
            else:
                pyautogui.press('\\')

def enter_key():
    if last_focused_window:
        last_focused_window.activate()
        pyautogui.press('enter')

def spacebar():
    if last_focused_window:
        last_focused_window.activate()
        pyautogui.typewrite(' ')

def update_keyboard_layout():
    layout = uppercase_alphabet if is_caps_lock or is_shifted else lowercase_alphabet
    for button, row in zip(letter_buttons, layout):
        for letter, button_text in zip(row, button):
            button_text.set(letter.upper() if is_caps_lock or is_shifted else letter.lower())
    backslash_button_text.set("|" if is_caps_lock or is_shifted  else "\\")

def check_last_focused_window():
    global last_focused_window
    while True:
        current_window = gw.getActiveWindow()
        # Exclude the virtual keyboard window from being considered
        if current_window != last_focused_window and current_window.title != "Virtual Keyboard":
             last_focused_window = current_window
        # Disaply variables on GUI
        # current_window_label.config(text=f"last_focused_window: {last_focused_window}\ncurrent_window: {current_window}")
        time.sleep(1)

root = tk.Tk()
root.title("Virtual Keyboard")

# Set the window to be always on top
root.wm_attributes('-topmost', 1)

# Define the lowercase and uppercase alphabets
lowercase_alphabet = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
]

uppercase_alphabet = [
    ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?']
]

# Create a label to display the current window
# current_window_label = tk.Label(root)
# current_window_label.pack(pady=10)

# Create the buttons for each letter
letter_buttons = []
layout = lowercase_alphabet
button_width = 2  # Adjust the width of the buttons
button_height = 1  # Adjust the height of the buttons
button_font_size = 8  # Adjust the font size of the button text
for row_index, row in enumerate(layout):
    button_row = []
    for col_index, letter in enumerate(row):
        button_text = tk.StringVar()
        button_text.set(letter)
        button = tk.Button(root, textvariable=button_text, width=button_width, height=button_height, font=("Arial", button_font_size), command=lambda l=letter: insert_letter(l))
        button.grid(row=row_index, column=col_index, padx=1, pady=1)
        button_row.append(button_text)
    letter_buttons.append(button_row)

# Create the Caps Lock button
caps_lock_button = tk.Button(root, text="Caps Lock", width=10, height=button_height, font=("Arial", button_font_size), command=toggle_caps_lock)
caps_lock_button.grid(row=4, column=13, padx=1, pady=1)

# Create the Shift button
shift_button = tk.Button(root, text="Shift", width=10, height=button_height, font=("Arial", button_font_size), command=toggle_shift)
shift_button.grid(row=3, column=13, padx=1, pady=1)


# Create the Backspace button
backspace_button = tk.Button(root, text="Backspace", width=10, height=button_height, font=("Arial", button_font_size), command=backspace)
backspace_button.grid(row=0, column=13, padx=1, pady=1)

# Create the Backslash button
backslash_button_text = tk.StringVar()
backslash_button_text.set("|" if is_caps_lock or is_shifted else "\\")
backslash_button = tk.Button(root, textvariable=backslash_button_text, width=10, height=button_height, font=("Arial", button_font_size), command=backslash)
backslash_button.grid(row=1, column=13, padx=1, pady=1)

# Create the Enter button
enter_button = tk.Button(root, text="Enter", width=10, height=button_height, font=("Arial", button_font_size), command=enter_key)
enter_button.grid(row=2, column=13, padx=1, pady=1)

# Create the spacebar button
spacebar_button = tk.Button(root, text="Space", width=20, height=button_height, font=("Arial", button_font_size), command=spacebar)
spacebar_button.grid(row=4, column=0, columnspan=13, padx=1, pady=1)

# Initialize the last focused window
last_focused_window = gw.getActiveWindow()

# Start a thread to continuously check the last focused window
window_check_thread = threading.Thread(target=check_last_focused_window)
window_check_thread.daemon = True
window_check_thread.start()

root.mainloop()