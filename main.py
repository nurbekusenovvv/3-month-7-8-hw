from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.uic import loadUi
import sys 
import sqlite3

connect = sqlite3.connect("dodo.db")

connect.execute("""CREATE TABLE IF NOT EXISTS real(
    name VARCHAR(22),
    surname VARCHAR(22),
    number INTEGER(33),
    addres VARCHAR(33),
    food VARCHAR(44)
    
    )""")
connect.commit()





class MenuWindow(QWidget):
    def __init__(self):
        super(MenuWindow, self).__init__()
        loadUi('menu.ui', self)
        print("Ok")

class AdminPanelWindow(QWidget):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi('adminpanel.ui',self)


class AdminWindow(QWidget):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi('admin.ui', self)
        self.confirm.clicked.connect(self.check_password)
        # self.next.clicked.connect(self.show_admin_panel)
        
        
    def show_admin_panel(self):
        admin_panel = AdminPanelWindow()
        admin_panel.show()
       
        
    def check_password(self):
        get_password = self.password.text()
        
        if get_password == "geeks":
            self.show_admin_panel()
        else:
            self.result.setText("Incorrect")
    # def show_admin_pamel(self):
    #     self.admin_panel.show()
            

        
    
    
    

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.menu_window = MenuWindow()
        self.admin_window = AdminWindow()
        self.hide_input_order()
        self.order.clicked.connect(self.send_order)
        self.send.clicked.connect(self.send_order)
        self.menu.clicked.connect(self.show_menu_window)
        self.admin.clicked.connect(self.show_admin_window)

    def show_menu_window(self):
        self.menu_window.show()

    def show_admin_window(self):
        self.admin_window.show()

    def hide_input_order(self):
        self.name.hide()
        self.surname.hide()
        self.number.hide()
        self.addres.hide()
        self.food.hide()
        self.send.hide()

    def show_input_order(self):
        self.name.show()
        self.surname.show()
        self.number.show()
        self.addres.show()
        self.food.show()
        self.send.show()

    def send_order(self):
        self.show_input_order()
        get_name = self.name.text()
        get_surname = self.surname.text()
        get_number = self.number.text()
        get_addres = self.addres.text()
        get_food = self.food.text()
        # get_chatid = self.chatid.text()
        connect.execute(f"INSERT INTO real VALUES ('{get_name}','{get_surname}','{get_number}','{get_addres}','{get_food}')")
        connect.commit()
        # print(get_name, get_surname, get_number, get_addres, get_food)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()