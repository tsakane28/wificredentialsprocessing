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
