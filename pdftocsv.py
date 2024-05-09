import csv
import pdfplumber
from tkinter import Tk, filedialog

def extract_credentials_from_pdf(pdf_file_path):
    credentials = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            username = lines[2].split(":")[1].strip()
            password = lines[3].split(":")[1].strip()
            credentials.append((username, password))
    return credentials

def write_to_csv(credentials, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password'])
        for username, password in credentials:
            writer.writerow([username, password])

def main():
    # Prompt the user to select a PDF file
    root = Tk()
    root.withdraw()  # Hide the main window
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    root.destroy()  # Destroy the main window after file selection

    if pdf_file_path:
        credentials = extract_credentials_from_pdf(pdf_file_path)
        print("Extracted credentials:")
        for username, password in credentials:
            print(f"Username: {username}, Password: {password}")
        
        # Prompt the user to select a location to save the CSV file
        root = Tk()
        root.withdraw()  # Hide the main window
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        root.destroy()  # Destroy the main window after file selection

        if csv_file_path:
            write_to_csv(credentials, csv_file_path)
            print(f"Credentials saved to {csv_file_path}")
        else:
            print("No CSV file path selected.")
    else:
        print("No PDF file selected.")

if __name__ == "__main__":
    main()
