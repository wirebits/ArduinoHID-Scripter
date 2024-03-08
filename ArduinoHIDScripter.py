import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

alphabet_keys = {
    'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g',
    'H': 'h', 'I': 'i', 'J': 'j','K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
    'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't', 'U': 'u',
    'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z'
}

other_keys = {
    'F1': 'KEY_F1', 'F2': 'KEY_F2', 'F3': 'KEY_F3', 'F4': 'KEY_F4',
    'F5': 'KEY_F5', 'F6': 'KEY_F6', 'F7': 'KEY_F7', 'F8': 'KEY_F8', 'F9': 'KEY_F9',
    'F10': 'KEY_F10', 'F11': 'KEY_F11', 'F12': 'KEY_F12', 'LEFT': 'KEY_LEFT_ARROW',
    'UP': 'KEY_UP_ARROW', 'RIGHT': 'KEY_RIGHT_ARROW', 'DOWN': 'KEY_DOWN_ARROW',
    'TAB': 'KEY_TAB', 'HOME': 'KEY_HOME', 'END': 'KEY_END', 'PGUP': 'KEY_PAGE_UP',
    'PGDN': 'KEY_PAGE_DOWN', 'CAPS': 'KEY_CAPS_LOCK', 'NUM': 'KEY_NUM_LOCK',
    'SCROLL': 'KEY_SCROLL_LOCK', 'GUI': 'KEY_LEFT_GUI', 'ESC': 'KEY_ESC',
    'PRTSCR': 'KEY_PRINT_SCREEN', 'PAUSE': 'KEY_PAUSE', 'SPACE': 'KEY_SPACE', 'DEL': 'KEY_DELETE',
    'INSERT': 'KEY_INSERT', 'BKSP': 'KEY_BACKSPACE', 'ENTER': 'KEY_RETURN'
}

modifier_keys = {'CTRL': 'KEY_LEFT_CTRL', 'SHIFT': 'KEY_LEFT_SHIFT', 'ALT': 'KEY_LEFT_ALT'}

class ArduinoHIDConverter:
    @staticmethod
    def convert_to_arduino_script(arduino_mnemonic):
        if arduino_mnemonic.startswith("TYPE"):
            string_text = arduino_mnemonic.split(" ", 1)[1]
            string_text = string_text.replace('"', r'\"')
            return f" Keyboard.print(\"{string_text}\");"
        elif arduino_mnemonic.startswith("TYNL"):
            string_text = arduino_mnemonic.split(" ", 1)[1]
            string_text = string_text.replace('"', r'\"')
            return f" Keyboard.println(\"{string_text}\");"
        elif arduino_mnemonic.startswith("PRESS"):
            keys = arduino_mnemonic.split()[1:]
            key_sequence = [alphabet_keys.get(key, other_keys.get(key, modifier_keys.get(key))) for key in keys]
            formatted_sequence = ''.join(key_sequence)
            press_code = ""
            release_code = "Keyboard.releaseAll();"
            for key in key_sequence:
                if key.startswith("KEY_"):
                    press_code += f" Keyboard.press({key});\n"
                else:
                    press_code += f" Keyboard.press('{key}');\n"
            press_code += f" {release_code}"
            return press_code
        elif arduino_mnemonic.startswith("WAIT"):
            delay_time = int(arduino_mnemonic.split(" ")[1])
            return f" delay({delay_time});"
        else:
            return arduino_mnemonic

class ArduinoHIDMain:
    def __init__(self, main_window):
        self.main_window = main_window
        self.create_widgets()

    def create_widgets(self):
        self.main_window.title("ArduinoHID Scripter")
        self.main_window.resizable(0, 0)

        main_split_frame = ttk.Frame(self.main_window)
        main_split_frame.pack(side="top", fill="both", expand=True)

        self.mnemonic_frame = tk.Text(main_split_frame, font='courier 10', fg='black')
        self.mnemonic_frame.pack(side="left", fill="both", expand=True)
        self.mnemonic_frame.insert(tk.END, "Enter your mnemonic")

        self.arduino_frame = tk.Text(main_split_frame, font='courier 10', fg='black')
        self.arduino_frame.pack(side="right", fill="both", expand=True)
        self.arduino_frame.insert(tk.END, "Your arduino script")

        self.mnemonic_frame.bind("<FocusIn>", self.clear_placeholder)
        self.mnemonic_frame.bind("<Button-1>", self.disable_convert_button)

        buttons_frame = ttk.Frame(self.main_window)
        buttons_frame.pack(side="top", fill="x")

        self.convert_button = ttk.Button(buttons_frame, text="Convert", command=self.convert_text, state=tk.DISABLED)
        self.convert_button.pack(side="left", padx=5, pady=5)

        copy_button = ttk.Button(buttons_frame, text="Copy", command=self.copy_text)
        copy_button.pack(side="left", padx=5, pady=5)

        reset_button = ttk.Button(buttons_frame, text="Reset", command=self.reset_all)
        reset_button.pack(side="left", padx=5, pady=5)

        save_button = ttk.Button(buttons_frame, text="Save", command=self.save_file)
        save_button.pack(side="left", padx=5, pady=5)

        exit_button = ttk.Button(buttons_frame, text="Exit", command=self.exit_window)
        exit_button.pack(side="right", padx=5, pady=5)

    def clear_placeholder(self, event):
        if event.widget.get(1.0, tk.END).strip() == "Enter your mnemonic":
            event.widget.delete(1.0, tk.END)

    def disable_convert_button(self, event):
        self.convert_button.configure(state=tk.NORMAL)
    
    def convert_text(self):
        mnemonic_script = self.mnemonic_frame.get(1.0, tk.END).strip()
        if not mnemonic_script:
            self.arduino_frame.delete(1.0, tk.END)
            self.arduino_frame.insert(tk.END, "Enter some mnemonics to convert!")
        else:
            mnemonics = "#include<Keyboard.h>\nvoid setup()\n{\n Keyboard.begin();\n"
            for line in mnemonic_script.splitlines():
                if line.startswith("REDO"):
                    parts = line.split()
                    if len(parts) < 3:
                        continue
                    try:
                        num_iterations = int(parts[1])
                        if "PRESS" in parts[2:]:
                            self.arduino_frame.delete(1.0, tk.END)
                            self.arduino_frame.insert(tk.END, "Use TYPE, TYNL and WAIT Only!")
                            return
                    except ValueError:
                        continue
                    mnemonics += f" for (int i=0; i<={num_iterations}; i++)\n"
                    mnemonics += " {\n"
                    for mnemonic in " ".join(parts[2:]).split(","):
                        converted_line = ArduinoHIDConverter.convert_to_arduino_script(mnemonic.strip())
                        mnemonics += f" {converted_line}\n"
                    mnemonics += " }\n"
                elif line.strip() == "PRESS":
                    self.arduino_frame.delete(1.0, tk.END)
                    self.arduino_frame.insert(tk.END, "Use TYPE, TYNL and WAIT Only!")
                    return
                else:
                    converted_line = ArduinoHIDConverter.convert_to_arduino_script(line.strip())
                    mnemonics += converted_line + '\n'
            mnemonics += " Keyboard.end();\n}\nvoid loop()\n{\n //Nothing to do here ;)\n}"
            self.arduino_frame.delete(1.0, tk.END)
            self.arduino_frame.insert(tk.END, mnemonics)
            self.arduino_frame.mark_set(tk.INSERT, "end-1c linestart")

    def copy_text(self):
        self.main_window.clipboard_clear()
        self.main_window.clipboard_append(self.arduino_frame.get(1.0, tk.END))

    def reset_all(self):
        self.mnemonic_frame.delete(1.0, tk.END)
        self.mnemonic_frame.insert(tk.END, "Enter your mnemonic")
        self.arduino_frame.delete(1.0, tk.END)
        self.arduino_frame.insert(tk.END, "Your arduino script")
        self.convert_button.configure(state=tk.DISABLED)

    def exit_window(self):
        self.main_window.destroy()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('Arduino Files', '*.ino')], defaultextension='.ino')
        if not file_path:
            return
        with open(file_path, 'w') as file:
            file.write(self.arduino_frame.get(1.0, tk.END))

main_window = tk.Tk()
app = ArduinoHIDMain(main_window)
main_window.mainloop()