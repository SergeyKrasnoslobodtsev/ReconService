import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from client_process import ReconServiceClient

class ReconServiceGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ReconService Client")
        self.root.geometry("600x500")
        
        self.client = ReconServiceClient()
        self.current_process_id = None
        self.extraction_result = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # URL сервера
        url_frame = ttk.Frame(self.root)
        url_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(url_frame, text="URL сервера:").pack(side="left")
        self.url_var = tk.StringVar(value="http://127.0.0.1:8000")
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=40)
        url_entry.pack(side="left", padx=5)
        
        # Выбор файла
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(file_frame, text="Выбрать PDF файл", command=self.select_file).pack(side="left")
        self.file_var = tk.StringVar(value="Файл не выбран")
        ttk.Label(file_frame, textvariable=self.file_var).pack(side="left", padx=10)
        
        # Кнопки действий
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Отправить и обработать", 
                  command=self.process_document).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Заполнить документ", 
                  command=self.fill_document, state="disabled").pack(side="left", padx=5)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill="x", padx=10, pady=5)
        
        # Лог
        log_frame = ttk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ttk.Label(log_frame, text="Лог операций:").pack(anchor="w")
        
        self.log_text = tk.Text(log_frame, height=15)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите PDF файл",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.file_var.set(file_path)
            self.selected_file = file_path
    
    def process_document(self):
        if not hasattr(self, 'selected_file'):
            messagebox.showerror("Ошибка", "Выберите PDF файл")
            return
        
        self.client.base_url = self.url_var.get().rstrip('/')
        
        def worker():
            try:
                self.progress.start()
                self.log("🚀 Начинаем обработку документа")
                
                # Отправляем PDF
                process_id = self.client.send_pdf(self.selected_file)
                self.current_process_id = process_id
                self.log(f"✅ PDF отправлен. Process ID: {process_id}")
                
                # Ждем обработки
                result = self.client.wait_for_processing(process_id)
                self.extraction_result = result
                
                self.log("✅ Документ успешно обработан!")
                self.log(f"   Продавец: {result.get('seller', 'Не найден')}")
                self.log(f"   Покупатель: {result.get('buyer', 'Не найден')}")
                self.log(f"   Записей дебета: {len(result.get('debit', []))}")
                self.log(f"   Записей кредита: {len(result.get('credit', []))}")
                
                # Активируем кнопку заполнения
                self.root.after(0, lambda: self.root.children['!frame3'].children['!button2'].configure(state="normal"))
                
            except Exception as e:
                self.log(f"❌ Ошибка: {e}")
            finally:
                self.progress.stop()
        
        threading.Thread(target=worker, daemon=True).start()
    
    def fill_document(self):
        if not self.current_process_id or not self.extraction_result:
            messagebox.showerror("Ошибка", "Сначала обработайте документ")
            return
        
        def worker():
            try:
                self.progress.start()
                self.log("📝 Заполняем документ...")
                
                debit_entries = self.extraction_result.get('debit', [])
                credit_entries = self.extraction_result.get('credit', [])
                # debit_entries[3]['value'] = "ntcnsakdlaasdjlad"  # Пример изменения значения дебета
                output_path = self.client.fill_and_get_pdf(
                    self.current_process_id, debit_entries, credit_entries
                )
                
                self.log(f"🎉 Документ заполнен и сохранен: {output_path}")
                messagebox.showinfo("Успех", f"Документ сохранен:\n{output_path}")
                
            except Exception as e:
                self.log(f"❌ Ошибка заполнения: {e}")
            finally:
                self.progress.stop()
        
        threading.Thread(target=worker, daemon=True).start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ReconServiceGUI()
    app.run()