🔒 File Encryptor/Decryptor Tool
A simple and effective tool for encrypting and decrypting files using the XOR algorithm, designed with an attractive and professional user interface using the CustomTkinter library in Python. This project aims to demonstrate an understanding of encryption fundamentals, file handling, and GUI development.

✨ Features
Attractive Graphical User Interface (GUI): Designed using CustomTkinter for a modern, dark-themed appearance.

Simple Encryption and Decryption: Utilizes the efficient and easy-to-understand XOR algorithm for cryptographic operations.

Binary File Support: Capable of encrypting and decrypting any file type (text, images, videos, etc.) as it processes data at the byte level.

File Path Management: Easy selection of input files and saving of output results.

Key Security: The secret key input field hides its content for security during typing.

Clear Status Messages: Provides immediate feedback to the user regarding the success or failure of an operation.

🚀 Technologies Used
Python 3.x: The primary programming language.

CustomTkinter: For building the graphical user interface (GUI).

os Module: For interacting with the file system (e.g., reading and writing files).

tkinter.filedialog, tkinter.messagebox: For file dialogs and displaying user messages.

⚙️ Installation and Setup
To run this application on your machine, follow these steps:

Clone the Repository:

git clone https://github.com/YourUsername/File-Encryptor-Decryptor.git
cd File-Encryptor-Decryptor

(Note: Replace YourUsername with your GitHub username, and ensure you create the repository first).

Install Dependencies:
This project relies on the CustomTkinter library. You can install it using pip:

pip install customtkinter

Run the Application:
After installation, you can launch the application from your Terminal or Command Prompt:

python encryptor_app_new.py

📝 How to Use
Select a File: Click the "Browse" button to choose the file you want to encrypt or decrypt.

Enter the Secret Key: In the "Secret Key" field, enter the key you will use for the operation.

Important Note: The key used for decryption must be exactly the same as the key used for encryption (case-sensitive, including spaces and symbols).

Choose the Operation:

To Encrypt: Click the "Encrypt File" button. A new file will be created with the same original filename but with a .enc extension added (e.g., my_document.txt.enc).

To Decrypt: Click the "Decrypt File" button. If the file ends with .enc, this extension will be removed. Otherwise, .decrypted will be appended (e.g., my_document.txt or my_image.png.decrypted).

Verify the Result: The output file will be saved in the same directory as the original file. A confirmation message will appear with the new file's name.

⚠️ Security Note
The XOR Cipher algorithm used in this project is very simple and suitable for educational purposes and understanding basic encryption principles. It is not recommended for protecting sensitive or critical data in production environments, as it is vulnerable to various analytical attacks. The goal of this project is to demonstrate the ability to apply fundamental programming and security concepts.

💡 Potential Future Enhancements
Add support for stronger encryption algorithms (e.g., AES) using dedicated Python cryptography libraries (like cryptography).

Implement a progress bar for operations on large files.

Allow users to manually specify the output file path and name.

Improve error handling and add logging for events.

This project demonstrates my skills in GUI development, file handling, and applying fundamental security concepts, making it a valuable addition to my IT resume.