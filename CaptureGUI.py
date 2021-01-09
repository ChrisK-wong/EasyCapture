from tkinter import filedialog
import tkinter as tk
import json
from PIL import ImageTk, Image, ImageGrab
from CaptureSave import save
import CaptureScreen


class CaptureGUI:
    def __init__(self, configs, image):
        self.root = tk.Tk()
        self.root.title('EasyCapture')
        self.root.iconbitmap('EasyCapture.ico')
        tk.Label(self.root, text="EasyCapture")
        self.root.resizable(False, False)
        self.settings = configs
        self.image = image

        self.entry = tk.StringVar()
        self.entry2 = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.Setting = tk.StringVar(value=self.settings['setting'])

        if image:
            self.image_frame = tk.Frame(self.root, padx=20, pady=5)
            self.pic = ImageTk.PhotoImage(self.resize())
            self.image_label = tk.Label(self.image_frame, image=self.pic)
            width, height = self.image.size
            self.image_res = tk.Label(self.image_frame, text="{} x {}".format(width, height))
            self.save_label = tk.Label(self.image_frame, text="Save as:")
            self.save_name = tk.Entry(self.image_frame, width=25)
            self.image_frame.grid()
            self.image_label.grid()
            self.save_label.grid(row=1, column=0, sticky="W", pady=10)
            self.save_as()
            self.save_name.grid(row=1, column=0, padx=60, sticky="W")
            self.image_res.grid(row=1, column=0, sticky="E")
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=1, column=0, sticky="W", padx=20)

        if image:
            self.SaveButton = tk.Button(self.frame, text="Save", padx=40, pady=10, command=self.save_pic)
            self.SaveButton.grid(row=0, column=0, padx=20, pady=10)

        self.NewButton = tk.Button(self.frame, text="New", padx=40, pady=10, command=self.new)
        self.AdvancedButton = tk.Button(self.frame, text="Advanced", padx=50, command=self.show_advanced)
        self.NewButton.grid(row=0, column=1, padx=20, pady=10)
        self.AdvancedButton.grid(row=2, column=0, pady=10, columnspan=2)

        self.frame_folder = tk.LabelFrame(self.root, text="Folder Path", padx=5, pady=5)
        self.frame_settings = tk.LabelFrame(self.root, text="Settings")

        self.path_name = tk.Entry(self.frame_folder, width=30)
        self.BrowseButton = tk.Button(self.frame_folder, text="Browse", command=self.browse)

        self.OpenInterface = tk.Radiobutton(self.frame_settings, text="Prompt this interface after capturing image",
                                            variable=self.Setting, command=self.update_settings, value="1")
        self.AutoSaveButton = tk.Radiobutton(self.frame_settings,
                                             text="Automatically save to folder after capturing image",
                                             variable=self.Setting, command=self.update_settings, value="2")

        self.frame_AutoCapture = tk.LabelFrame(self.root, text="Auto Capture")
        self.AC_label1 = tk.Label(self.frame_AutoCapture, text='Delay (sec):')
        vcmd = (self.root.register(self.validation), '%S')
        self.AC_delay = tk.Entry(self.frame_AutoCapture, width=5, validate='key', vcmd=vcmd, textvariable=self.entry)
        self.AC_label2 = tk.Label(self.frame_AutoCapture, text='Count:')
        self.AC_count = tk.Entry(self.frame_AutoCapture, width=5, validate='key', vcmd=vcmd, textvariable=self.entry2)
        self.AC_start = tk.Button(self.frame_AutoCapture, text="Start", bg='chartreuse3', width=5, command=self.start, state='disabled')
        self.AC_label3 = tk.Label(self.frame_AutoCapture, text='( Auto Capture will save to folder )')
        self.entry.trace('w', self.validation_start)
        self.entry2.trace('w', self.validation_start)
        self.root.mainloop()


    def resize(self):
        width, height = self.image.size
        if width > 500 or height > 500:
            if width >= height:
                new_width = width * (500 / width)
                new_height = height * (500 / width)
            elif height > width:
                new_width = width * (500 / height)
                new_height = height * (500 / height)
        else:
            new_width = width
            new_height = height
        resized_image = self.image.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        return resized_image

    def new(self):
        self.root.destroy()
        with open('settings.json') as f:
            configs = json.load(f)
        CaptureScreen.Capture(configs, False)

    def save_pic(self):
        save_name = self.save_name.get()
        if self.settings['folder'] == '':
            self.browse()
        save(self.image, save_name)

    def show_advanced(self):
        self.AdvancedButton.configure(bg="gray70")
        self.AdvancedButton["command"] = self.hide_advanced
        self.frame_folder.grid(row=2, column=0, sticky="W", padx=20)
        self.path_name.grid(row=0, column=0, sticky="W", padx=10)
        self.path_name.insert(tk.END, self.settings['folder'])
        self.BrowseButton.grid(row=0, column=1, sticky="W", padx=10)
        self.frame_settings.grid(row=3, column=0, sticky="W", padx=20, pady=10)
        self.OpenInterface.grid(row=3, column=0, columnspan=3, padx=0, sticky="W")
        self.AutoSaveButton.grid(row=4, column=0, columnspan=3, padx=0, sticky="W")
        self.frame_AutoCapture.grid(sticky="W", padx=20, pady=10, row=4)
        self.AC_label1.grid(row=0, column=0, padx=5)
        self.AC_delay.grid(row=0, column=1, padx=1, pady=10)
        self.AC_label2.grid(row=0, column=2, padx=5)
        self.AC_count.grid(row=0, column=3, padx=1)
        self.AC_start.grid(row=0, column=4, padx=20)
        self.AC_label3.grid(row=1, column=0, columnspan=3, padx=5)


    def hide_advanced(self):
        self.AdvancedButton.configure(bg="#F0F0F0")
        self.AdvancedButton["command"] = self.show_advanced
        self.frame_settings.grid_forget()
        self.frame_folder.grid_forget()
        self.frame_AutoCapture.grid_forget()

    def browse(self):
        file_name = filedialog.askdirectory()
        if file_name:
            self.path_name.delete(0, tk.END)
            self.path_name.insert(tk.END, file_name)
            self.settings['folder'] = file_name
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f, indent=2)

    def save_as(self):
        image_name = "EasyCapture.png"
        self.save_name.insert(tk.END, image_name)

    def update_settings(self):
        self.settings['setting'] = self.Setting.get()
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)

    def validation(self, input):
        if len(input) > 1:
            for num in input:
                if num not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return False
            return True
        elif input in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        return False

    def validation_start(self, *args):
        if len(self.AC_delay.get()) > 0 and len(self.AC_count.get()) > 0:
            self.AC_start.configure(state='normal')
        else:
            self.AC_start.configure(state='disabled')

    def start(self):
        if len(self.settings['folder']) == 0:
            self.browse()
        self.AC_delay.configure(state='disabled')
        self.AC_count.configure(state='disabled')
        with open('settings.json') as f:
            configs = json.load(f)
        delay = int(self.AC_delay.get())
        count = int(self.AC_count.get())
        self.root.destroy()
        CaptureScreen.Capture(configs, ac=True, ac_delay=delay, ac_count=count)
