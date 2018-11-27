import sys
from UserInfo import UserInfo
from PyQt5.QtWidgets import QWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QStackedWidget, QHBoxLayout, QGridLayout, QPushButton, QButtonGroup, QRadioButton, QApplication, QFormLayout, QLabel
from PyQt5.QtGui import QIntValidator
import PyQt5.QtCore as QtCore

from serial_pm_dcm import pacemaker_serial_comm as serial
from sim_egram import sim_egram

from matplotlib.figure import Figure

# for egram
from RealTimePlot import CustomFigCanvas
import threading
import numpy as np
import time

# used to control multithreading
stop = False   # set to True kills the thread
start = False  # set to True when the thread is running
bpm = 60       # displayed on the egram

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
      self.Stack.addWidget(self.stack1)
      self.Stack.addWidget(self.stack2)
      self.Stack.addWidget(self.stack3)
		
      hbox = QHBoxLayout(self)
      hbox.addWidget(self.Stack)

      self.setLayout(hbox)
      self.setGeometry(300, 50, 750, 400)
      self.setWindowTitle('Pacemaker DCM')
      self.show()

# ---- Init Functions
   def init_main_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(300,150,300,150) # left,top,right,bottom
      

      # - Textboxes
      self.t_username, self.t_password = QLineEdit("test_user"), QLineEdit("pass")
      self.t_password.setEchoMode(QLineEdit.Password)
      layout.addRow("Username:", self.t_username)
      layout.addRow("Password:", self.t_password)

      # - Buttons
      b_login, b_register = QPushButton("Login"), QPushButton("Register")
      layout.addRow(b_login,b_register)

      b_login.clicked.connect(self.login)
      b_register.clicked.connect(self.register)

      # - Label
      self.l_message = QLabel("                       ")
      self.l_message.setStyleSheet("font-weight:bold;color:red")
      layout.addRow(self.l_message)
      
      self.stack1.setLayout(layout)
		
   def init_parameter_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(300,150,300,150) # left,top,right,bottom

      # - Parameters

      # heart rate
      self.sb_heartrate = QSpinBox()
      self.sb_heartrate.setRange(30,175)

      container = Wrapper((self.sb_heartrate,QLabel(("(bpm)"))))
      layout.addRow("Heart Rate:",container);

      # chamber to pulse
      rbg_chambertopulse = QButtonGroup()
      self.rb_ctp_A = QRadioButton("A")
      rbg_chambertopulse.addButton(self.rb_ctp_A)
      self.rb_ctp_V = QRadioButton("V")
      rbg_chambertopulse.addButton(self.rb_ctp_V)

      container = Wrapper((self.rb_ctp_A,self.rb_ctp_V))
      layout.addRow("Chamber to Pulse: ",container);

      # pulse width
      self.sb_pulsewidth = QDoubleSpinBox()
      self.sb_pulsewidth.setRange(0.1,1.9)
      self.sb_pulsewidth.setDecimals(1)
      self.sb_pulsewidth.setSingleStep(0.1)

      container = Wrapper((self.sb_pulsewidth,QLabel(("(msec)"))))
      layout.addRow("Pulse Width:",container);
      
      # pulse amplitude
      self.sb_pulseamplitude = QDoubleSpinBox()
      self.sb_pulseamplitude.setRange(0.5,7.0)
      self.sb_pulseamplitude.setDecimals(1)
      self.sb_pulseamplitude.setSingleStep(0.1)
      
      container = Wrapper((self.sb_pulseamplitude,QLabel(("(V)"))))
      layout.addRow( "Pulse Amplitude:",container);

      # chamber to sense
      rbg_chambertosense = QButtonGroup()
      self.rb_cts_A = QRadioButton("A")
      rbg_chambertosense.addButton(self.rb_cts_A)
      self.rb_cts_V = QRadioButton("V")
      rbg_chambertosense.addButton(self.rb_cts_V)
      self.rb_cts_none = QRadioButton("None")
      rbg_chambertosense.addButton(self.rb_cts_none)

      container = Wrapper((self.rb_cts_A,self.rb_cts_V,self.rb_cts_none))
      layout.addRow("Chamber to Sense: ",container);
      
      # ventricular sensitivity
      self.sb_ventricularsensitivity = QDoubleSpinBox()
      self.sb_ventricularsensitivity.setRange(1,10)
      self.sb_ventricularsensitivity.setDecimals(1)
      self.sb_ventricularsensitivity.setSingleStep(0.1)

      container = Wrapper((self.sb_ventricularsensitivity,QLabel(("(mV)"))))
      layout.addRow("Ventricular Sensitivity: ",container);

      # atrial sensitivity
      rbg_atrialsensitivity = QButtonGroup()
      self.rb_as_25= QRadioButton("0.25")
      rbg_atrialsensitivity.addButton(self.rb_as_25)
      self.rb_as_50 = QRadioButton("0.50")
      rbg_atrialsensitivity.addButton(self.rb_as_50)
      self.rb_as_75 = QRadioButton("0.75")
      rbg_atrialsensitivity.addButton(self.rb_as_75)

      container = Wrapper((self.rb_as_25,self.rb_as_50,self.rb_as_75,QLabel("(mV)")))
      layout.addRow("Atrial Sensitivity: ",container);

      # rate adaption
      rbg_rateadaption = QButtonGroup()
      self.rb_ra_on= QRadioButton("On")
      rbg_rateadaption.addButton(self.rb_ra_on)
      self.rb_ra_off = QRadioButton("Off")
      rbg_rateadaption.addButton(self.rb_ra_off)

      container = Wrapper((self.rb_ra_on,self.rb_ra_off)) 
      layout.addRow("Rate Adaption: ",container);

      # Medium Activity Threshold
      self.sb_mediumactivitythreshold = QSpinBox()
      self.sb_mediumactivitythreshold.setRange(0,500)

      container = Wrapper((self.sb_mediumactivitythreshold,))
      layout.addRow("Medium Activity Threshold: ",container)

      # High Activity Threshold
      self.sb_highactivitythreshold = QSpinBox()
      self.sb_highactivitythreshold.setRange(0,500)

      container = Wrapper((self.sb_highactivitythreshold,))
      layout.addRow("High Activity Interval: ",container)

      # Reaction Time
      self.sb_reactiontime = QSpinBox()
      self.sb_reactiontime.setRange(10,50)

      container = Wrapper((self.sb_reactiontime,QLabel("(s)")))
      layout.addRow("Reaction Time: ",container)

      # Recovery Time
      self.sb_recoverytime = QSpinBox()
      self.sb_recoverytime.setRange(2,16)

      container = Wrapper((self.sb_recoverytime,QLabel("(min)")))
      layout.addRow("Recovery Time: ",container)

      # hysterisis
      rbg_hysteris = QButtonGroup()
      self.rb_h_on= QRadioButton("On")
      rbg_hysteris.addButton(self.rb_ra_on)
      self.rb_h_off = QRadioButton("Off")
      rbg_hysteris.addButton(self.rb_ra_off)

      container = Wrapper((self.rb_h_on,self.rb_h_off)) 
      layout.addRow("Hysterisis: ",container);

      # hysterisis interval
      self.sb_hysterisisinterval = QSpinBox()
      self.sb_hysterisisinterval.setRange(200,500)

      container = Wrapper((self.sb_hysterisisinterval,QLabel(("(msec)"))))
      layout.addRow("Hysterisis Interval: ",container);

      # vrp
      self.sb_vrp = QSpinBox()
      self.sb_vrp.setRange(150,500)

      container = Wrapper((self.sb_vrp, QLabel("(msec)")));
      layout.addRow("VRP: ", container)

      # arp
      self.sb_arp = QSpinBox()
      self.sb_arp.setRange(150,500)

      container = Wrapper((self.sb_arp, QLabel("(msec)")));
      layout.addRow("ARP: ", container)
      
      # - Set default parameter values
      self.param_set_default()

      # - Buttons
      b_logout, b_update, b_egram = QPushButton("Logout"), QPushButton("Update"), QPushButton("Show Electrogram")
      container = Wrapper((b_logout, b_update, b_egram))
      layout.addRow(container)

      b_logout.clicked.connect(self.logout)
      b_update.clicked.connect(self.update)
      b_egram.clicked.connect(self.show_egram)

      self.rb_ctp_A.clicked.connect(self.check_chamber_pulse)
      self.rb_ctp_V.clicked.connect(self.check_chamber_pulse)
      self.rb_cts_A.clicked.connect(self.check_chamber_sense)
      self.rb_cts_V.clicked.connect(self.check_chamber_sense)
      
      self.stack2.setLayout(layout)

   def param_set_default(self):
      self.sb_heartrate.setValue(60)
      self.rb_ctp_V.setChecked(True)
      self.sb_pulsewidth.setValue(0.4)
      self.sb_pulseamplitude.setValue(3.5)
      self.rb_cts_none.setChecked(True)
      self.sb_ventricularsensitivity.setValue(2.5)
      self.rb_as_75.setChecked(True)
      self.rb_ra_off.setChecked(True)
      self.sb_mediumactivitythreshold.setValue(0)
      self.sb_highactivitythreshold.setValue(0)
      self.sb_reactiontime.setValue(10)
      self.sb_recoverytime.setValue(2)
      self.rb_h_off.setChecked(True)
      self.sb_hysterisisinterval.setValue(300)
      self.sb_vrp.setValue(320)
      self.sb_arp.setValue(250)

   def init_egram_window(self):
      
      layout = QFormLayout()
      layout.setContentsMargins(30, 30, 30, 30) # left,top,right,bottom

      # matplotlib figure
      self.figure = CustomFigCanvas((0,175), (-2,4), 5,5, 75)
      layout.addRow(self.figure)

      # - Buttons
      back, start = QPushButton("Back"), QPushButton("Start")
      layout.addRow(back, start)

      back.clicked.connect(self.back)
      start.clicked.connect(self.start)
      
      self.stack3.setLayout(layout)

# ---- Get Functions

   # Returns a list of parameters if all parameters are within acceptable range
   # Returns an error message if not


   def get_parameters(self):

      # Read values
      heartrate               = int(self.sb_heartrate.value())
      chambertopulse          = 0 if self.rb_ctp_A.isChecked() else (\
                                1 if self.rb_ctp_V.isChecked() else 'P')
      pulsewidth              = int(self.sb_pulsewidth.value() * 10)
      pulseamplitude          = int(self.sb_pulseamplitude.value() * 10)
      chambertosense          = 0 if self.rb_cts_none.isChecked() else (\
                                1 if self.rb_cts_V.isChecked() else (\
                                2 if self.rb_cts_A.isChecked() else 'S'))
      ventricularsensitivity  = int(self.sb_ventricularsensitivity.value() * 10)
      atrialsensitivity       = 25 if self.rb_cts_A.isChecked() else (\
                                50 if self.rb_cts_V.isChecked() else (\
                                75 if self.rb_cts_none.isChecked() else ''))
      rateadaptation          = 1 if self.rb_ra_on.isChecked() else (\
                                0 if self.rb_ra_off.isChecked() else '')
      mediumthreshold         = self.sb_mediumactivitythreshold.value()
      highthreshold           = self.sb_highactivitythreshold.value()
      reactiontime            = self.sb_reactiontime.value()
      recoverytime            = self.sb_recoverytime.value()
      hysterisis              = 1 if self.rb_h_on.isChecked() else (\
                                0 if self.rb_h_off.isChecked() else 'H')
      hysterisisinterval      = self.sb_hysterisisinterval.value() // 2
      vrp                     = self.sb_vrp.value() // 2
      arp                     = self.sb_arp.value() // 2
      

      return [22,
              85,
              0,
              heartrate,               # byte 4
              chambertopulse,          # byte 5
              pulsewidth,              # byte 6
              mediumthreshold,         # byte 7
              pulseamplitude,          # byte 8
              highthreshold,           # byte 9
              chambertosense,          # byte 10
              ventricularsensitivity,  # byte 11
              0,                       # byte 12 (free)
              atrialsensitivity,       # byte 13
              rateadaptation,          # byte 14 
              hysterisis,              # byte 15
              hysterisisinterval,      # byte 16
              reactiontime,            # byte 17 
              vrp,                     # byte 18
              recoverytime,            # byte 19 
              arp]                     # byte 20  

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

      
      self.param_set_default()   
      self.l_message.setText(message)

   def logout(self):
      self.Stack.setCurrentIndex(0)
      self.t_username.setText("")
      self.t_password.setText("")
      self.l_message.setText("")
      
   def update(self):
      global bpm
      bpm = int(self.sb_heartrate.value())
      
      par = self.get_parameters()
      print("Sent:\t", bytearray(par))
      serial(bytearray(par))

      a = bytearray(par)
      print( [ i for i in a ] )

   def show_egram(self):
      self.Stack.setCurrentIndex(2)
      
   def back(self):
      global stop, start
      
      if start:
         stop = True    # kills thread
         start = False
         self.t1.join() 

         self.figure.y = self.figure.n * 0.0
         
      self.Stack.setCurrentIndex(1)

   def start(self):
      global stop, start
      
      if start:
         print("Cannot start multiple threads.")
         return 
      
      stop = False
      start = True
      
      self.t1 = threading.Thread(target = dataSendLoop, daemon = True, args = (self.addData_callback,)) # setting daemon to True kills the thread when the main thread exits.
      self.t1.start()

   # ensures that pulse and sense are in the same mode at all times
   def check_chamber_pulse(self):
      if self.rb_cts_none.isChecked():
         return
      if (self.rb_ctp_A.isChecked()):
         self.rb_cts_A.setChecked(True)
      elif (self.rb_ctp_V.isChecked()):
         self.rb_cts_V.setChecked(True)

   def check_chamber_sense(self):
      if (self.rb_cts_A.isChecked()):
         self.rb_ctp_A.setChecked(True)
      elif (self.rb_cts_V.isChecked()):
         self.rb_ctp_V.setChecked(True)
      
      
# ---- For egram multithreading

   def addData_callback(self, val):
      self.figure.add_data(val)
      
class Communicate(QtCore.QObject):
    data_signal = QtCore.pyqtSignal((float))

def dataSendLoop(addData_callback):
    global stop, bpm
    
    # Setup the signal-slot mechanism.
    source = Communicate()
    source.data_signal.connect(addData_callback)

    # Simulate some data
    n,y = sim_egram(bpm)
    
    y = 5*y # scale values since sim_egram returns values <1
    
    i = 0
    while(not stop):
        if i >= len(n)-1:
           i=0
           
        time.sleep(0.01)

        source.data_signal.emit(y[i]) 

        i += 1

# ---- PyQt Helpers

# Wraps a list of PyQt5 widgets into a single widget
def Wrapper(widgets):
   layout = QGridLayout()
   layout.setSpacing(5)

   for i in range(0,len(widgets)):
            layout.addWidget(widgets[i],0,i)
   
   re = QWidget()
   re.setLayout(layout)
   return re

   

# ---- Main
def main():
   app = QApplication(sys.argv)
   win = Ui_MainWindow()

   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
