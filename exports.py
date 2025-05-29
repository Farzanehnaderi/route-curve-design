import pandas as pd
from tkinter import filedialog, messagebox
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from matplotlib.figure import Figure

def export_excel(data, params, figure):
    try:
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return

        # پارامترها در شیت اول
        df_params = pd.DataFrame(params.items(), columns=["Parameter", "Value"])

        # جدول پیاده‌سازی در شیت دوم
        df_table = pd.DataFrame(data)

        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            df_params.to_excel(writer, sheet_name='Parameters', index=False)
            df_table.to_excel(writer, sheet_name='Staking Table', index=False)

            # ذخیره تصویر نمودار
            image_stream = BytesIO()
            figure.savefig(image_stream, format='png')
            image_stream.seek(0)

            workbook = writer.book
            worksheet = writer.sheets['Staking Table']
            worksheet.insert_image('H2', 'curve.png', {'image_data': image_stream})

        messagebox.showinfo("Export", "Excel exported successfully.")

    except Exception as e:
        messagebox.showerror("Export Error", str(e))

def export_pdf(data, params, figure):
    try:
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not path:
            return

        pdf = PdfPages(path)

        # صفحه 1: پارامترها
        fig1 = Figure(figsize=(8, 10))
        ax1 = fig1.add_subplot(111)
        ax1.axis("off")
        text = "\n".join([f"{k}: {v}" for k, v in params.items()])
        ax1.text(0.05, 0.95, text, fontsize=12, verticalalignment='top')
        pdf.savefig(fig1)

        # صفحه 2: جدول
        fig2 = Figure(figsize=(8, 10))
        ax2 = fig2.add_subplot(111)
        ax2.axis("off")
        table_text = "\n".join([
            f"{i+1}. {row}" for i, row in enumerate(pd.DataFrame(data).to_string(index=False).split('\n'))
        ])
        ax2.text(0.05, 0.95, table_text, fontsize=8, verticalalignment='top', family='monospace')
        pdf.savefig(fig2)

        # صفحه 3: خود نمودار
        pdf.savefig(figure)

        pdf.close()
        messagebox.showinfo("Export", "PDF exported successfully.")

    except Exception as e:
        messagebox.showerror("Export Error", str(e))

