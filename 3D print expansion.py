import tkinter as tk
from tkinter import ttk, messagebox

class SlicerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Printing Expansion & Calibration Tool")
        self.root.geometry("450x480")
        self.root.configure(bg="#f5f5f7")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', font=('Helvetica', 11), background='#f5f5f7')
        style.configure('TButton', font=('Helvetica', 11, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), foreground='#333333')

        # --- Title ---
        title = ttk.Label(root, text="XY Size & Hole Compensation Calculator", style='Header.TLabel')
        title.pack(pady=15)

        # --- Frame for External / Horizontal Expansion ---
        ext_frame = ttk.LabelFrame(root, text=" Outer / Perimeter Dimensions (e.g., Calibration Cube) ", padding=15)
        ext_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(ext_frame, text="Designed / Target Width (mm):").grid(row=0, column=0, sticky="w", pady=5)
        self.ext_target = ttk.Entry(ext_frame, width=12)
        self.ext_target.grid(row=0, column=1, pady=5, padx=5)
        self.ext_target.insert(0, "20.0")

        ttk.Label(ext_frame, text="Measured Printed Width (mm):").grid(row=1, column=0, sticky="w", pady=5)
        self.ext_measured = ttk.Entry(ext_frame, width=12)
        self.ext_measured.grid(row=1, column=1, pady=5, padx=5)

        # --- Frame for Internal / Hole Expansion ---
        int_frame = ttk.LabelFrame(root, text=" Inner / Hole Dimensions (e.g., Peg Holes) ", padding=15)
        int_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(int_frame, text="Designed Hole Diameter (mm):").grid(row=0, column=0, sticky="w", pady=5)
        self.int_target = ttk.Entry(int_frame, width=12)
        self.int_target.grid(row=0, column=1, pady=5, padx=5)
        self.int_target.insert(0, "10.0")

        ttk.Label(int_frame, text="Measured Printed Diameter (mm):").grid(row=1, column=0, sticky="w", pady=5)
        self.int_measured = ttk.Entry(int_frame, width=12)
        self.int_measured.grid(row=1, column=1, pady=5, padx=5)

        # --- Calculate Button ---
        calc_btn = ttk.Button(root, text="Calculate Slicer Values", command=self.calculate)
        calc_btn.pack(pady=15)

        # --- Results Display ---
        self.result_text = tk.StringVar(value="Enter values and click Calculate")
        result_label = tk.Label(root, textvariable=self.result_text, font=('Helvetica', 11, 'italic'),
                                 bg='#e8e8ed', fg='#333333', justify="left", relief="solid", bd=1, padx=10, pady=10)
        result_label.pack(fill="x", padx=15, pady=5)

    def calculate(self):
        results = []
        
        # Calculate Outer Horizontal Expansion
        try:
            if self.ext_measured.get().strip():
                t_ext = float(self.ext_target.get())
                m_ext = float(self.ext_measured.get())
                # Slicer value = (Target - Measured) / 2
                he_val = (t_ext - m_ext) / 2
                results.append(f"Horizontal Expansion / XY Compensation: {he_val:+.4f} mm")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for outer dimensions.")
            return

        # Calculate Hole Horizontal Expansion
        try:
            if self.int_measured.get().strip():
                t_int = float(self.int_target.get())
                m_int = float(self.int_measured.get())
                # Hole values are typically calculated differently depending on the slicer
                # Cura uses direct radius adjustment for Hole Expansion: (Target - Measured) / 2
                hole_val = (t_int - m_int) / 2
                results.append(f"Hole Horizontal Expansion: {hole_val:+.4f} mm")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for hole dimensions.")
            return

        if not results:
            self.result_text.set("Please enter at least one set of measured data.")
        else:
            self.result_text.set("\n".join(results))

if __name__ == "__main__":
    root = tk.Tk()
    app = SlicerCalculator(root)
    root.mainloop()
