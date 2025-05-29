import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math
from exports import export_excel, export_pdf

class SimpleCurve:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.radius = tk.DoubleVar(value=200)
        self.central_angle_deg = tk.DoubleVar(value=40)
        self.pi_station = tk.DoubleVar(value=10000)
        self.max_arc_length = tk.DoubleVar(value=50)
        self.azimuth = tk.DoubleVar(value=45)
        self.curve_direction = tk.StringVar(value="Right")

        self.initialize_ui()

    def initialize_ui(self):
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.main_frame.pack(fill="both", expand=True)

        title = tk.Label(self.main_frame, text="Simple Curve Design", font=('Helvetica', 20, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_input_tab()
        self.create_results_tab()
        self.create_staking_table_tab()
        self.create_diagram_tab()

    def create_input_tab(self):
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text="Input")
        
        input_frame = ttk.LabelFrame(self.input_tab, text="Input Parameters")
        input_frame.pack(padx=10, pady=10, fill='x')

        self.add_input_field(input_frame, "Radius (R):", self.radius, 0)
        self.add_input_field(input_frame, "Central Angle (Δ°):", self.central_angle_deg, 1)
        self.add_input_field(input_frame, "PI Station (m):", self.pi_station, 2)
        self.add_input_field(input_frame, "Max Arc Length (m):", self.max_arc_length, 3)
        self.add_input_field(input_frame, "Azimuth (°):", self.azimuth, 4)

        ttk.Label(input_frame, text="Direction:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        ttk.Combobox(input_frame, textvariable=self.curve_direction, values=["Right", "Left"]).grid(row=5, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.input_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Calculate", command=self.calculate_curve).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Help", command=self.show_help_dialog).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Back", command=self.back_callback).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Export Excel", command=self.export_to_excel).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Export PDF", command=self.export_to_pdf).pack(side="left", padx=10)

    def create_results_tab(self):
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Results")
        
        self.results_text = tk.Text(self.results_tab, height=15, font=('Courier', 10))
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_staking_table_tab(self):
        self.staking_table_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.staking_table_tab, text="Staking Table")
        
        self.staking_table = ttk.Treeview(self.staking_table_tab, 
                                        columns=("Point", "Station", "Arc Length", "Deflection", "Chord"), 
                                        show="headings")
        for col in self.staking_table["columns"]:
            self.staking_table.heading(col, text=col)
            self.staking_table.column(col, width=120, anchor='center')
        self.staking_table.pack(fill='both', expand=True, padx=10, pady=10)

    def create_diagram_tab(self):
        self.diagram_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.diagram_tab, text="Diagram")
        
        self.figure = Figure(figsize=(6, 4))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.diagram_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def add_input_field(self, parent, label_text, variable, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, padx=5, pady=5)

    def show_help_dialog(self):
        help_content = """Simple Curve Help:\n\n- Radius (R): Curve radius in meters\n- Central Angle (Δ): Total deflection angle in degrees\n- PI Station: Point of Intersection station\n- Max Arc Length: Maximum segment length for staking\n- Azimuth: Direction of incoming tangent (degrees)\n- Direction: Curve direction (Left or Right)\n\nCalculates PC, PT, curve geometry and staking points."""
        messagebox.showinfo("Help", help_content)

    def calculate_curve(self):
        try:
            radius = self.radius.get()
            central_angle_deg = self.central_angle_deg.get()
            central_angle_rad = math.radians(central_angle_deg)
            pi_station = self.pi_station.get()
            max_arc = self.max_arc_length.get()
            
            if radius <= 0 or central_angle_rad <= 0:
                raise ValueError("Radius and angle must be positive values.")

            curve_length = radius * central_angle_rad
            tangent_length = radius * math.tan(central_angle_rad / 2)
            chord_length = 2 * radius * math.sin(central_angle_rad / 2)
            external_distance = radius * (1 / math.cos(central_angle_rad / 2) - 1)
            middle_ordinate = radius * (1 - math.cos(central_angle_rad / 2))
            
            pc_station = pi_station - tangent_length
            pt_station = pc_station + curve_length

            result_text = f"""Simple Curve Results:\nRadius (R): {radius:.2f} m\nAngle (Δ): {central_angle_deg:.2f}°\nTangent (T): {tangent_length:.2f} m\nLength (L): {curve_length:.2f} m\nChord (C): {chord_length:.2f} m\nExternal (E): {external_distance:.2f} m\nMiddle Ordinate (M): {middle_ordinate:.2f} m\nPC: {pc_station:.2f} m\nPT: {pt_station:.2f} m\n"""

            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result_text)

            first_staking_point = math.ceil(pc_station / max_arc) * max_arc
            staking_points = [first_staking_point] if first_staking_point < pt_station else []
            
            while staking_points and staking_points[-1] + max_arc < pt_station:
                staking_points.append(staking_points[-1] + max_arc)
            
            if not staking_points or staking_points[-1] < pt_station:
                staking_points.append(pt_station)

            self.staking_data = []
            previous_point = pc_station
            total_deflection = 0

            for point_id, station in enumerate(staking_points, 1):
                arc_segment = station - previous_point
                if arc_segment <= 0:
                    continue
                    
                segment_angle_rad = arc_segment / (2 * radius)
                segment_angle_deg = math.degrees(segment_angle_rad)
                total_deflection += segment_angle_deg
                segment_chord = 2 * radius * math.sin(segment_angle_rad)

                self.staking_data.append({
                    'id': point_id,
                    'station': station,
                    'arc_length': arc_segment,
                    'deflection': segment_angle_deg,
                    'total_deflection': total_deflection,
                    'chord': segment_chord
                })
                previous_point = station

            self.update_staking_table(pc_station, pt_station, curve_length, central_angle_deg, chord_length)
            self.store_curve_parameters(radius, central_angle_rad, tangent_length, curve_length, chord_length, 
                                      external_distance, middle_ordinate, pc_station, pt_station)
            self.plot_curve()
            
        except Exception as error:
            messagebox.showerror("Calculation Error", str(error))

    def update_staking_table(self, pc_station, pt_station, curve_length, central_angle_deg, chord_length):
        self.staking_table.delete(*self.staking_table.get_children())
        self.staking_table["columns"] = ("Point", "Station", "Arc Length", "Δi (°)", "ΣΔ (°)", "Chord")
        
        for col in self.staking_table["columns"]:
            self.staking_table.heading(col, text=col)
            self.staking_table.column(col, width=100, anchor='center')

        self.staking_table.insert("", "end", values=("PC", f"{pc_station:.2f}", "0.00", "0.00", "0.00", "0.00"))
        
        for point in self.staking_data:
            is_pt = (math.isclose(point['total_deflection'], central_angle_deg / 2, abs_tol=0.5) or 
                    math.isclose(point['station'], pt_station, abs_tol=0.01))
            
            point_name = "PT" if is_pt else f"P{point['id']}"
            
            self.staking_table.insert("", "end", values=(
                point_name,
                f"{point['station']:.2f}",
                f"{point['arc_length']:.2f}",
                f"{point['deflection']:.2f}",
                f"{point['total_deflection']:.2f}",
                f"{point['chord']:.2f}"
            ))

        self.staking_table.insert("", "end", values=(
            "PT", 
            f"{pt_station:.2f}", 
            f"{curve_length:.2f}", 
            "-", 
            f"{central_angle_deg:.2f}", 
            f"{chord_length:.2f}"
        ))

    def store_curve_parameters(self, radius, central_angle, tangent, length, chord, external, middle, pc, pt):
        self.curve_radius = radius
        self.curve_angle = central_angle
        self.tangent_length = tangent
        self.curve_length = length
        self.chord_length = chord
        self.external_distance = external
        self.middle_ordinate = middle
        self.pc_station = pc
        self.pt_station = pt

    def plot_curve(self):
        try:
            self.axes.clear()
            
            radius = self.curve_radius
            central_angle = self.curve_angle
            tangent = self.tangent_length
            pc = self.pc_station
            pt = self.pt_station
            direction = self.curve_direction.get()
            azimuth = math.radians(self.azimuth.get())

            staking_stations = [pc] + [p['station'] for p in self.staking_data] + [pt]
            arc_lengths = [station - pc for station in staking_stations]
            arc_angles = [length / radius for length in arc_lengths]

            local_x = []
            local_y = []
            
            for angle in arc_angles:
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                if direction == "Left":
                    x = -x
                local_x.append(x)
                local_y.append(y)

            def rotate_point(x, y, angle):
                x_rotated = x * np.cos(-angle) - y * np.sin(-angle)
                y_rotated = x * np.sin(-angle) + y * np.cos(-angle)
                return x_rotated, y_rotated

            pc_x_local = radius if direction == "Right" else -radius
            pc_y_local = 0
            
            pt_x_local = radius * np.cos(central_angle)
            pt_y_local = radius * np.sin(central_angle)
            if direction == "Left":
                pt_x_local = -pt_x_local

            pi_x_local = radius if direction == "Right" else -radius
            pi_y_local = tangent

            pc_x, pc_y = rotate_point(pc_x_local, pc_y_local, azimuth)
            pt_x, pt_y = rotate_point(pt_x_local, pt_y_local, azimuth)
            pi_x, pi_y = rotate_point(pi_x_local, pi_y_local, azimuth)

            global_x = []
            global_y = []
            
            for x, y in zip(local_x, local_y):
                x_global, y_global = rotate_point(x, y, azimuth)
                global_x.append(x_global)
                global_y.append(y_global)

            theta = np.linspace(0, central_angle, 100)
            curve_x_local = radius * np.cos(theta)
            curve_y_local = radius * np.sin(theta)
            
            if direction == "Left":
                curve_x_local = -curve_x_local
                
            curve_x, curve_y = rotate_point(curve_x_local, curve_y_local, azimuth)
            
            self.axes.plot(curve_x, curve_y, 'b-', linewidth=2, label='Circular Curve')

            for i, (x, y) in enumerate(zip(global_x, global_y)):
                self.axes.plot(x, y, 'ro')
                point_label = 'PC' if i == 0 else ('PT' if i == len(global_x)-1 else f'P{i}')
                self.axes.text(x, y, point_label, fontsize=8, ha='right', va='bottom')

            self.axes.plot([pi_x, pc_x], [pi_y, pc_y], 'k--', label='Tangent In')
            self.axes.plot([pi_x, pt_x], [pi_y, pt_y], 'r--', label='Tangent Out')

            self.axes.plot(pi_x, pi_y, 'go', markersize=8, label='PI')
            self.axes.text(pi_x, pi_y, 'PI', fontsize=8, ha='right', va='bottom')

            self.axes.set_aspect('equal')
            self.axes.grid(True)
            self.axes.legend()
            self.axes.set_title('Simple Circular Curve')
            self.canvas.draw()
            
        except Exception as error:
            messagebox.showerror("Plotting Error", str(error))

    def get_curve_parameters(self):
        return {
            "Radius (R)": self.radius.get(),
            "Central Angle (Δ°)": self.central_angle_deg.get(),
            "Tangent (T)": self.tangent_length,
            "Length (L)": self.curve_length,
            "Chord (C)": self.chord_length,
            "External (E)": self.external_distance,
            "Middle Ordinate (M)": self.middle_ordinate,
            "PC Station": self.pc_station,
            "PT Station": self.pt_station,
            "Azimuth (°)": self.azimuth.get(),
            "Direction": self.curve_direction.get()
        }

    def export_to_excel(self):
        if not hasattr(self, 'staking_data') or not self.staking_data:
            messagebox.showwarning("Export Error", "Please calculate the curve first.")
            return
        export_excel(self.staking_data, self.get_curve_parameters(), self.figure)

    def export_to_pdf(self):
        if not hasattr(self, 'staking_data') or not self.staking_data:
            messagebox.showwarning("Export Error", "Please calculate the curve first.")
            return
        export_pdf(self.staking_data, self.get_curve_parameters(), self.figure)