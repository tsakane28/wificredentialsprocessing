import csv
from tkinter import Tk, filedialog
from fpdf import FPDF

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

# Prompt the user to select a CSV file
root = Tk()
root.withdraw()  # Hide the main window
csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
root.destroy()  # Destroy the main window after file selection

# Read data from the CSV file
wifi_credentials = []
if csv_file_path:
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            wifi_credentials.append((row[0], row[1]))  # Assuming the first column contains usernames and the second column contains passwords

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
for i, (username, password) in enumerate(wifi_credentials):
    if i % 8 == 0 and i != 0:
        pdf.add_page()  # Add new page for every 8 credentials except the first
    x = x_offsets[i % 2]
    y = y_offsets[(i // 2) % len(y_offsets)]  # Ensure proper y offset for new pages
    width = 98
    height = 58
    pdf.add_wifi_card(username, password, x, y, width, height)

# Save the PDF to a file
pdf_file_path = "wifi_credentials.pdf"
pdf.output(pdf_file_path)
print(f"PDF generated successfully at {pdf_file_path}")