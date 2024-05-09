import csv
import pdfplumber
from tkinter import Tk, filedialog
from fpdf import FPDF
import os  # Add this line to import the os module

class PDF(FPDF):
  
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_wifi_card(self, username, password, x, y, width, height):
        # Add rectangle border
        self.rect(x, y, width, height)

        # Calculate logo position
        logo_width = min(20, width / 4)
        logo_height = logo_width
        logo_x = x + 5
        logo_y = y + 5

        # Add logo and "Welcome To ZINGSA" header
        self.image('logo.png', logo_x, logo_y, logo_width)
        self.set_xy(logo_x + logo_width + 5, logo_y)
        self.set_font('Arial', 'B', 10)
        self.cell(width - (logo_width + 10), 6, 'Welcome To ZINGSA', 0, 1)
        

        # Calculate text position
        text_x = x + 5
        text_y = logo_y + logo_height + 1

        # Add WiFi Network Name
        self.set_xy(text_x, text_y)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, '1. Connect to the following wireless network: Network', 0, 1)
       
         # Add Wifi Password
        self.set_xy(text_x, self.get_y() + 1)
        self.cell(0, 5, '2. Enter the password: T!@_zing2a', 0, 1)
            
        # Add Username
        self.set_xy(text_x, self.get_y() + 1)
        self.cell(0, 5, f'Username: {username}', 0, 1)

        # Add Password
        self.set_xy(text_x, self.get_y() + 1)
        self.cell(0, 5, f'Password: {password}', 0, 1)

        # Add Validity
        self.set_xy(text_x, self.get_y() + 1)
        self.cell(0, 5, 'Validity: 60 days after first log in', 0, 1)

def extract_credentials_from_pdf(pdf_file_path):
    credentials = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for i in range(len(lines)):
                if "Username :" in lines[i] and "Password :" in lines[i+1]:
                    username = lines[i].split(":")[1].strip()
                    password = lines[i+1].split(":")[1].strip()
                    credentials.append((username, password))
    return credentials


def write_to_csv(credentials, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password'])
        for username, password in credentials:
            writer.writerow([username, password])

def main():
    # Prompt the user to select a directory to save the files
    root = Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory()
    root.destroy()  # Destroy the main window after directory selection

    if directory_path:
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

            # CSV file path
            csv_file_path = os.path.join(directory_path, "wifi_credentials.csv")

            # Write credentials to CSV
            write_to_csv(credentials, csv_file_path)
            print(f"Credentials saved to {csv_file_path}")

            # Generate PDF with credentials
            # PDF file path
            pdf_file_path = os.path.join(directory_path, "wifi_credentials.pdf")

            # Create instance of FPDF class and set margin
            pdf = PDF()
            pdf.set_left_margin(10)
            pdf.set_right_margin(10)

            # Add a blank page to start with
            pdf.add_page()

            # Adjusted for 8 cards per page
            x_offsets = [8, 110]
            y_offsets = [8, 68, 128, 188]  # Adjust as needed for vertical spacing

            # Add WiFi cards to PDF
            for i, (username, password) in enumerate(credentials):
                if i % 8 == 0 and i != 0:
                    pdf.add_page()  # Add new page for every 8 credentials except the first
                x = x_offsets[i % 2]
                y = y_offsets[(i // 2) % len(y_offsets)]  # Ensure proper y offset for new pages
                width = 98
                height = 58
                pdf.add_wifi_card(username, password, x, y, width, height)

            # Save the PDF to a file
            pdf.output(pdf_file_path)
            print(f"PDF generated successfully at {pdf_file_path}")

        else:
            print("No PDF file selected.")
    else:
        print("No directory selected.")

if __name__ == "__main__":
    main()
