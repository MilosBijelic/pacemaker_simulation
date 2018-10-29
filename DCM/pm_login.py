import sys
from UserInfo import UserInfo
from PyQt5.QtWidgets import QWidget, QLineEdit, QStackedWidget, QHBoxLayout, QPushButton, QApplication, QFormLayout, QLabel

class Ui_MainWindow(QWidget):

   def __init__(self):
      super(Ui_MainWindow, self).__init__()

      self.userinfo = UserInfo("userinfo.txt")
		
      self.stack1 = QWidget()
      self.stack2 = QWidget()
		
      self.main_window()
      self.parameter_window()
		
      self.Stack = QStackedWidget (self)
      self.Stack.addWidget (self.stack1)
      self.Stack.addWidget (self.stack2)
		
      hbox = QHBoxLayout(self)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.setGeometry(300, 50, 10,10)
      self.setWindowTitle('Pacemaker DCM')
      self.show()
		
   def main_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(100, 50, 100, 50)
      

      # Textboxes
      self.t_username, self.t_password = QLineEdit(), QLineEdit()
      self.t_password.setEchoMode(QLineEdit.Password)
      layout.addRow("Username:",self.t_username)
      layout.addRow("Password:",self.t_password)

      # Buttons
      b_login, b_register = QPushButton("Login"), QPushButton("Register")
      layout.addRow(b_login,b_register)

      b_login.clicked.connect(self.login)
      b_register.clicked.connect(self.register)

      # Label
      self.l_message = QLabel("                       ")
      self.l_message.setStyleSheet("font-weight:bold;color:red")
      layout.addRow(self.l_message)
      
      self.stack1.setLayout(layout)
		
   def parameter_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(100, 50, 100, 50)

      # Textboxes
      self.t_pulsewidth, self.t_pulseamplitude, self.t_heartrate, self.t_chambertopace = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
      layout.addRow("Pulse Width:",self.t_pulsewidth)
      layout.addRow("Pulse Amplitude:",self.t_pulseamplitude)
      layout.addRow("Heart Rate:",self.t_heartrate)
      layout.addRow("Chamber to Pace:",self.t_chambertopace)

      # Buttons
      b_logout, b_update = QPushButton("Logout"), QPushButton("Update")
      layout.addRow(b_logout,b_update)

      b_logout.clicked.connect(self.logout)
      b_update.clicked.connect(self.update)
      
      self.stack2.setLayout(layout)

   # Button functions	
   def login(self):
      user,password = self.t_username.text(), self.t_password.text()
      message = self.userinfo.login(user,password)
      if message == "Login successful.":
         self.Stack.setCurrentIndex(1)
      else:
         self.l_message.setText(message)
        
   def register(self):
      user,password = self.t_username.text(), self.t_password.text()
      message = self.userinfo.register(user,password)
      self.l_message.setText(message)

   def logout(self):
      self.Stack.setCurrentIndex(0)
      self.t_username.setText("")
      self.t_password.setText("")
      self.l_message.setText("")

   def update(self):
      pass
		
def main():
   app = QApplication(sys.argv)
   win = Ui_MainWindow()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
