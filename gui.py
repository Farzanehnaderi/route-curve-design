import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from PIL import Image, ImageTk
from simple_curve import SimpleCurve
from compound_curve import CompoundCurve
from reverse_curve import ReverseCurve
from exports import export_excel, export_pdf

class RouteSurveyingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Route Curve Design and Implementation")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        self.current_curve_type = None
        self.curve_instance = None

        self.create_welcome_page()

    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_welcome_page(self):
        self.clear_frames()
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Route Curve Design and Implementation Project",
                 font=('Helvetica', 24, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(pady=30)

        tk.Label(frame, text="Dr. Yousef Kanani Sadat \n Developer: Farzaneh Naderi \n 2024-2025",
                 font=('Helvetica', 18), bg='#f0f0f0', fg='#34495e').pack(pady=20)

        try:
            img = Image.open("Back.jpg").resize((500, 300))
            photo = ImageTk.PhotoImage(img)
            tk.Label(frame, image=photo, bg='#f0f0f0').pack(pady=30)
            self.welcome_image = photo  # نگهداری مرجع
        except:
            pass

        tk.Button(frame, text="Start Project", font=('Helvetica', 16), bg='#3498db', fg='white',
                  command=self.create_curve_selection_page).pack(pady=20, ipadx=20, ipady=10)

    def create_curve_selection_page(self):
        self.clear_frames()
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Select Curve Type", font=('Helvetica', 24, 'bold'),
                 bg='#f0f0f0', fg='#2c3e50').pack(pady=30)

        btn_frame = tk.Frame(frame, bg='#f0f0f0')
        btn_frame.pack(pady=50)

        tk.Button(btn_frame, text="Simple Curve", font=('Helvetica', 16), bg='#2ecc71', fg='white', width=20, height=3,
                  command=lambda: self.start_curve("simple")).grid(row=0, column=0, padx=20, pady=10)

        tk.Button(btn_frame, text="Compound Curve", font=('Helvetica', 16), bg='#e74c3c', fg='white', width=20, height=3,
                  command=lambda: self.start_curve("compound")).grid(row=0, column=1, padx=20, pady=10)

        tk.Button(btn_frame, text="Reverse Curve", font=('Helvetica', 16), bg='#f39c12', fg='white', width=20, height=3,
                  command=lambda: self.start_curve("reverse")).grid(row=0, column=2, padx=20, pady=10)

        tk.Button(frame, text="Back", font=('Helvetica', 14), bg='#95a5a6', fg='white',
                  command=self.create_welcome_page).pack(pady=20, ipadx=15, ipady=5)

        tk.Button(frame, text="Help", font=('Helvetica', 14), bg='#95a5a6', fg='white',
                  command=self.show_help_message).pack(pady=25, ipadx=20, ipady=5)

    def start_curve(self, curve_type):
        self.clear_frames()
        self.current_curve_type = curve_type

        if curve_type == "simple":
            self.curve_instance = SimpleCurve(self.root, self.create_curve_selection_page)
        elif curve_type == "compound":
            self.curve_instance = CompoundCurve(self.root, self.create_curve_selection_page)
        elif curve_type == "reverse":
            self.curve_instance = ReverseCurve(self.root, self.create_curve_selection_page)

    def show_help_message(self):
        help_text = """Route Curve Design Help:

1. Simple Curve:
   - Has a single radius and central angle
   - Requires radius, central angle, PI station, and maximum arc length

2. Compound Curve:
   - Consists of two curves with different radii
   - Requires radii and central angles for both curves
   - The curves must have the same direction (both right or left)

3. Reverse Curve:
   - Consists of two curves with opposite directions
   - Requires radius, deflection angle for each curve, and PI station

General Notes:
- All angles should be in degrees
- All lengths should be in meters
- The azimuth is the direction of the incoming tangent
- The curve direction determines if it turns right or left

After selecting a curve type, you'll be taken to the input parameters page.
"""
        messagebox.showinfo("Help", help_text)
