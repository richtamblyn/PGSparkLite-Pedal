#########################################
# Custom Large Font for HD44780 Displays
#########################################

class HD44780_Large_Font:
    def __init__(self, lcd):

        self.lcd = lcd

        # Create the 8 building blocks of the font
        lt_template = (
            0b00111,
            0b01111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111
        )

        self.lt = 0
        self.lcd.create_char(self.lt, lt_template)

        ub_template = (
            0b11111,
            0b11111,
            0b11111,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000
        )

        self.ub = 1
        self.lcd.create_char(self.ub, ub_template)

        rt_template = (
            0b11100,
            0b11110,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111
        )

        self.rt = 2
        self.lcd.create_char(self.rt, rt_template)

        ll_template = (
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b01111,
            0b00111
        )

        self.ll = 3
        self.lcd.create_char(self.ll, ll_template)

        lb_template = (
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b11111,
            0b11111,
            0b11111
        )

        self.lb = 4
        self.lcd.create_char(self.lb, lb_template)

        lr_template = (
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11111,
            0b11110,
            0b11100
        )

        self.lr = 5
        self.lcd.create_char(self.lr, lr_template)

        umb_template = (
            0b11111,
            0b11111,
            0b11111,
            0b00000,
            0b00000,
            0b00000,
            0b11111,
            0b11111
        )

        self.umb = 6
        self.lcd.create_char(self.umb, umb_template)

        lmb_template = (
            0b11111,
            0b00000,
            0b00000,
            0b00000,
            0b00000,
            0b11111,
            0b11111,
            0b11111
        )

        self.lmb = 7
        self.lcd.create_char(self.lmb, lmb_template)

    def write_string(self, text):

        x = 0
        space = 4

        for letter in text:

            self.lcd.cursor_pos = (0, x)

            if letter == 'A':
                self.print_A(x)
            elif letter == 'U':
                self.print_U(x)
            elif letter == '1':
                self.print_1(x)
            elif letter == '2':
                self.print_2(x)
            elif letter == '3':
                self.print_3(x)
            elif letter == '4':
                self.print_4(x)
            elif letter == '5':
                self.print_5(x)
            elif letter == '6':
                self.print_6(x)
            elif letter == '7':
                self.print_7(x)
            elif letter == '8':
                self.print_8(x)
            elif letter == '9':
                self.print_9(x)
            elif letter == '0':
                self.print_0(x)
            
            x += space

    def print_A(self, x):        
        self.lcd.write(self.lt)
        self.lcd.write(self.umb)
        self.lcd.write(self.rt)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(255)
        self.lcd.write(254)
        self.lcd.write(255)

    def print_U(self, x):
        self.lcd.write(255)
        self.lcd.write(254)
        self.lcd.write(255)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.ll)
        self.lcd.write(self.lb)
        self.lcd.write(self.lr)

    def print_1(self, x):        
        self.lcd.write(self.ub)
        self.lcd.write(self.rt)
        y = x + 1
        self.lcd.cursor_pos = (1, y)
        self.lcd.write(255)

    def print_2(self, x):
        self.lcd.write(self.umb)
        self.lcd.write(self.umb)
        self.lcd.write(self.rt)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.ll)
        self.lcd.write(self.lmb)
        self.lcd.write(self.lmb)

    def print_3(self, x):
        self.lcd.write(self.umb)
        self.lcd.write(self.umb)
        self.lcd.write(self.rt)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.lmb)
        self.lcd.write(self.lmb)
        self.lcd.write(self.lr)

    def print_4(self, x):
        self.lcd.write(self.ll)
        self.lcd.write(self.lb)
        self.lcd.write(self.rt)
        y = x + 2
        self.lcd.cursor_pos = (1, y)
        self.lcd.write(255)

    def print_5(self, x):
        self.lcd.write(255)
        self.lcd.write(self.umb)
        self.lcd.write(self.umb)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.lmb)
        self.lcd.write(self.lmb)
        self.lcd.write(self.lr)

    def print_6(self, x):
        self.lcd.write(self.lt)
        self.lcd.write(self.umb)
        self.lcd.write(self.umb)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.ll)
        self.lcd.write(self.umb)
        self.lcd.write(self.lr)

    def print_7(self, x):
        self.lcd.write(self.ub)
        self.lcd.write(self.ub)
        self.lcd.write(self.rt)
        y = x + 1
        self.lcd.cursor_pos = (1, y)
        self.lcd.write(self.lt)

    def print_8(self, x):
        self.lcd.write(self.lt)
        self.lcd.write(self.umb)
        self.lcd.write(self.rt)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.ll)
        self.lcd.write(self.lmb)
        self.lcd.write(self.lr)

    def print_9(self, x):
        self.lcd.write(self.lt)
        self.lcd.write(self.umb)
        self.lcd.write(self.rt)
        y = x + 2
        self.lcd.cursor_pos = (1, y)
        self.lcd.write(255)

    def print_0(self, x):
        self.lcd.write(self.lt)
        self.lcd.write(self.ub)
        self.lcd.write(self.rt)
        self.lcd.cursor_pos = (1, x)
        self.lcd.write(self.ll)
        self.lcd.write(self.lb)
        self.lcd.write(self.lr)