import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from datetime import datetime
import os

class LectorTXT:
    def __init__(self, root):
        self.root = root
        self.root.title("Lector de Archivos .txt")
        self.root.geometry("700x600")  # Aumentado el tamaño vertical
        
        self.archivo_actual = None
        self.ruta_guardado = os.path.expanduser("~\\Documents")  # Ruta por defecto
        
        # Marco principal
        self.marco_principal = tk.Frame(self.root, padx=20, pady=20)
        self.marco_principal.pack(expand=True, fill='both')
        
        # Título
        tk.Label(self.marco_principal, 
                text="Lector y Procesador de Archivos .txt", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para codificación
        self.frame_encoding = tk.Frame(self.marco_principal)
        self.frame_encoding.pack(pady=5)
        
        # Label para codificación
        tk.Label(self.frame_encoding, 
                text="Codificación:").pack(side=tk.LEFT, padx=5)
        
        # Combobox para seleccionar codificación
        self.codificaciones = ['windows-1252', 'utf-8', 'ascii', 'latin-1', 'cp1252', 
                             'utf-16', 'utf-32', 'iso-8859-15']
        self.combo_encoding = ttk.Combobox(self.frame_encoding, 
                                         values=self.codificaciones,
                                         width=15)
        self.combo_encoding.set('windows-1252')
        self.combo_encoding.pack(side=tk.LEFT)
        
        # Botón para seleccionar archivo
        self.btn_seleccionar = tk.Button(self.marco_principal, 
                                       text="Seleccionar Archivo TXT",
                                       command=self.seleccionar_archivo,
                                       bg="#4CAF50",
                                       fg="white",
                                       pady=10)
        self.btn_seleccionar.pack(pady=20)
        
        # Campo para mostrar la ruta del archivo
        self.lbl_ruta = tk.Label(self.marco_principal, 
                                text="Ningún archivo seleccionado",
                                wraplength=500)
        self.lbl_ruta.pack(pady=10)
        
        # Área de texto para previsualización
        tk.Label(self.marco_principal, text="Previsualización:").pack()
        self.texto_preview = tk.Text(self.marco_principal, height=10)
        self.texto_preview.pack(pady=10, fill='both', expand=True)
        
        # Frame para la ruta de guardado
        self.frame_guardado = tk.Frame(self.marco_principal)
        self.frame_guardado.pack(fill='x', pady=10)
        
        # Label para mostrar la ruta de guardado
        self.lbl_ruta_guardado = tk.Label(self.frame_guardado, 
                                        text=f"Guardar en: {self.ruta_guardado}",
                                        wraplength=400)
        self.lbl_ruta_guardado.pack(side=tk.LEFT, padx=5)
        
        # Botón para cambiar ruta de guardado
        self.btn_ruta_guardado = tk.Button(self.frame_guardado,
                                         text="Cambiar",
                                         command=self.seleccionar_ruta_guardado)
        self.btn_ruta_guardado.pack(side=tk.RIGHT)
        
        # Botón para procesar y guardar
        self.btn_procesar = tk.Button(self.marco_principal,
                                    text="Procesar y Guardar CSV",
                                    command=self.procesar_archivo,
                                    bg="#2196F3",
                                    fg="white",
                                    pady=10,
                                    state='disabled')
        self.btn_procesar.pack(pady=20)

    def seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt")]
        )
        
        if archivo:
            self.archivo_actual = archivo
            self.lbl_ruta.config(text=f"Archivo seleccionado: {archivo}")
            self.btn_procesar.config(state='normal')
            self.mostrar_preview()
    
    def seleccionar_ruta_guardado(self):
        ruta = filedialog.askdirectory(
            initialdir=self.ruta_guardado,
            title="Seleccionar carpeta para guardar archivos"
        )
        if ruta:
            self.ruta_guardado = ruta
            self.lbl_ruta_guardado.config(text=f"Guardar en: {ruta}")
    
    def mostrar_preview(self):
        try:
            encoding_seleccionado = self.combo_encoding.get()
            with open(self.archivo_actual, 'r', encoding=encoding_seleccionado) as f:
                contenido = f.read(1000)  # Primeros 1000 caracteres
            self.texto_preview.delete(1.0, tk.END)
            self.texto_preview.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Error al leer el archivo con codificación {encoding_seleccionado}:\n{str(e)}")
    
    def procesar_archivo(self):
        try:
            encoding_seleccionado = self.combo_encoding.get()
            df = pd.read_csv(self.archivo_actual, 
                           encoding=encoding_seleccionado,
                           delimiter='|')  # Ajusta el delimitador según necesites
            
            # Generar nombre del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"datos_procesados_{timestamp}.csv"
            ruta_completa = os.path.join(self.ruta_guardado, nombre_archivo)
            
            # Guardar el archivo
            df.to_csv(ruta_completa, index=False, encoding=encoding_seleccionado)
            
            messagebox.showinfo("Éxito", 
                              f"Archivo procesado y guardado exitosamente en:\n{ruta_completa}")
            
            # Abrir el explorador de archivos en la carpeta donde se guardó
            os.startfile(os.path.dirname(ruta_completa))
            
        except Exception as e:
            messagebox.showerror("Error", 
                               f"Error al procesar el archivo: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LectorTXT(root)
    root.mainloop()