import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math
from exports import export_excel, export_pdf

class CompoundCurve:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.radius1 = tk.DoubleVar(value=200)
        self.angle1_deg = tk.DoubleVar(value=20)
        self.radius2 = tk.DoubleVar(value=300)
        self.angle2_deg = tk.DoubleVar(value=20)
        self.station_value = tk.DoubleVar(value=10000)
        self.max_arc_length = tk.DoubleVar(value=50)
        self.azimuth_deg = tk.DoubleVar(value=45)
        self.curve_direction = tk.StringVar(value="Right")

        self.init_ui()

    def init_ui(self):
        self.main_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(self.main_frame, text="Compound Curve Design", font=('Helvetica', 20, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.pack(pady=10)

        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill="both", expand=True, padx=20, pady=10)

        self.input_tab = ttk.Frame(self.tab_control)
        self.results_tab = ttk.Frame(self.tab_control)
        self.output_tab = ttk.Frame(self.tab_control)
        self.plot_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.input_tab, text="Input")
        self.tab_control.add(self.results_tab, text="Results")
        self.tab_control.add(self.output_tab, text="Staking Table")
        self.tab_control.add(self.plot_tab, text="Diagram")

        self.create_input_tab()
        self.create_results_tab()
        self.create_output_tab()
        self.create_plot_tab()

    def create_input_tab(self):
        input_frame = ttk.LabelFrame(self.input_tab, text="Input Parameters")
        input_frame.pack(padx=10, pady=10, fill='x')

        self.add_input_field(input_frame, "Radius 1 (R1):", self.radius1, 0)
        self.add_input_field(input_frame, "Angle 1 (Δ1°):", self.angle1_deg, 1)
        self.add_input_field(input_frame, "Radius 2 (R2):", self.radius2, 2)
        self.add_input_field(input_frame, "Angle 2 (Δ2°):", self.angle2_deg, 3)
        self.add_input_field(input_frame, "PI Station (m):", self.station_value, 4)
        self.add_input_field(input_frame, "Max Arc Length (m):", self.max_arc_length, 5)
        self.add_input_field(input_frame, "Azimuth (°):", self.azimuth_deg, 6)

        #ttk.Label(input_frame, text="Direction:").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        #ttk.Combobox(input_frame, textvariable=self.curve_direction, values=["Right", "Left"]).grid(row=7, column=1, padx=5, pady=5)

        button_frame = ttk.Frame(self.input_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Calculate", command=self.calculate).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Help", command=self.show_help).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Back", command=self.back_callback).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Export Excel", command=self.export_excel).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Export PDF", command=self.export_pdf).pack(side="left", padx=10)

    def create_results_tab(self):
        self.results_text = tk.Text(self.results_tab, height=15, font=('Courier', 10))
        self.results_text.pack(fill='both', expand=True, padx=10, pady=10)

    def create_output_tab(self):
        self.staking_table = ttk.Treeview(self.output_tab, 
                           columns=("Point", "Station", "ArcLength", "Deflection", "TotalDeflection", "Chord", "Curve"), 
                           show="headings")
    
        self.staking_table.heading("Point", text="Point")
        self.staking_table.heading("Station", text="Station (m)")
        self.staking_table.heading("ArcLength", text="Arc Length (m)")
        self.staking_table.heading("Deflection", text="Δi (°)")
        self.staking_table.heading("TotalDeflection", text="ΣΔ")
        self.staking_table.heading("Chord", text="Chord (m)")
        self.staking_table.heading("Curve", text="Curve")
    
        self.staking_table.column("Point", width=60, anchor='center')
        self.staking_table.column("Station", width=100, anchor='center')
        self.staking_table.column("ArcLength", width=100, anchor='center')
        self.staking_table.column("Deflection", width=80, anchor='center')
        self.staking_table.column("TotalDeflection", width=80, anchor='center')
        self.staking_table.column("Chord", width=100, anchor='center')
        self.staking_table.column("Curve", width=80, anchor='center')
    
        scrollbar = ttk.Scrollbar(self.output_tab, orient="vertical", command=self.staking_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.staking_table.configure(yscrollcommand=scrollbar.set)
    
        self.staking_table.pack(fill='both', expand=True, padx=10, pady=10)

    def create_plot_tab(self):
        plot_figure = Figure(figsize=(6, 4))
        self.plot_axes = plot_figure.add_subplot(111)
        self.plot_canvas = FigureCanvasTkAgg(plot_figure, master=self.plot_tab)
        self.plot_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def add_input_field(self, parent, label_text, variable, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, padx=5, pady=5)

    def show_help(self):
        messagebox.showinfo("Help", "Compound Curve = Two connected simple curves.\nStaking table and diagram are computed separately for each curve.\nUses traverse + azimuth method.")

    def calculate(self):
        try:
            radius1 = self.radius1.get()
            angle1_deg = self.angle1_deg.get()
            radius2 = self.radius2.get()
            angle2_deg = self.angle2_deg.get()
            PI_station = self.station_value.get()
            max_arc = self.max_arc_length.get()
            azimuth = self.azimuth_deg.get()
            direction = self.curve_direction.get()

            azimuth_rad = math.radians(azimuth)
            angle1_rad = math.radians(angle1_deg)
            angle2_rad = math.radians(angle2_deg)

            total_angle_rad = angle1_rad + angle2_rad
            if total_angle_rad > math.pi:
                messagebox.showerror("Error", "Δ1 + Δ2 > π")
                return

            tangent1 = radius1 * math.tan(angle1_rad / 2)
            tangent2 = radius2 * math.tan(angle2_rad / 2)
            length1 = radius1 * angle1_rad
            length2 = radius2 * angle2_rad
            total_length = length1 + length2

            common_tangent = tangent1 + tangent2
            tangent1_PI = common_tangent * math.sin(angle2_rad) / math.sin(total_angle_rad)
            tangent2_PI = common_tangent * math.sin(angle1_rad) / math.sin(total_angle_rad)

            total_tangent1 = tangent1 + tangent1_PI
            total_tangent2 = tangent2 + tangent2_PI

            PC_station_raw = PI_station - total_tangent1
            PC_station = math.floor(PC_station_raw / max_arc) * max_arc
            if (PC_station_raw - PC_station) > (max_arc / 2):
                PC_station += max_arc

            PC1 = PC_station
            PT1 = PC1 + length1
            PC2 = PT1
            PT2 = PC2 + length2

            result = f'''Radius 1: {radius1:.2f} m
Angle 1: {angle1_deg:.2f}°
Radius 2: {radius2:.2f} m
Angle 2: {angle2_deg:.2f}°
Tangent 1: {tangent1:.2f} m
Tangent 2: {tangent2:.2f} m
Curve 1 Length: {length1:.2f} m
Curve 2 Length: {length2:.2f} m
Total Length: {total_length:.2f} m
PC1: {PC1:.2f} m
PT1/PC2: {PT1:.2f} m
PT2: {PT2:.2f} m
'''
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, result)

            first_station1 = math.ceil(PC1 / max_arc) * max_arc
            stations1 = [first_station1] if first_station1 < PT1 else []
            while stations1 and stations1[-1] + max_arc < PT1:
                stations1.append(stations1[-1] + max_arc)
            if not stations1 or stations1[-1] < PT1:
                stations1.append(PT1)

            prev_station = PC1
            total_deflection1 = 0
            self.curve1_data = []

            for i, station in enumerate(stations1):
                arc_len = station - prev_station
                if arc_len <= 0:
                    continue
                deflection_rad = arc_len / (2 * radius1)
                deflection_deg = math.degrees(deflection_rad)
                total_deflection1 += deflection_deg
                chord = 2 * radius1 * math.sin(deflection_rad)

                self.curve1_data.append({
                    'id': i + 1,
                    'station': station,
                    'arc_length': arc_len,
                    'deflection': deflection_deg,
                    'total_deflection': total_deflection1,
                    'chord': chord,
                    'curve': 'Curve 1'
                })
                prev_station = station

            first_station2 = math.ceil(PC2 / max_arc) * max_arc
            stations2 = [first_station2] if first_station2 < PT2 else []
            while stations2 and stations2[-1] + max_arc < PT2:
                stations2.append(stations2[-1] + max_arc)
            if not stations2 or stations2[-1] < PT2:
                stations2.append(PT2)

            prev_station = PC2
            total_deflection2 = 0
            self.curve2_data = []

            for i, station in enumerate(stations2):
                arc_len = station - prev_station
                if arc_len <= 0:
                    continue
                deflection_rad = arc_len / (2 * radius2)
                deflection_deg = math.degrees(deflection_rad)
                total_deflection2 += deflection_deg
                chord = 2 * radius2 * math.sin(deflection_rad)

                self.curve2_data.append({
                    'id': i + 1,
                    'station': station,
                    'arc_length': arc_len,
                    'deflection': deflection_deg,
                    'total_deflection': total_deflection2,
                    'chord': chord,
                    'curve': 'Curve 2'
                })
                prev_station = station

            self.staking_table.delete(*self.staking_table.get_children())
            self.staking_table.insert("", "end", values=("PC1", f"{PC1:.2f}", "0.00", "0.00", "0.00", "0.00", "Curve 1"))
            for p in self.curve1_data:
                self.staking_table.insert("", "end", values=(
                    f"P{p['id']}", f"{p['station']:.2f}", f"{p['arc_length']:.2f}",
                    f"{p['deflection']:.2f}", f"{p['total_deflection']:.2f}", f"{p['chord']:.2f}", "Curve 1"
                ))
            self.staking_table.insert("", "end", values=("PT1", f"{PT1:.2f}", f"{length1:.2f}", "-", f"{angle1_deg:.2f}", "-", "Curve 1"))

            self.staking_table.insert("", "end", values=("-"*10,)*7)

            self.staking_table.insert("", "end", values=("PC2", f"{PC2:.2f}", "0.00", "0.00", "0.00", "0.00", "Curve 2"))
            for p in self.curve2_data:
                self.staking_table.insert("", "end", values=(
                    f"P{p['id']}", f"{p['station']:.2f}", f"{p['arc_length']:.2f}",
                    f"{p['deflection']:.2f}", f"{p['total_deflection']:.2f}", f"{p['chord']:.2f}", "Curve 2"
                ))
            self.staking_table.insert("", "end", values=("PT2", f"{PT2:.2f}", f"{length2:.2f}", "-", f"{angle2_deg:.2f}", "-", "Curve 2"))

            self.curve_data = self.curve1_data + self.curve2_data
            self.radius1_value = radius1
            self.angle1_deg_value = angle1_deg
            self.radius2_value = radius2
            self.angle2_deg_value = angle2_deg
            self.tangent1_value = tangent1
            self.tangent2_value = tangent2
            self.length1_value = length1
            self.length2_value = length2
            self.total_length_value = total_length
            self.azimuth_value = azimuth
            self.direction_value = direction
            self.PC_station_value = PC1
            self.PT_station_value = PT2
            self.PI_station_value = PI_station
            self.total_angle_rad_value = total_angle_rad
            self.azimuth_rad_value = azimuth_rad
            self.angle1_rad_value = angle1_rad
            self.angle2_rad_value = angle2_rad
            self.total_tangent1_value = total_tangent1
            self.total_tangent2_value = total_tangent2
            self.tangent2_PI_value = tangent2_PI

            self.draw_curve()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def draw_curve(self):
        try:
            self.plot_axes.clear()
            radius1 = self.radius1.get()
            radius2 = self.radius2.get()
            azimuth_rad = self.azimuth_rad_value
            direction = self.curve_direction.get()

            T1_x, T1_y = 0, 0

            PI_x = self.total_tangent1_value * math.sin(self.azimuth_rad_value)
            PI_y = self.total_tangent1_value * math.cos(self.azimuth_rad_value)

            back_azimuth = self.azimuth_rad_value + self.total_angle_rad_value
            T2_x = PI_x + self.total_tangent2_value * math.sin(back_azimuth)
            T2_y = PI_y + self.total_tangent2_value * math.cos(back_azimuth)

            if direction == "Right":
                dir_sign = 1
            else:
                dir_sign = -1

            dir1 = self.azimuth_rad_value + dir_sign * math.pi / 2

            t1_x = T1_x + self.tangent1_value * math.sin(self.azimuth_rad_value)
            t1_y = T1_y + self.tangent1_value * math.cos(self.azimuth_rad_value)

            t2_x = PI_x + self.tangent2_PI_value * math.sin(back_azimuth)
            t2_y = PI_y + self.tangent2_PI_value * math.cos(back_azimuth)

            dir1 = self.azimuth_rad_value + math.pi / 2
            O1_x = T1_x + radius1 * math.sin(dir1)
            O1_y = T1_y + radius1 * math.cos(dir1)

            d1_start = math.atan2(T1_x - O1_x, T1_y - O1_y)
            d1_end = d1_start + self.angle1_rad_value
            theta1 = np.linspace(d1_start, d1_end, 100)
            x1 = O1_x + radius1 * np.sin(theta1)
            y1 = O1_y + radius1 * np.cos(theta1)

            t_x, t_y = x1[-1], y1[-1]

            dir2 = d1_end - math.pi
            O2_x = t_x + radius2 * math.sin(dir2)
            O2_y = t_y + radius2 * math.cos(dir2)

            d2_start = d1_end
            d2_end = d2_start + self.angle2_rad_value
            theta2 = np.linspace(d2_start, d2_end, 100)
            x2 = O2_x + radius2 * np.sin(theta2)
            y2 = O2_y + radius2 * np.cos(theta2)

            for point in self.curve1_data:
                delta_angle = point['total_deflection'] * math.pi / 180
                angle = d1_start + delta_angle
                x_point = O1_x + radius1 * math.sin(angle)
                y_point = O1_y + radius1 * math.cos(angle)
                
                self.plot_axes.plot(x_point, y_point, 'go', markersize=6)
                self.plot_axes.annotate(f"P{point['id']}", 
                                xy=(x_point, y_point),
                                xytext=(3, 3),
                                textcoords='offset points',
                                fontsize=8,
                                color='green')

            for point in self.curve2_data:
                delta_angle = point['total_deflection'] * math.pi / 180
                angle = d2_start + delta_angle
                x_point = O2_x + radius2 * math.sin(angle)
                y_point = O2_y + radius2 * math.cos(angle)
                
                self.plot_axes.plot(x_point, y_point, 'ro', markersize=6)
                self.plot_axes.annotate(f"P{point['id']}", 
                                xy=(x_point, y_point),
                                xytext=(3, 3),
                                textcoords='offset points',
                                fontsize=8,
                                color='red')

            self.plot_axes.plot([T1_x, PI_x], [T1_y, PI_y], 'k--')
            self.plot_axes.plot([T2_x, PI_x], [T2_y, PI_y], 'k--')
            self.plot_axes.plot([t1_x, t2_x], [t1_y, t2_y], 'c--')
            self.plot_axes.plot(x1, y1, 'b-', label='curve 1')
            self.plot_axes.plot(x2, y2, 'r-', label='curve 2')
            self.plot_axes.plot(T1_x, T1_y, 'go')
            self.plot_axes.annotate("T1", xy=(T1_x, T1_y), xytext=(T1_x - 5, T1_y + 5))
            self.plot_axes.plot(PI_x, PI_y, 'ko')
            self.plot_axes.annotate("PI", xy=(PI_x, PI_y), xytext=(PI_x, PI_y + 5))
            self.plot_axes.plot(T2_x, T2_y, 'ro')
            self.plot_axes.annotate("T2", xy=(T2_x, T2_y), xytext=(T2_x + 5, T2_y + 5))
            self.plot_axes.plot(t1_x, t1_y, 'yo')
            self.plot_axes.annotate("t1", xy=(t1_x, t1_y), xytext=(t1_x - 5, t1_y + 5))
            self.plot_axes.plot(t2_x, t2_y, 'yo')
            self.plot_axes.annotate("t2", xy=(t2_x, t2_y), xytext=(t2_x + 5, t2_y + 5))
            self.plot_axes.plot(t_x, t_y, 'mo')
            self.plot_axes.annotate("t", xy=(t_x, t_y), xytext=(t_x, t_y + 5))

            self.plot_axes.set_aspect('equal')
            self.plot_axes.grid(True)
            self.plot_axes.legend()
            self.plot_canvas.draw()

        except AttributeError:
            messagebox.showerror("Error")

    def export_excel(self):
        try:
            import pandas as pd
            from tkinter import filedialog

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if not file_path:
                return

            df_params = pd.DataFrame({
                'Parameter': [
                    'R1', 'Δ1', 'R2', 'Δ2', 'T1', 'T2', 'L1', 'L2',
                    'Total Length', 'Azimuth', 'Direction', 'PC', 'PT', 'PI'
                ],
                'Value': [
                    self.radius1_value, self.angle1_deg_value, self.radius2_value, self.angle2_deg_value,
                    self.tangent1_value, self.tangent2_value, self.length1_value, self.length2_value,
                    self.total_length_value, self.azimuth_value, self.direction_value,
                    self.PC_station_value, self.PT_station_value, self.PI_station_value
                ]
            })

            df_staking = pd.DataFrame(
                [{
                    'Point': f"P{p['id']}",
                    'Station': p['station'],
                    'Arc Length': p['arc_length'],
                    'Deflection': p['deflection'],
                    'Chord': p['chord'],
                    'Curve': p['curve']
                } for p in self.curve1_data + self.curve2_data]
            )

            with pd.ExcelWriter(file_path) as writer:
                df_params.to_excel(writer, sheet_name="Parameters", index=False)
                df_staking.to_excel(writer, sheet_name="Staking Table", index=False)

            messagebox.showinfo("Success", "Excel exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_pdf(self):
        try:
            from tkinter import filedialog
            from matplotlib.backends.backend_pdf import PdfPages
            from matplotlib.figure import Figure
            import matplotlib.pyplot as plt

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                                   filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                return

            with PdfPages(file_path) as pdf:
                fig1 = Figure(figsize=(8, 6))
                ax1 = fig1.add_subplot(111)
                param_text = f'''Compound Curve Parameters:

Radius 1: {self.radius1_value:.2f} m
Angle 1: {self.angle1_deg_value:.2f}°
Radius 2: {self.radius2_value:.2f} m
Angle 2: {self.angle2_deg_value:.2f}°
Tangent 1: {self.tangent1_value:.2f} m
Tangent 2: {self.tangent2_value:.2f} m
Curve 1 Length: {self.length1_value:.2f} m
Curve 2 Length: {self.length2_value:.2f} m
Total Length: {self.total_length_value:.2f} m
Azimuth: {self.azimuth_value:.2f}°
Direction: {self.direction_value}
PC Station: {self.PC_station_value:.2f} m
PT Station: {self.PT_station_value:.2f} m
PI Station: {self.PI_station_value:.2f} m
'''
                ax1.text(0.1, 0.5, param_text, fontsize=12, va='center')
                ax1.axis('off')
                pdf.savefig(fig1, bbox_inches='tight')

                fig2 = Figure(figsize=(10, 8))
                ax2 = fig2.add_subplot(111)
                ax2.axis('off')
                
                table_data = [["Point", "Station (m)", "Arc Length (m)", "Deflection (°)", "Total Deflection (°)", "Chord (m)", "Curve"]]
                
                table_data.append([
                    "PC1", f"{self.PC_station_value:.2f}", "0.00", "0.00", "0.00", "0.00", "Curve 1"
                ])
                
                for p in self.curve1_data:
                    table_data.append([
                        f"P{p['id']}",
                        f"{p['station']:.2f}",
                        f"{p['arc_length']:.2f}",
                        f"{p['deflection']:.2f}",
                        f"{p['total_deflection']:.2f}",
                        f"{p['chord']:.2f}",
                        "Curve 1"
                    ])
                
                table_data.append([
                    "PT1", f"{self.PC_station_value + self.length1_value:.2f}", "0.00", "0.00", "0.00", "0.00", "Curve 2"
                ])
                
                for p in self.curve2_data:
                    table_data.append([
                        f"P{p['id']}",
                        f"{p['station']:.2f}",
                        f"{p['arc_length']:.2f}",
                        f"{p['deflection']:.2f}",
                        f"{p['total_deflection']:.2f}",
                        f"{p['chord']:.2f}",
                        "Curve 2"
                    ])

                table = ax2.table(cellText=table_data, loc='center', cellLoc='center', 
                                colLabels=None, colWidths=[0.1, 0.15, 0.15, 0.1, 0.1, 0.15, 0.1])
                
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 1.2)
                
                ax2.set_title('Compound Curve Staking Table', pad=20)
                
                pdf.savefig(fig2, bbox_inches='tight')

                fig3 = self.plot_canvas.figure
                pdf.savefig(fig3, bbox_inches='tight')

            messagebox.showinfo("Success", "PDF exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))