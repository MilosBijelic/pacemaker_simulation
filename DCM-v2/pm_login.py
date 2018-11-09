import sys
from UserInfo import UserInfo
from PyQt5.QtWidgets import QWidget, QLineEdit, QStackedWidget, QHBoxLayout, QPushButton, QApplication, QFormLayout, QLabel

# for egram
from RealTimePlot import CustomFigCanvas
import threading
import keyboard
stop = False

class Ui_MainWindow(QWidget):

   def __init__(self):
      super(Ui_MainWindow, self).__init__()

      self.userinfo = UserInfo("userinfo.txt")

      self.figure = Figure()
		
      self.stack1 = QWidget()
      self.stack2 = QWidget()
      self.stack3 = QWidget()
		
      self.init_main_window()
      self.init_parameter_window()
      self.init_egram_window()
		
      self.Stack = QStackedWidget (self)
      self.Stack.addWidget (self.stack1)
      self.Stack.addWidget (self.stack2)
      self.Stack.addWidget (self.stack3)
		
      hbox = QHBoxLayout(self)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.setGeometry(300, 50, 500, 300)
      self.setWindowTitle('Pacemaker DCM')
      self.show()

# ---- Init Functions
   def init_main_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(100, 50, 100, 50)
      

      # Textboxes
      self.t_username, self.t_password = QLineEdit("Alexander"), QLineEdit("sWB2PP!d")
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
		
   def init_parameter_window(self):
      
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

   def init_egram_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(0, 0, 0, 0)

      # matplotlib figure
      self.figure = CustomFigCanvas((0,175), (-5,5), 5,5, 75)
      layout.addRow(self.figure)

      # Buttons
      back, start = QPushButton("Back"), QPushButton("Start")
      layout.addRow(back, start)

      back.clicked.connect(self.back)
      start.clicked.connect(self.start)
      
      self.stack3.setLayout(layout)

# ----  Button Functions	
   def login(self):
      user,password = self.t_username.text(), self.t_password.text()

      if user == '' or password == '':
         message = "The fields cannot be empty."
      else:
         message = self.userinfo.login(user,password)
         
      if message == "Login successful.":
         self.Stack.setCurrentIndex(1)
      else:
         self.l_message.setText(message)
        
   def register(self):
      user,password = self.t_username.text(), self.t_password.text()

      if user == '' or password == '':
         message = "The fields cannot be empty."
      else:
         message = self.userinfo.register(user,password)
         
      self.l_message.setText(message)

   def logout(self):
      self.Stack.setCurrentIndex(0)
      self.t_username.setText("")
      self.t_password.setText("")
      self.l_message.setText("")
      
   def update(self):
      self.Stack.setCurrentIndex(2)
   
   def back(self):
      global stop
      stop = True
      self.t1.join()

      self.figure.y = self.figure.n * 0.0

      self.Stack.setCurrentIndex(1)

   def start(self):
      global stop
      stop = False

      self.t1 = threading.Thread(target = dataSendLoop, daemon = True, args = (self.addData_callback,)) # setting daemon to True kills the thread when the main thread exits.
      self.t1.start()

   def addData_callback(self, val1, val2):
      self.figure.add_data(val1,val2)
      
# ---- For egram multithreading
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal((float,float))

def dataSendLoop(addData_callback):
    global stop
    
    # Setup the signal-slot mechanism.
    source = Communicate()
    source.data_signal.connect(addData_callback)

    # Simulate some data
    n = np.linspace(0, 499, 500)
    y = (np.sin(n/8.3)) - np.cos(n/12.3) + 2*np.sin(n/5) * np.cos(n/10)
    i = 0

    while(not stop):
        if i >=499:
           i=0
        time.sleep(0.01)

        #source.data_signal.emit(y[i]) 
        source.data_signal.emit(keyboard.is_pressed('1'),keyboard.is_pressed('2')) 

        i += 1

# ---- Main
def main():
   app = QApplication(sys.argv)
   win = Ui_MainWindow()

   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
