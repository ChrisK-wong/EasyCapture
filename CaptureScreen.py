import tkinter as tk
from PIL import ImageGrab
import json
from CaptureSave import save
import CaptureGUI
import screeninfo

class Capture:
    def __init__(self, configs, ac=False, ac_delay=None, ac_count=None):
        self.root = tk.Tk()
        self.settings = configs
        self.mode = ac
        self.ac_delay = ac_delay
        self.ac_count = ac_count
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', '0.05')
        self.root.attributes('-transparentcolor', 'ghost white')
        self.root.overrideredirect(True)
        width = 0
        for monitor in screeninfo.get_monitors():
            width += monitor.width
            height = monitor.height
        self.overlay = tk.Canvas(self.root, width=width, height=height, bg='black', highlightthickness=0,
                                 cursor='crosshair')
        self.overlay.pack()
        self.overlay.bind('<ButtonPress-1>', self.button_press_m1)
        self.overlay.bind('<ButtonRelease-3>', self.button_press_m2)
        self.overlay.bind("<B1-Motion>", self.button_move)
        self.overlay.bind('<ButtonRelease-1>', self.button_release)
        self.pos_x1 = None
        self.pos_y1 = None
        self.pos_x2 = None
        self.pos_y2 = None
        self.highlight = None
        self.AC_coords = None

        self.root.mainloop()

    def button_press_m1(self, event):
        self.pos_x1 = event.x
        self.pos_y1 = event.y
        if not self.highlight:
            if not self.mode:
                self.highlight = self.overlay.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x1, self.pos_y1,
                                                               outline='purple', width=2, fill="white")
            else:
                self.highlight = self.overlay.create_rectangle(self.pos_x1, self.pos_y1, self.pos_x1, self.pos_y1,
                                                               outline='purple', width=2, fill="ghost white")

    def button_press_m2(self, event):
        if self.pos_x2 or self.mode:
            self.root.destroy()
            self.root.quit()
        else:
            self.root.destroy()
            CaptureGUI.CaptureGUI(self.settings, image=False)


    def button_move(self, event):
        self.pos_x2 = self.overlay.canvasx(event.x)
        self.pos_y2 = self.overlay.canvasy(event.y)
        self.overlay.coords(self.highlight, self.pos_x1, self.pos_y1, self.pos_x2, self.pos_y2)

    def button_release(self, event):
        self.pos_x2 = event.x
        self.pos_y2 = event.y
        if self.mode and (self.pos_x1 != self.pos_x2) and (self.pos_y1 != self.pos_y2):
            self.auto_capture_mode()
        elif (self.pos_x1 != self.pos_x2) and (self.pos_y1 != self.pos_y2):
            self.root.destroy()
            self.actions(self.capture_image())
        else:
            self.root.destroy()
            self.root.quit()
        # ImageGrab (left_x, top_y, right_x, bottom_y)

    def capture_image(self):
        if self.pos_x1 < self.pos_x2 and self.pos_y1 > self.pos_y2:
            return ImageGrab.grab(bbox=(self.pos_x1 + 1, self.pos_y2 + 1, self.pos_x2 - 1, self.pos_y1 - 1), include_layered_windows=False, all_screens=True)
        elif self.pos_x1 > self.pos_x2 and self.pos_y1 < self.pos_y2:
            return ImageGrab.grab(bbox=(self.pos_x2 + 1, self.pos_y1 + 1, self.pos_x1 - 1, self.pos_y2 - 1), include_layered_windows=False, all_screens=True)
        elif self.pos_x1 > self.pos_x2 and self.pos_y1 > self.pos_y2:
            return ImageGrab.grab(bbox=(self.pos_x2 + 1, self.pos_y2 + 1, self.pos_x1 - 1, self.pos_y1 - 1), include_layered_windows=False, all_screens=True)
        else:
            return ImageGrab.grab(bbox=(self.pos_x1 + 1, self.pos_y1 + 1, self.pos_x2 - 1, self.pos_y2 - 1), include_layered_windows=False, all_screens=True)

    def auto_capture_mode(self):
        self.overlay.configure(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight(),
                               bg='ghost white')
        self.root.attributes('-alpha', '1')
        AC = tk.Tk()
        AC.title('Auto Capture')
        AC.iconbitmap('EasyCapture.ico')
        AC.resizable(False, False)

        label_delay = tk.Label(AC, width=15)
        label_count = tk.Label(AC, width=15, text="Count: 0" + "/" + str(self.ac_count))
        label_delay.pack(side="left", padx=10)
        label_count.pack(side="left", padx=10)

        def disable_event():
            pass

        AC.protocol("WM_DELETE_WINDOW", disable_event)

        def stop():
            self.root.destroy()
            AC.destroy()

        stop = tk.Button(AC, text="Stop", bg='red3', width=5, command=stop)
        stop.pack(side="left", padx=10)

        def countdown(delay, max):
            label_delay['text'] = "Delay: " + str(delay) + "/" + str(self.ac_delay)
            if delay > 0:
                AC.after(1000, countdown, delay-1, max)
            elif delay == 0:
                max -= 1
                countdown(self.ac_delay, max)
                label_count['text'] = "Count: " + str(self.ac_count - max) + "/" + str(self.ac_count)
                save(self.capture_image())
                if max == 0:
                    AC.destroy()
                    self.root.destroy()

        countdown(self.ac_delay, self.ac_count)
        AC.mainloop()

    def actions(self, pic):
        if self.settings['setting'] == "1":  # Open Interface
            CaptureGUI.CaptureGUI(self.settings, pic)
        elif self.settings['setting'] == "2":  # Auto Save
            save(pic)

if __name__ == "__main__":
    with open('settings.json') as f:
        settings = json.load(f)
    Capture = Capture(settings, False)
    #print(Capture.pos_x1, Capture.pos_y1, Capture.pos_x2, Capture.pos_y2)
