# -*- coding: utf-8 -*-
# Python File Encryptor/Decryptor Tool
# Developed using CustomTkinter for a modern and attractive GUI.

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys # Used for potential debugging output to console

# Set CustomTkinter appearance and color theme
# تعيين المظهر العام والسمة اللونية لـ CustomTkinter
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

def xor_encrypt_decrypt(data: bytes, key: str) -> bytes:
    """
    Encrypts or decrypts data using the XOR cipher.
    This function performs both encryption and decryption as XOR is symmetric.

    Args:
        data (bytes): The input data (file content) as bytes.
        key (str): The secret key used for encryption/decryption.

    Returns:
        bytes: The processed (encrypted or decrypted) data as bytes.
    """
    # Encode the string key to bytes using UTF-8. This is crucial for consistency.
    # تحويل المفتاح النصي إلى بايتات باستخدام UTF-8. هذا أمر أساسي للاتساق.
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    
    # Use bytearray for mutable byte sequence to perform XOR operation efficiently.
    # استخدام bytearray لتسلسل بايتات قابل للتعديل لتنفيذ عملية XOR بكفاءة.
    result = bytearray(data)

    # Iterate through each byte of the data and apply XOR with the corresponding key byte.
    # The key is repeated (using modulo operator) if it's shorter than the data.
    # التكرار عبر كل بايت من البيانات وتطبيق XOR مع بايت المفتاح المقابل.
    # يتم تكرار المفتاح (باستخدام عامل المعامل %) إذا كان أقصر من البيانات.
    for i in range(len(result)):
        result[i] = result[i] ^ key_bytes[i % key_len]
        
    # Convert the bytearray back to immutable bytes before returning.
    # تحويل bytearray مرة أخرى إلى بايتات غير قابلة للتعديل قبل الإرجاع.
    return bytes(result)

class FileEncryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configure main window ---
        # تهيئة النافذة الرئيسية للتطبيق
        self.title("أداة تشفير وفك تشفير الملفات")
        self.geometry("650x550")
        self.resizable(False, False) # Prevent window resizing for fixed layout
        
        # Configure grid layout for the main window to allow widgets to expand
        # تهيئة تخطيط الشبكة للنافذة الرئيسية للسماح بتوسع العناصر
        self.grid_columnconfigure(0, weight=1)
        # Set row weights to control vertical distribution of widgets
        # تعيين أوزان الصفوف للتحكم في التوزيع العمودي للعناصر
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=0) # File Frame
        self.grid_rowconfigure(2, weight=0) # Key Frame
        self.grid_rowconfigure(3, weight=0) # Buttons Frame
        self.grid_rowconfigure(4, weight=1) # Status Label (will push it to bottom if space available)

        # --- Variables ---
        # Tkinter StringVars to hold dynamic data from entry widgets
        # متغيرات Tkinter StringVars للاحتفاظ بالبيانات الديناميكية من حقول الإدخال
        self.file_path_var = ctk.StringVar()
        self.key_var = ctk.StringVar()

        # --- Widgets ---

        # Main Title Label for the application
        # عنوان التطبيق الرئيسي
        self.title_label = ctk.CTkLabel(self, text="أداة تشفير وفك تشفير الملفات",
                                        font=ctk.CTkFont(size=26, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 15), sticky="n")

        # File Selection Frame: Contains file path entry and browse button
        # إطار اختيار الملف: يحتوي على حقل إدخال مسار الملف وزر الاستعراض
        self.file_frame = ctk.CTkFrame(self, corner_radius=12)
        self.file_frame.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        # Configure columns within the file frame for proper alignment
        # تهيئة الأعمدة داخل إطار الملف للمحاذاة الصحيحة
        self.file_frame.grid_columnconfigure(0, weight=0) # Label
        self.file_frame.grid_columnconfigure(1, weight=1) # Entry (expands)
        self.file_frame.grid_columnconfigure(2, weight=0) # Button

        self.file_label = ctk.CTkLabel(self.file_frame, text="مسار الملف:", font=ctk.CTkFont(size=15))
        self.file_label.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

        self.file_entry = ctk.CTkEntry(self.file_frame, textvariable=self.file_path_var,
                                       placeholder_text="الرجاء اختيار ملف...",
                                       width=350, height=38, font=ctk.CTkFont(size=13))
        self.file_entry.grid(row=0, column=1, padx=5, pady=15, sticky="ew")

        self.browse_button = ctk.CTkButton(self.file_frame, text="استعراض", command=self.browse_file,
                                          width=110, height=38, corner_radius=10,
                                          font=ctk.CTkFont(size=14, weight="bold"))
        self.browse_button.grid(row=0, column=2, padx=(10, 20), pady=15, sticky="e")

        # Key Input Frame: Contains key entry field
        # إطار إدخال المفتاح: يحتوي على حقل إدخال المفتاح
        self.key_frame = ctk.CTkFrame(self, corner_radius=12)
        self.key_frame.grid(row=2, column=0, padx=25, pady=10, sticky="ew")
        # Configure columns within the key frame
        # تهيئة الأعمدة داخل إطار المفتاح
        self.key_frame.grid_columnconfigure(0, weight=0) # Label
        self.key_frame.grid_columnconfigure(1, weight=1) # Entry (expands)

        self.key_label = ctk.CTkLabel(self.key_frame, text="المفتاح السري:", font=ctk.CTkFont(size=15))
        self.key_label.grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

        self.key_entry = ctk.CTkEntry(self.key_frame, textvariable=self.key_var,
                                      placeholder_text="أدخل المفتاح هنا...",
                                      show="*", # Hide input for security purposes
                                      width=400, height=38, font=ctk.CTkFont(size=13))
        self.key_entry.grid(row=0, column=1, padx=(10, 20), pady=15, sticky="ew")

        # Action Buttons Frame: Contains Encrypt and Decrypt buttons
        # إطار أزرار الإجراءات: يحتوي على أزرار التشفير وفك التشفير
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent") # Transparent frame for aesthetic spacing
        self.button_frame.grid(row=3, column=0, padx=25, pady=25, sticky="n")
        # Configure columns within the button frame to make buttons expand equally
        # تهيئة الأعمدة داخل إطار الأزرار لجعل الأزرار تتوسع بالتساوي
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.encrypt_button = ctk.CTkButton(self.button_frame, text="تشفير الملف", command=self.encrypt_file,
                                           width=200, height=50, corner_radius=12,
                                           font=ctk.CTkFont(size=16, weight="bold"),
                                           fg_color="#2ecc71", hover_color="#27ae60", # Green colors for encrypt
                                           compound="left", image=self._get_icon("lock_open"))
        self.encrypt_button.grid(row=0, column=0, padx=20, pady=5)

        self.decrypt_button = ctk.CTkButton(self.button_frame, text="فك تشفير الملف", command=self.decrypt_file,
                                           width=200, height=50, corner_radius=12,
                                           font=ctk.CTkFont(size=16, weight="bold"),
                                           fg_color="#e74c3c", hover_color="#c0392b", # Red colors for decrypt
                                           compound="left", image=self._get_icon("lock_closed"))
        self.decrypt_button.grid(row=0, column=1, padx=20, pady=5)

        # Status Message Label at the bottom
        # شريط رسائل الحالة في الأسفل
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13, slant="italic"), text_color="#f1c40f")
        self.status_label.grid(row=4, column=0, padx=20, pady=(15, 25), sticky="s")

    def _get_icon(self, name: str):
        """Helper to create simple icons (e.g., lock icons for buttons)."""
        # دالة مساعدة لإنشاء أيقونات بسيطة (مثل أيقونات القفل للأزرار).
        # Note: CustomTkinter typically needs PIL for image handling, but for simple shapes/emojis,
        # we can sometimes use built-in methods or just omit for simplicity.
        # For a truly robust icon system, you'd load actual image files.
        # هنا، سنبقيها فارغة لأن CustomTkinter لا يدعم SVG مباشرة أو أيقونات مدمجة بسهولة
        # بدون مكتبات إضافية مثل Pillow.
        # يمكن للمستخدمين إضافة أيقونات PNG/JPG إذا أرادوا.
        return None # Return None for now, as direct SVG/emoji icons are not natively handled by CTk.
                    # If you wish to add icons, you would use:
                    # from PIL import Image, ImageTk
                    # icon_image = ctk.CTkImage(light_image=Image.open("path/to/light_icon.png"),
                    #                           dark_image=Image.open("path/to/dark_icon.png"),
                    #                           size=(20, 20))
                    # return icon_image

    def browse_file(self):
        """
        Opens a file dialog to let the user select a file.
        Updates the file path entry and status label with the selected file's base name.
        """
        # فتح نافذة استعراض الملفات للسماح للمستخدم باختيار ملف.
        # تحديث حقل مسار الملف وشريط الحالة باسم الملف الأساسي للملف المختار.
        filepath = filedialog.askopenfilename(
            title="اختر ملفًا للتشفير أو فك التشفير",
            filetypes=(("جميع الملفات", "*.*"), ("ملفات نصية", "*.txt"), ("ملفات HTML", "*.html"))
        )
        if filepath:
            self.file_path_var.set(filepath)
            self.status_label.configure(text=f"تم اختيار الملف: {os.path.basename(filepath)}")
        else:
            self.status_label.configure(text="لم يتم اختيار أي ملف.")

    def process_file(self, operation_type: str):
        """
        Handles the core file processing logic (encryption or decryption).

        Args:
            operation_type (str): Specifies the operation, either 'encrypt' or 'decrypt'.
        """
        filepath = self.file_path_var.get()
        key = self.key_var.get()

        # Validate inputs: file path and key must not be empty
        # التحقق من صحة المدخلات: مسار الملف والمفتاح يجب ألا يكونا فارغين
        if not filepath:
            messagebox.showwarning("خطأ في الإدخال", "الرجاء اختيار ملف أولاً للمتابعة.")
            self.status_label.configure(text="خطأ: لم يتم اختيار ملف.")
            return
        if not key:
            messagebox.showwarning("خطأ في الإدخال", "الرجاء إدخال المفتاح السري قبل المعالجة.")
            self.status_label.configure(text="خطأ: لم يتم إدخال المفتاح.")
            return

        try:
            # --- Debugging Step: Verify Key Consistency ---
            # خطوة تصحيح الأخطاء: التحقق من اتساق المفتاح
            # لإزالة التعليق عن هذه السطور، احذف `#` من بدايتها.
            # ستطبع هذه السطور المفتاح المستخدم ومسار الملف في الطرفية
            # لمساعدتك في تحديد ما إذا كانت هناك مسافات زائدة أو اختلافات غير مرئية.
            print(f"DEBUG: Operation Type: {operation_type}", file=sys.stderr)
            print(f"DEBUG: Key string from input: '{key}'", file=sys.stderr)
            print(f"DEBUG: Key bytes encoded: {key.encode('utf-8')}", file=sys.stderr)
            print(f"DEBUG: File path: {filepath}", file=sys.stderr)
            # ---------------------------------------------

            # Read the entire file content as bytes. This is crucial for handling any file type
            # (text, image, executable, etc.) and for byte-level XOR operation.
            # قراءة محتوى الملف بالكامل كبايتات. هذا أمر حاسم للتعامل مع أي نوع ملف
            # (نص، صورة، قابل للتنفيذ، إلخ) ولعملية XOR على مستوى البايت.
            with open(filepath, 'rb') as f:
                original_data = f.read()

            # Perform the XOR encryption/decryption using the helper function
            # تنفيذ عملية XOR للتشفير/فك التشفير باستخدام الدالة المساعدة
            processed_data = xor_encrypt_decrypt(original_data, key)

            # Determine the output file path based on the operation type
            # تحديد مسار ملف الإخراج بناءً على نوع العملية
            if operation_type == 'encrypt':
                # For encryption, append '.enc' extension
                # للتشفير، يتم إضافة امتداد '.enc'
                output_filepath = filepath + ".enc"
                success_message = "تم تشفير الملف بنجاح!"
            else:  # decrypt
                # For decryption, try to remove '.enc' or append '.decrypted'
                # لفك التشفير، حاول إزالة '.enc' أو إضافة '.decrypted'
                if filepath.endswith(".enc"):
                    output_filepath_base = filepath[:-4] # Remove .enc
                    
                    # Ensure unique file name if a file with the base name already exists
                    # ضمان اسم ملف فريد إذا كان ملف بالاسم الأساسي موجودًا بالفعل
                    counter = 1
                    output_filepath = output_filepath_base
                    while os.path.exists(output_filepath):
                        base, ext = os.path.splitext(output_filepath_base)
                        output_filepath = f"{base}_decrypted_{counter}{ext}"
                        counter += 1
                else:
                    # If original file didn't have .enc, append .decrypted
                    # إذا لم يكن للملف الأصلي امتداد .enc، أضف .decrypted
                    output_filepath = filepath + ".decrypted"
                success_message = "تم فك تشفير الملف بنجاح!"

            # Write the processed data to the new output file in binary mode
            # كتابة البيانات المعالجة إلى ملف الإخراج الجديد في الوضع الثنائي
            with open(output_filepath, 'wb') as f:
                f.write(processed_data)

            # Update status label and show success message box
            # تحديث شريط الحالة وعرض مربع رسالة النجاح
            self.status_label.configure(text=success_message)
            messagebox.showinfo("العملية تمت بنجاح", f"{success_message}\nالملف الناتج: {os.path.basename(output_filepath)}")

            # --- Debugging Step: Compare File Sizes (Optional) ---
            # خطوة تصحيح الأخطاء: مقارنة أحجام الملفات (اختياري)
            # إذا كان حجم الملف الأصلي والمعالج متطابقين، فهذا مؤشر جيد على أن العملية تمت بشكل كامل.
            # print(f"DEBUG: Original file size: {len(original_data)} bytes", file=sys.stderr)
            # print(f"DEBUG: Processed file size: {len(processed_data)} bytes", file=sys.stderr)
            # ----------------------------------------------------

        except FileNotFoundError:
            # Handle case where the selected file does not exist
            # التعامل مع الحالة التي لا يوجد فيها الملف المختار
            messagebox.showerror("خطأ في الملف", "الملف المحدد غير موجود. الرجاء التحقق من المسار.")
            self.status_label.configure(text="خطأ: الملف غير موجود.")
        except Exception as e:
            # Catch any other unexpected errors during file processing
            # التقاط أي أخطاء أخرى غير متوقعة أثناء معالجة الملف
            messagebox.showerror("خطأ غير متوقع", f"حدث خطأ أثناء المعالجة: {e}")
            self.status_label.configure(text=f"خطأ: {e}")
            # print(f"ERROR: An unexpected error occurred: {e}", file=sys.stderr)


    def encrypt_file(self):
        """Callback function for the 'Encrypt File' button."""
        # دالة الاستدعاء لزر "تشفير الملف".
        self.process_file('encrypt')

    def decrypt_file(self):
        """Callback function for the 'Decrypt File' button."""
        # دالة الاستدعاء لزر "فك تشفير الملف".
        self.process_file('decrypt')

# Main execution block: Ensures the application runs only when the script is executed directly.
# كتلة التنفيذ الرئيسية: تضمن تشغيل التطبيق فقط عند تنفيذ السكريبت مباشرة.
if __name__ == "__main__":
    app = FileEncryptorApp()
    app.mainloop()

