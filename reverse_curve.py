import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math
from exports import export_excel, export_pdf

class ReverseCurve:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback

        self.R = tk.DoubleVar(value=300)
        self.delta_deg = tk.DoubleVar(value=40)
        self.station = tk.DoubleVar(value=1500)
        self.max_arc = tk.DoubleVar(value=50)
        self.azimuth = tk.DoubleVar(value=50)
        
        self.init_ui()

    def init_ui(self):
        self.frame = tk.Frame(self.root, bg='#ecf0f1')
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(self.frame, text="Reverse Curve Design", font=('Helvetica', 20, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title.pack(pady=10)

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.input_tab = ttk.Frame(self.notebook)
        self.result_tab = ttk.Frame(self.notebook)
        self.output_tab = ttk.Frame(self.notebook)
        self.diagram_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.input_tab, text="Input")
        self.notebook.add(self.result_tab, text="Results")
        self.notebook.add(self.output_tab, text="Staking Table")
        self.notebook.add(self.diagram_tab, text="Diagram")

        self.build_input_tab()
        self.build_result_tab()
        self.build_output_tab()
        self.build_diagram_tab()

    def build_input_tab(self):
        input_frame = ttk.LabelFrame(self.input_tab, text="Input Parameters")
        input_frame.pack(padx=10, pady=10, fill='x')

        self.add_entry(input_frame, "Radius (R):", self.R, 0)
        self.add_entry(input_frame, "Deflection Angle (Δ°):", self.delta_deg, 1)
        self.add_entry(input_frame, "T1 Station (m):", self.station, 2)
        self.add_entry(input_frame, "Max Arc Length (m):", self.max_arc, 3)
        self.add_entry(input_frame, "Azimuth (°):", self.azimuth, 4)

        btns = ttk.Frame(self.input_tab)
        btns.pack(pady=10)
        ttk.Button(btns, text="Calculate", command=self.calculate).pack(side="left", padx=10)
        ttk.Button(btns, text="Help", command=self.show_help).pack(side="left", padx=10)
        ttk.Button(btns, text="Back", command=self.back_callback).pack(side="left", padx=10)
        ttk.Button(btns, text="Export Excel", command=self.export_excel).pack(side="left", padx=10)
        ttk.Button(btns, text="Export PDF", command=self.export_pdf).pack(side="left", padx=10)

    def build_result_tab(self):
        self.text = tk.Text(self.result_tab, height=15, font=('Courier', 10))
        self.text.pack(fill='both', expand=True, padx=10, pady=10)
        self.results_text = self.text

    def build_output_tab(self):
        self.tree = ttk.Treeview(self.output_tab, 
                           columns=("Point", "Station", "Arc Length", "Δi (°)", "ΣΔ", "Chord", "Curve"), 
                           show="headings")
        
        self.tree.heading("Point", text="Point")
        self.tree.heading("Station", text="Station (m)")
        self.tree.heading("Arc Length", text="Arc Length (m)")
        self.tree.heading("Δi (°)", text="Δi (°)")
        self.tree.heading("ΣΔ", text="ΣΔ")
        self.tree.heading("Chord", text="Chord (m)")
        self.tree.heading("Curve", text="Curve")
        
        self.tree.column("Point", width=60, anchor='center')
        self.tree.column("Station", width=100, anchor='center')
        self.tree.column("Arc Length", width=100, anchor='center')
        self.tree.column("Δi (°)", width=80, anchor='center')
        self.tree.column("ΣΔ", width=80, anchor='center')
        self.tree.column("Chord", width=100, anchor='center')
        self.tree.column("Curve", width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.output_tab, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

    def build_diagram_tab(self):
        fig = Figure(figsize=(6, 4))
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=self.diagram_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    def add_entry(self, parent, text, var, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, padx=5, pady=5)

    def show_help(self):
        messagebox.showinfo("Help", "Reverse Curve = Two simple curves with opposite directions.\nStaking table and diagram are computed for both curves together.")

    def calculate(self):
      try:
        R = self.R.get()
        delta_deg = self.delta_deg.get()
        delta_rad = math.radians(delta_deg)
        T1_chainage = self.station.get()
        max_arc_length = self.max_arc.get()
        azimuth_deg = self.azimuth.get()

        # Calculate curve parameters
        T = R * math.tan(delta_rad / 2)
        L1 = R * delta_rad
        L2 = R * delta_rad
        L_total = L1 + L2
        P = 2 * R * (1 - math.cos(delta_rad))

        # Calculate key stations
        E_chainage = T1_chainage + L1
        T2_chainage = E_chainage + L2

        # Display results
        results = f"""Reverse Curve Results:
Radius (R): {R:.2f} m
Angle (Δ): {delta_deg:.2f}°
Tangent (T): {T:.2f} m
Curve 1 Length (L1): {L1:.2f} m
Curve 2 Length (L2): {L2:.2f} m
Total Length (L): {L_total:.2f} m
Distance Between Tangents (P): {P:.2f} m
T1 Station: {T1_chainage:.2f} m
E Station: {E_chainage:.2f} m
T2 Station: {T2_chainage:.2f} m
"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results)

        # Clear the treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Calculate staking points for Curve 1 (Right curve)
        self.impl_data1 = []
        first_impl1 = math.ceil(T1_chainage / max_arc_length) * max_arc_length
        impl_chainages1 = [first_impl1] if first_impl1 < E_chainage else []
        while impl_chainages1 and impl_chainages1[-1] + max_arc_length < E_chainage:
            impl_chainages1.append(impl_chainages1[-1] + max_arc_length)
        if not impl_chainages1 or impl_chainages1[-1] < E_chainage:
            impl_chainages1.append(E_chainage)

        prev_chainage = T1_chainage
        cumulative_deflection = 0

        # Add T1 point
        self.tree.insert("", "end", values=(
            "T1",
            f"{T1_chainage:.2f}",
            "0.00",
            "0.00",
            "0.00",
            "0.00",
            "Curve 1"
        ))

        for i, ch in enumerate(impl_chainages1):
            arc_len = ch - prev_chainage
            if arc_len <= 0:
                continue
            delta_rad_i = arc_len / (2 * R)
            delta_deg_i = math.degrees(delta_rad_i)
            cumulative_deflection += delta_deg_i
            chord = 2 * R * math.sin(delta_rad_i)

            self.impl_data1.append({
                'id': i + 1,
                'chainage': ch,
                'arc_length': arc_len,
                'deflection': delta_deg_i,
                'cumulative_deflection': cumulative_deflection,
                'chord': chord,
                'curve': 'Curve 1'
            })

            point_name = "E" if math.isclose(ch, E_chainage, abs_tol=0.01) else f"P{i+1}"
            self.tree.insert("", "end", values=(
                point_name,
                f"{ch:.2f}",
                f"{arc_len:.2f}",
                f"{delta_deg_i:.2f}",
                f"{cumulative_deflection:.2f}",
                f"{chord:.2f}",
                "Curve 1"
            ))
            prev_chainage = ch

        # Calculate staking points for Curve 2 (Left curve)
        self.impl_data2 = []
        first_impl2 = math.ceil(E_chainage / max_arc_length) * max_arc_length
        impl_chainages2 = [first_impl2] if first_impl2 < T2_chainage else []
        while impl_chainages2 and impl_chainages2[-1] + max_arc_length < T2_chainage:
            impl_chainages2.append(impl_chainages2[-1] + max_arc_length)
        if not impl_chainages2 or impl_chainages2[-1] < T2_chainage:
            impl_chainages2.append(T2_chainage)

        prev_chainage = E_chainage
        cumulative_deflection = 0

        # Add E point
        self.tree.insert("", "end", values=(
            "E",
            f"{E_chainage:.2f}",
            "0.00",
            "0.00",
            "0.00",
            "0.00",
            "Curve 2"
        ))

        for i, ch in enumerate(impl_chainages2):
            arc_len = ch - prev_chainage
            if arc_len <= 0:
                continue
            delta_rad_i = arc_len / (2 * R)
            delta_deg_i = math.degrees(delta_rad_i)
            cumulative_deflection += delta_deg_i
            chord = 2 * R * math.sin(delta_rad_i)

            self.impl_data2.append({
                'id': len(self.impl_data1) + i + 1,
                'chainage': ch,
                'arc_length': arc_len,
                'deflection': delta_deg_i,
                'cumulative_deflection': cumulative_deflection,
                'chord': chord,
                'curve': 'Curve 2'
            })

            point_name = "T2" if math.isclose(ch, T2_chainage, abs_tol=0.01) else f"P{len(self.impl_data1)+i+1}"
            self.tree.insert("", "end", values=(
                point_name,
                f"{ch:.2f}",
                f"{arc_len:.2f}",
                f"{delta_deg_i:.2f}",
                f"{cumulative_deflection:.2f}",
                f"{chord:.2f}",
                "Curve 2"
            ))
            prev_chainage = ch

        # Update class variables
        self.R_val = R
        self.delta_deg_val = delta_deg
        self.T = T
        self.L1 = L1
        self.L2 = L2
        self.L_total = L_total
        self.P = P
        self.azimuth_deg = azimuth_deg
        self.T1_chainage = T1_chainage
        self.E_chainage = E_chainage
        self.T2_chainage = T2_chainage
        self.delta_rad = delta_rad
        azimuth_rad = math.radians(self.azimuth_deg)

        self.draw_curve()
      except Exception as e:
        messagebox.showerror("Error", str(e))
    def draw_curve(self):
      try:
        self.ax.clear()
        
        R = self.R_val
        delta_rad = self.delta_rad
        azimuth_rad = math.radians(self.azimuth_deg)

        # Calculate key points
        T1_x, T1_y = 0, 0
        I1_x = self.T * math.sin(azimuth_rad)
        I1_y = self.T * math.cos(azimuth_rad)
        
        back_azimuth = (azimuth_rad + delta_rad) % (2 * math.pi)
        I2_x = I1_x + 2 * self.T * math.sin(back_azimuth)
        I2_y = I1_y + 2 * self.T * math.cos(back_azimuth)
        
        T2_x = I2_x + self.T * math.sin(azimuth_rad)
        T2_y = I2_y + self.T * math.cos(azimuth_rad)

        # Calculate first curve (right turn)
        dir1 = azimuth_rad + math.pi / 2
        O1_x = T1_x + R * math.sin(dir1)
        O1_y = T1_y + R * math.cos(dir1)
        
        d1_start = math.atan2(T1_x - O1_x, T1_y - O1_y)
        d1_end = d1_start + delta_rad
        theta1 = np.linspace(d1_start, d1_end, 100)
        x1 = O1_x + R * np.sin(theta1)
        y1 = O1_y + R * np.cos(theta1)
        E_x, E_y = x1[-1], y1[-1]

        # Calculate second curve (left turn)
        dir2 = azimuth_rad - math.pi / 2
        O2_x = T2_x + R * math.sin(dir2)
        O2_y = T2_y + R * math.cos(dir2)
        
        d2_start = math.atan2(E_x - O2_x, E_y - O2_y)
        d2_end = d2_start - delta_rad
        theta2 = np.linspace(d2_start, d2_end, 100)
        x2 = O2_x + R * np.sin(theta2)
        y2 = O2_y + R * np.cos(theta2)

        # Draw lines
        self.ax.plot([T1_x, I1_x], [T1_y, I1_y], 'k--')
        self.ax.plot([I1_x, I2_x], [I1_y, I2_y], 'k--')
        self.ax.plot([T2_x, I2_x], [T2_y, I2_y], 'k--')
        self.ax.plot(x1, y1, 'b-', label='Curve 1')
        self.ax.plot(x2, y2, 'r-', label='Curve 2')

        # Plot key points
        self.ax.plot(T1_x, T1_y, 'go', markersize=8)
        self.ax.annotate("T1", xy=(T1_x, T1_y), xytext=(T1_x - 5, T1_y + 5))
        self.ax.plot(I1_x, I1_y, 'yo', markersize=8)
        self.ax.annotate("I1", xy=(I1_x, I1_y), xytext=(I1_x, I1_y + 5))
        self.ax.plot(E_x, E_y, 'ko', markersize=8)
        self.ax.annotate("E", xy=(E_x, E_y), xytext=(E_x, E_y + 5))
        self.ax.plot(I2_x, I2_y, 'yo', markersize=8)
        self.ax.annotate("I2", xy=(I2_x, I2_y), xytext=(I2_x, I2_y + 5))
        self.ax.plot(T2_x, T2_y, 'ro', markersize=8)
        self.ax.annotate("T2", xy=(T2_x, T2_y), xytext=(T2_x + 5, T2_y + 5))

        # Plot staking points with labels and different colors
        for p in self.impl_data1 + self.impl_data2:
            arc_len = p['arc_length']
            if arc_len <= self.L1:
                # Curve 1 points
                delta_i = arc_len / R
                theta_i = d1_start + delta_i
                x_i = O1_x + R * math.sin(theta_i)
                y_i = O1_y + R * math.cos(theta_i)
                color = 'blue'
                point_name = "E" if math.isclose(p['chainage'], self.E_chainage, abs_tol=0.01) else f"P{p['id']}"
                self.ax.plot(x_i, y_i, 'o', color=color, markersize=6, markerfacecolor='none')
                self.ax.annotate(point_name, xy=(x_i, y_i), xytext=(x_i + 1, y_i + 1), 
                           fontsize=8, color=color)
            else:
                # Curve 2 points
                arc_len2 = arc_len - self.L1
                delta_i2 = arc_len2 / R
                theta_i2 = d2_start - delta_i2
                x_i = O2_x + R * math.sin(theta_i2)
                y_i = O2_y + R * math.cos(theta_i2)
                color = 'red'
                point_name = "T2" if math.isclose(p['chainage'], self.T2_chainage, abs_tol=0.01) else f"P{p['id']}"
            
            # Plot point with different style for each curve
                self.ax.plot(x_i, y_i, 'o', color=color, markersize=6, markerfacecolor='none')
                self.ax.annotate(point_name, xy=(x_i, y_i), xytext=(x_i + 1, y_i + 1), 
                           fontsize=8, color=color)

        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_title('Reverse Curve with Staking Points')
        self.canvas.draw()

      except Exception as e:
        messagebox.showerror("Error", str(e))

    def export_excel(self):
      try:
        import pandas as pd
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", 
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        # داده‌های پارامترها
        df_params = pd.DataFrame({
            'Parameter': [
                'Radius (R)', 'Deflection Angle (Δ)', 'Tangent (T)',
                'Curve 1 Length (L1)', 'Curve 2 Length (L2)',
                'Total Length', 'Distance Between Tangents (P)',
                'Azimuth', 'T1 Station', 'E Station', 'T2 Station'
            ],
            'Value': [
                self.R_val, self.delta_deg_val, self.T,
                self.L1, self.L2, self.L_total, self.P,
                self.azimuth_deg, self.T1_chainage,
                self.E_chainage, self.T2_chainage
            ],
            'Unit': [
                'm', '°', 'm', 'm', 'm', 'm', 'm',
                '°', 'm', 'm', 'm'
            ]
        })

        # داده‌های جدول استقرار
        staking_data = self.get_staking_table_data()
        df_staking = pd.DataFrame(staking_data)

        # ذخیره در اکسل
        with pd.ExcelWriter(file_path) as writer:
            df_params.to_excel(writer, sheet_name="Parameters", index=False)
            df_staking.to_excel(writer, sheet_name="Staking Table", index=False)

        messagebox.showinfo("Success", "Excel exported successfully!")
    
      except Exception as e:
        messagebox.showerror("Error", str(e))

    def export_pdf(self):
      try:
        from matplotlib.backends.backend_pdf import PdfPages
        from tkinter import filedialog
        import matplotlib.pyplot as plt
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        # Create PDF document
        with PdfPages(file_path) as pdf:
            # Page 1: Parameters
            fig1 = plt.figure(figsize=(8, 6))
            ax1 = fig1.add_subplot(111)
            ax1.axis('off')
            
            params_text = (
                f"Reverse Curve Parameters:\n\n"
                f"Radius (R): {self.R_val:.2f} m\n"
                f"Deflection Angle (Δ): {self.delta_deg_val:.2f}°\n"
                f"Tangent (T): {self.T:.2f} m\n"
                f"Curve 1 Length (L1): {self.L1:.2f} m\n"
                f"Curve 2 Length (L2): {self.L2:.2f} m\n"
                f"Total Length: {self.L_total:.2f} m\n"
                f"Distance Between Tangents (P): {self.P:.2f} m\n"
                f"Azimuth: {self.azimuth_deg:.2f}°\n"
                f"T1 Station: {self.T1_chainage:.2f} m\n"
                f"E Station: {self.E_chainage:.2f} m\n"
                f"T2 Station: {self.T2_chainage:.2f} m"
            )
            
            ax1.text(0.1, 0.5, params_text, fontsize=10)
            pdf.savefig(fig1)
            plt.close(fig1)

            # Page 2: Staking Table
            fig2 = plt.figure(figsize=(10, 8))
            ax2 = fig2.add_subplot(111)
            ax2.axis('off')
            
            # Prepare table data
            table_data = [["Point", "Station", "Arc Length", "Δi (°)", "ΣΔ", "Chord", "Curve"]]
            staking_data = self.get_staking_table_data()
            
            for item in staking_data:
                table_data.append([
                    item['Point'],
                    f"{item['Station']:.2f}",
                    f"{item['Arc Length']:.2f}",
                    f"{item['Δi (°)']:.2f}",
                    f"{item['ΣΔ']:.2f}",
                    f"{item['Chord']:.2f}",
                    item['Curve']
                ])
            
            # Create table
            table = ax2.table(
                cellText=table_data,
                loc='center',
                cellLoc='center',
                colWidths=[0.1, 0.15, 0.15, 0.1, 0.1, 0.15, 0.1]
            )
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.2)
            
            ax2.set_title('Staking Table', pad=20)
            pdf.savefig(fig2)
            plt.close(fig2)

            # Page 3: Diagram
            self.draw_curve()  # Ensure diagram is up to date
            pdf.savefig(self.canvas.figure)

        messagebox.showinfo("Success", "PDF exported successfully!")
        
      except Exception as e:
        messagebox.showerror("Error", str(e))
    def get_staking_table_data(self):
     staking_data = []
     staking_data.append({
        'Point': 'T1',
        'Station': self.T1_chainage,
        'Arc Length': 0.0,
        'Δi (°)': 0.0,
        'ΣΔ': 0.0,
        'Chord': 0.0,
        'Curve': 'Curve 1'
    })

     for p in self.impl_data1:
        staking_data.append({
            'Point': 'E' if math.isclose(p['chainage'], self.E_chainage, abs_tol=0.01) else f"P{p['id']}",
            'Station': p['chainage'],
            'Arc Length': p['arc_length'],
            'Δi (°)': p['deflection'],
            'ΣΔ': p['cumulative_deflection'],
            'Chord': p['chord'],
            'Curve': 'Curve 1'
        })

     staking_data.append({
        'Point': 'E',
        'Station': self.E_chainage,
        'Arc Length': 0.0,
        'Δi (°)': 0.0,
        'ΣΔ': 0.0,
        'Chord': 0.0,
        'Curve': 'Curve 2'
    })
     for p in self.impl_data2:
        staking_data.append({
            'Point': 'T2' if math.isclose(p['chainage'], self.T2_chainage, abs_tol=0.01) else f"P{p['id']}",
            'Station': p['chainage'],
            'Arc Length': p['arc_length'],
            'Δi (°)': p['deflection'],
            'ΣΔ': p['cumulative_deflection'],
            'Chord': p['chord'],
            'Curve': 'Curve 2'
        })
     return staking_data