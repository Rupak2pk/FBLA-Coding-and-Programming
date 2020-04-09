#This program was created by Rupak Kannan from FHN Class of 2021
#Hello there!
#modules
import sys
import os
import os.path
import math
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QDialogButtonBox
import mysql.connector as mysql

#Username database, I connect to the mysql database
db = mysql.connect(host = "127.0.0.1", 
                   user = "root", 
                   passwd = "root",
                   database = "username"
                   )

# the cursor is what executes a mysql command. For the list of commands check http://g2pc1.bu.edu/~qzpeng/manual/MySQL%20Commands.htm
cursor = db.cursor(buffered=True)
#Security account purposes and data transfers, kinda like a save file.
account = ""
student = ""
#Data transfer purposes
name = ""
selected_student_id = ""
location = ""
time = ""
date = ""
time_format = 0
#Im basically taking certain values from functions and "saving" them for later as a global. Then when i need them for another function I bring them up as global "X"
#The ui classes, these classes play an important role in being the GUI app. Without them, there would be no app. Most the code is just setting up the Ui and setting their geometry

#Defintions. Used for running functions that need a special code

def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

#The ui classes, these classes play an important role in being the GUI app. Without them, there would be no app. Most the code is just setting up the Ui and setting their geometry
class UILog(object):
    def __init__(self):
        global name, location, time, date, account, selected_student_id, time_format
        
        #I retrieve all the data from the selected student using their student id and account id. This ensures that I get the CORRECT student information from them.
        cursor.execute("SELECT Location FROM log WHERE student_id = %s and user_id = %s and location is not NULL", (selected_student_id[0], account[0]))
        locations = cursor.fetchall()
        location = [x[0] for x in locations]
        
        cursor.execute("SELECT time FROM log WHERE student_id = %s and user_id = %s and time is NOT NULL", (selected_student_id[0], account[0]))
        times = cursor.fetchall()
        time = [x[0] for x in times]
        
        cursor.execute("SELECT Date FROM log WHERE student_id = %s and user_id = %s and DATE is NOT NULL", (selected_student_id[0], account[0]))
        dates = cursor.fetchall()
        date = [x[0] for x in dates]
        
    def setup_Ui(self, Form):
        global time_format
        
        Form.setObjectName("Form")
        Form.resize(420, 498)
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.student_name = QtWidgets.QLabel(Form)
        self.student_name.setGeometry(QtCore.QRect(10, 140, 411, 31))
        self.student_name.setFont(font)
        self.student_name.setObjectName("student_name")
        
        self.add_hours = QtWidgets.QPushButton(Form)
        self.add_hours.setGeometry(QtCore.QRect(300, 20, 91, 31))
        self.add_hours.setFont(font)
        self.add_hours.setObjectName("AddHours")
        self.add_hours.clicked.connect(self.get_values)
        
        self.exit_button = QtWidgets.QPushButton(Form)
        self.exit_button.setGeometry(QtCore.QRect(300, 140, 91, 31))
        self.exit_button.setFont(font)
        self.exit_button.setObjectName("ExitButton")
        self.exit_button.clicked.connect(Controller.close_hour_logger)
        
        self.format_time_button = QtWidgets.QPushButton(Form)
        self.format_time_button.setGeometry(QtCore.QRect(275, 110, 141, 31))
        self.format_time_button.setFont(font)
        self.format_time_button.setObjectName("formattimebutton")
        self.format_time_button.clicked.connect(self.change_time_format)        

        self.view_info_button = QtWidgets.QPushButton(Form)
        self.view_info_button.setGeometry(QtCore.QRect(280, 80, 131, 31))
        self.view_info_button.setFont(font)
        self.view_info_button.setObjectName("View Info")
        self.view_info_button.clicked.connect(self.view_info)
        
        self.table_widget = QtWidgets.QTableWidget(Form)
        self.table_widget.setGeometry(QtCore.QRect(5, 180, 400, 271))
        #The table NEEDS rows, so it makes new rows depending on how much data needs to be placed, I used location as the placeholder
        needrows = len(location)
        self.table_widget.setRowCount(needrows)
        self.table_widget.setColumnCount(3)
        self.table_widget.setObjectName("tableWidget")
        self.table_widget.setHorizontalHeaderLabels(("Location;Hours;Date").split(";"))
        #Disables the edit ablility of a table widget
        self.table_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_widget.resetHorizontalScrollMode()
        #Adds all the data that was orginally stored in the userbase into the table
        for row in range(needrows):
            for col in [0]:
                item = QtWidgets.QTableWidgetItem(str(location[row]))
                self.table_widget.setItem(row, col, item)
             
            #If user decides how he wants see his time on the table the if and elif statement will take care of it.   
            for col in [1]:
                if time_format == 0:
                    text_min = "min"
                    mins = abs((int(time[row]) - time[row])*60)
                    
                    if mins == '' or mins == 0:
                        text_min = "" 
                        mins = ""
                    
                    elif int(mins) > 1:
                        text_min = "mins"    
                    #check ifs mins is roundable or not.   
                    try:
                        total_time = ("{} hour(s) {} {}".format(int(time[row]), normal_round(mins), text_min))
                        
                    except:
                        total_time = ("{} hour(s) {} {}".format(int(time[row]), mins, text_min))
                        
                    item = QtWidgets.QTableWidgetItem(str(total_time))
                    self.table_widget.setItem(row, col, item)
                        
                elif time_format == 1:                   
                    total_time = ("{} Hours".format(time[row]))
                    item = QtWidgets.QTableWidgetItem(str(total_time))
                    self.table_widget.setItem(row, col, item)                    
                
            for col in [2]:
                item = QtWidgets.QTableWidgetItem(str(date[row]))
                self.table_widget.setItem(row, col, item)                   
        #You may notice that the second column is different from the others and thats because that column is coded to have decimals be converted into hours and minutes using logicial math.
        
        self.delete_hours = QtWidgets.QPushButton(Form)
        self.delete_hours.setGeometry(QtCore.QRect(280, 50, 131, 31))
        self.delete_hours.setFont(font)
        self.delete_hours.setObjectName("pushButton")
        self.delete_hours.clicked.connect(self.delete_values)
        
        self.spin_hours = QtWidgets.QSpinBox(Form)
        self.spin_hours.setGeometry(QtCore.QRect(50, 30, 42, 22))
        self.spin_hours.setObjectName("spinBox")
        
        self.spin_minutes = QtWidgets.QSpinBox(Form)
        self.spin_minutes.setGeometry(QtCore.QRect(150, 30, 42, 22))
        self.spin_minutes.setObjectName("spinBox2")   
        
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 30, 61, 20))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 71, 20))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 61, 16))
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.label_8.setGeometry(QtCore.QRect(90, 30, 62, 22))
        self.label_8.setFont(font)
        
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.label_9.setFont(font)
        self.label_9.setGeometry(QtCore.QRect(30, 468, 411, 22))
        
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setObjectName("label_10")
        self.label_10.setFont(font)
        self.label_10.setGeometry(QtCore.QRect(190, 30, 72, 22))
        
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setObjectName("label_11")
        self.label_11.setFont(font)
        self.label_11.setGeometry(QtCore.QRect(10, 320, 390, 300))
        
        self.location_edit = QtWidgets.QLineEdit(Form)
        self.location_edit.setGeometry(QtCore.QRect(80, 70, 113, 20))
        self.location_edit.setObjectName("location_edit")
        
        self.date_edit = QtWidgets.QDateEdit(Form)
        self.date_edit.setGeometry(QtCore.QRect(60, 110, 110, 22))
        self.date_edit.setObjectName("date_edit")
        
        self.retranslate_Ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form) 
        
    def get_values(self):
        global account, selected_student_id, name
        location = self.location_edit.text()
        Hours = self.spin_hours.value()
        Minutes = self.spin_minutes.value()
        Date = self.date_edit.text()
        
        #if you didn't fill out anything then its not gonna go through
        if self.location_edit.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Fill out accurate logs please!")
            Fail = msg.exec() 
            
        else:
            if self.spin_hours.value() == 0 and self.spin_minutes.value() != 0:
                #inserts what was written on the line edit
                total_hours = float(Hours) + float(Minutes/60)
                cursor.execute("INSERT INTO log (Location, time, Date, student_name, user_id, student_id) VALUES (%s, %s, %s, %s, %s, %s)", (location, float(total_hours), Date, name, account[0], selected_student_id[0]))
                db.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Done")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Hours have been logged")
                execute = msg.exec()
                Controller.close_hour_logger_reset()
                Controller.open_hour_logger()
                
            elif self.spin_hours.value() == 0 and self.spin_minutes.value() == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Fill out accurate logs please!")
                Fail = msg.exec() 
                
            else:
                #inserts what was written on the line edit
                total_hours = (Hours) + (Minutes/60)
                
                cursor.execute("SELECT * FROM log WHERE Location = %s and Date = %s and student_name = %s and user_id = %s and student_id = %s", (location, Date, name, account[0], selected_student_id[0]))
                Existing_volunteer_log = cursor.fetchone()
                #if the volunteer log exists then add to the the log instead.
                
                if Existing_volunteer_log:
                    cursor.execute("SELECT time FROM log WHERE Location = %s and Date = %s and student_name = %s and user_id = %s and student_id = %s", (location, Date, name, account[0], selected_student_id[0]))
                    current_hours = cursor.fetchone()
                    new_hours = float(current_hours[0]) + total_hours
                    cursor.execute("UPDATE log SET time  = FORMAT(%s, 3) WHERE Location = %s and Date = %s and student_name = %s and user_id = %s and student_id = %s", (new_hours, location, Date, name, account[0], selected_student_id[0]))
                    db.commit()
                    msg = QMessageBox()
                    msg.setWindowTitle("Done")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Hours have been added to an existing log")
                    execute = msg.exec()                    
                    
                else:
                    cursor.execute("INSERT INTO log  (Location, time, Date, student_name, user_id, student_id) VALUES (%s, FORMAT(%s, 3), %s, %s, %s, %s)", (location, total_hours, Date, name, account[0], selected_student_id[0]))
                    db.commit()
                    msg = QMessageBox()
                    msg.setWindowTitle("Done")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Hours have been logged")
                    execute = msg.exec()                    
                    
                #Retarts the window to showcase the data that was currently added in.
                Controller.close_hour_logger_reset()
                Controller.open_hour_logger() 
                
    def delete_values(self):
        global account, selected_student_id
        value = self.table_widget.selectedItems()
        #recieves selected values
        if value == "" or len(self.table_widget.selectedItems()) != 3:
            msg = QMessageBox()
            msg.setWindowTitle("Info")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select a row on the table please!")
            Fail = msg.exec() 
            
        else:
            #converts selected values into readable text
            location = value[0].text()
            time = value[1].text()
            date = value[2].text()
            time_split = time.split(" ")
            
            try:
                time_calculate = int(time_split[0]) + (int(time_split[2])/60)
                true_total_time = round(time_calculate, 2)  
            
            except:
                true_total_time = time_split[0]
                    
            #deletes the values selected on the row from the databases,
            cursor.execute("DELETE FROM log WHERE Location = %s and time = %s and Date = %s and student_name = %s and student_id = %s and user_id = %s", (location, true_total_time, date, name, selected_student_id[0], account[0]))
            db.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Done")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Logs deleted!")
            Fail = msg.exec() 
            Controller.close_hour_logger_reset
            Controller.open_hour_logger()
            
    def view_info(self):
        value = self.table_widget.selectedItems()
        try:
            location = value[0].text()
            time = value[1].text()
            date = value[2].text()
            time_split = time.split()           
            msg = QMessageBox()
            msg.setWindowTitle("Info")
            msg.setText("{} \n{} \n{}".format(location, time, date))
            msg.exec()
            
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Info")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Select a row on the table please!")
            Fail = msg.exec() 
            
    def change_time_format(self):
        global time_format
        
        if time_format == 0:
            time_format = 1
            
        elif time_format == 1:
            time_format = 0
            
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Time Format Changed!")
        info = msg.exec()            
        Controller.close_hour_logger_reset()
        Controller.open_hour_logger()        
            
    def retranslate_Ui(self, Form):
        global name
        cursor.execute("SELECT student_id FROM log WHERE student_name = %s and student_id is NOT NULL", (name,))
        student_id = cursor.fetchone()
        cursor.execute("SELECT Grade FROM log WHERE student_name = %s and student_id is NOT NULL", (name,))
        Grade = cursor.fetchone()
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        
        #Prints the user info onto the page.
        self.student_name.setText(student_id[0] + " " + name + " " + Grade[0] + "th Grade")
        self.add_hours.setText(_translate("Form", "Add Time"))
        self.exit_button.setText(_translate("Form", "Exit"))
        self.delete_hours.setText(_translate("Form", "Delete Hours"))
        self.view_info_button.setText(_translate("Form", "Log Details"))
        
        if time_format == 0:
            self.format_time_button.setText(_translate("Form", "Hours only"))
            
        elif time_format == 1:
            self.format_time_button.setText(_translate("Form", "Hours:Minutes"))
            
        self.label_4.setText(_translate("Form", "Time"))
        self.label_5.setText(_translate("Form", "Location"))
        self.label_7.setText(_translate("Form", "Date"))
        self.label_8.setText(_translate("Form", "-Hours"))
        self.label_10.setText(_translate("Form", "-Minutes"))
        self.label_11.setText(_translate("Form", "*Click on the vertical number of a row to view more \ninformation of the chosen log."))

class UIChangeStudent(object):
    def __init__(self):
        global name, selected_student_id, account
        
    def setup_Ui(self, Dialog):
        #To help new_grade set the proper value.
        cursor.execute('SELECT Grade FROM log WHERE student_name = %s and user_id = %s', (name, account[0]))
        student_grade = cursor.fetchone()
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 226)
        self.confirm = QtWidgets.QPushButton(Dialog)
        self.confirm.setGeometry(QtCore.QRect(10, 180, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.confirm.setFont(font)
        self.confirm.setObjectName("Confirm")
        self.confirm.clicked.connect(self.edit_values)
        
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setGeometry(QtCore.QRect(280, 180, 101, 31))
        self.cancel_button.setObjectName("Cancel")
        self.cancel_button.clicked.connect(self.cancel)
        
        self.current_student = QtWidgets.QLabel(Dialog)
        self.current_student.setGeometry(QtCore.QRect(40, 23, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.current_student.setFont(font)
        self.current_student.setObjectName("current_student")
        
        self.new_student_name = QtWidgets.QLineEdit(Dialog)
        self.new_student_name.setGeometry(QtCore.QRect(100, 80, 241, 21))
        self.new_student_name.setObjectName("new_student_name")
        self.new_student_name.setText(name)
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(26, 80, 61, 20))
        self.label_2.setObjectName("label_2")
        
        self.new_grade = QtWidgets.QSpinBox(Dialog)
        self.new_grade.setGeometry(QtCore.QRect(100, 120, 42, 22))
        self.new_grade.setObjectName("new_grade")
        self.new_grade.setMinimum(9)
        self.new_grade.setMaximum(12)
        self.new_grade.setValue(int(student_grade[0]))
        
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 120, 47, 13))
        self.label_3.setObjectName("label_3")
        self.retranslate_Ui(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def edit_values(self):
        global name, selected_student_id, account
        student_name = self.new_student_name.text()                               
        Grade = self.new_grade.value()
        values = (student_name, Grade)
        #gets the current text and check if the student selected_student_id matches, then it updates the data with the new values and removes and readds the value into the student_combo_box
        cursor.execute('SELECT * FROM log WHERE student_name = %s and user_id = %s', (student_name, account[0]))
        existing_student_name = cursor.fetchone()
        cursor.execute('SELECT * FROM log WHERE student_name = %s  and student_id = %s and user_id = %s', (student_name, selected_student_id[0], account[0]))
        current_student_name_and_id = cursor.fetchone() 
        cursor.execute('SELECT grade FROM log WHERE student_name = %s and user_id = %s', (student_name, account[0]))
        current_grade = cursor.fetchone()        
        #If the student has not been changed at all, it just leaves the program.
        if current_student_name_and_id:
            #Checks if the grade changed but the student name did not change.
            if self.new_grade.value() != int(current_grade[0]):
                cursor.execute("UPDATE log SET student_name = %s, grade = %s WHERE student_id = %s and user_id = %s", (student_name, Grade, selected_student_id[0], account[0]))
                db.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Info")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Grade changed only!")
                Register_fail = msg.exec()
                Controller.close_edit_student()
                Controller.show_login_page_reset()
                Controller.show_navigation_page()                
                
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Info")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Student unchanged")
                Register_fail = msg.exec()
                Controller.close_edit_student()
                Controller.show_login_page_reset()
                Controller.show_navigation_page()
            
        #prevent student edits from having the same name as an already existing student.    
        elif existing_student_name:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Student already exists")
            Register_fail = msg.exec()
        
            
        else:   
            cursor.execute("UPDATE log SET student_name = %s WHERE student_name = %s and user_id = %s and time is NOT NULL", (student_name, name, account[0]))
            db.commit()
            #sets all the logs in the log hours to the name.
            cursor.execute("UPDATE log SET student_name = %s, grade = %s WHERE student_id = %s and user_id = %s", (student_name, Grade, selected_student_id[0], account[0]))
            db.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Done")
            msg.setIcon(QMessageBox.Information)
            msg.setText("student info updated!")
            execute = msg.exec()
            Controller.close_edit_student()
            Controller.show_login_page_reset()
            Controller.show_navigation_page()
            
    def cancel(self):
        Controller.close_edit_student()
        Controller.show_login_page_reset()
        Controller.show_navigation_page()        

    def retranslate_Ui(self, Dialog):
        global name, selected_student_id
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.confirm.setText(_translate("Dialog", "Confirm"))
        self.cancel_button.setText(_translate("Dialog", "Cancel"))
        self.current_student.setText(_translate("Dialog", name + " " + "Student Id: " + selected_student_id[0]))
        self.label_2.setText(_translate("Dialog", "New name"))
        self.label_3.setText(_translate("Dialog", "Grade"))

class UIPasswordChange(object):
    def setup_Ui(self, Form):
        global account
        cursor.execute('SELECT username FROM users WHERE id = %s', (account[0],))
        alter_username = cursor.fetchone()
        #Retrieves current username being used
              
        Form.setObjectName("Change Password Name")
        Form.resize(531, 345)
        self.username_edit = QtWidgets.QLineEdit(Form)
        self.username_edit.setGeometry(QtCore.QRect(170, 70, 261, 31))
        self.username_edit.setObjectName("username_edit")
        self.username_edit.setText(alter_username[0])
        self.username_edit.setReadOnly(True)
        
        self.password_edit = QtWidgets.QLineEdit(Form)
        self.password_edit.setGeometry(QtCore.QRect(170, 140, 261, 31))
        self.password_edit.setObjectName("password_edit")
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.confirm_password_edit = QtWidgets.QLineEdit(Form)
        self.confirm_password_edit.setGeometry(QtCore.QRect(170, 210, 261, 31))
        self.confirm_password_edit.setObjectName("confirm_password_edit")
        self.confirm_password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.confirm_button = QtWidgets.QPushButton(Form)
        self.confirm_button.setGeometry(QtCore.QRect(160, 280, 93, 28))
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.clicked.connect(self.get_values)
        
        self.see_password_button = QtWidgets.QPushButton(Form)
        self.see_password_button.setGeometry(QtCore.QRect(260, 280, 93, 28))
        self.see_password_button.setObjectName("see_password")
        self.see_password_button.clicked.connect(self.see_password)
        
        self.cancel_button = QtWidgets.QPushButton(Form)
        self.cancel_button.setGeometry(QtCore.QRect(360, 280, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.cancel)
        
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 70, 71, 20))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 140, 61, 20))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 210, 111, 20))
        self.label_3.setObjectName("label_3")
        
        self.retranslate_Ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)  
        #Gets current value of the line edits from the register fourm and sets them to new variables, the database commands check to see if the account name is already taken, if not, it inserts the new values into the table,
        
    def get_values(self):
        global account
        if self.password_edit.text() == "" or self.username_edit.text() == "" or self.confirm_password_edit.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("You're missing a field")
            Register_fail = msg.exec()   
            
        else:   
            #Gets values and changes password
            if self.password_edit.text() == self.confirm_password_edit.text():
                new_user_cred = self.username_edit.text()
                new_pass_cred = self.password_edit.text()
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setWindowTitle("Change Password")
                msgBox.setText('Are you sure you want to change your password to "{}"?'.format(new_pass_cred))
                msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                return_value = msgBox.exec()
            
                if return_value == QMessageBox.Yes:    
                    cursor.execute("SELECT student_id FROM log WHERE student_name = %s ", (name,))
                    IDs = cursor.fetchall()
                    selected_student_id = [x[0] for x in IDs]
                    cursor.execute("UPDATE users SET password = ENCODE(%s, 'secret') WHERE username = %s", (new_pass_cred, new_user_cred))
                    db.commit()
                    msg = QMessageBox()
                    msg.setWindowTitle("Done")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Success, your password was changed!")
                    Register = msg.exec() 
                    account = ""
                    Controller.close_change_password()
                    Controller.show_login_page_reset()
                                    
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Information)
                msg.setText("The passwords do not match")
                Register_fail = msg.exec() 
                
    def see_password(self):
        current_pass_cred = self.password_edit.text()
        msg = QMessageBox()
        msg.setWindowTitle(" ")
        msg.setIcon(QMessageBox.Information)
        msg.setText("{}".format(current_pass_cred))
        Register_fail = msg.exec() 
                
    def cancel(self):
        Controller.close_change_password()
        Controller.show_navigation_page()
                   
    def retranslate_Ui(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Make a new account", "Form"))
        self.confirm_button.setText(_translate("Make a new account", "Confirm"))
        self.cancel_button.setText(_translate("Make a new account", "Cancel"))
        self.see_password_button.setText(_translate("Make a new account", "See Password"))
        self.label.setText(_translate("Make a new account", "Username"))
        self.label_2.setText(_translate("Make a new account", "Password"))
        self.label_3.setText(_translate("Make a new account", "Confirm Password"))
        
class UINavigationPage(object):
    def __init__(self):        
        #I fetch all the current students in this account using the user id of said account.
        global account, student
        cursor.execute("SELECT student_name FROM log WHERE user_id = %s and student_id is NOT NULL and time is NULL and Location is NUll and Date is NULL", (account[0],))
        students = cursor.fetchall()
        student = [x[0] for x in students] 

    def setup_Ui(self, MainWindow):
        global student
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 505)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.student_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.student_combo_box.setGeometry(QtCore.QRect(50, 100, 431, 21))
        self.student_combo_box.setObjectName("student_combo_box")  
        self.student_combo_box.addItems(student)   
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 70, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.log_hour_button = QtWidgets.QPushButton(self.centralwidget)
        self.log_hour_button.setGeometry(QtCore.QRect(590, 80, 131, 41))
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.log_hour_button.setFont(font)
        self.log_hour_button.setObjectName("pushButton")
        self.log_hour_button.clicked.connect(self.add_hours_for_student)
        
        self.remove_student_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_student_button.setGeometry(QtCore.QRect(590, 200, 131, 41))
        self.remove_student_button.setFont(font)
        self.remove_student_button.setObjectName("pushButton_2")
        self.remove_student_button.clicked.connect(self.remove_values)
        
        self.add_student_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_student_button.setGeometry(QtCore.QRect(360, 370, 131, 41))
        self.add_student_button.setFont(font)
        self.add_student_button.setObjectName("pushButton_3")
        self.add_student_button.clicked.connect(self.get_values)
        
        self.view_report_button = QtWidgets.QPushButton(self.centralwidget)
        self.view_report_button.setGeometry(QtCore.QRect(590, 120, 131, 41))
        self.view_report_button.setFont(font)
        self.view_report_button.setObjectName("pushButton_4")
        self.view_report_button.clicked.connect(self.print_values)
        
        self.log_out_button = QtWidgets.QPushButton(self.centralwidget)
        self.log_out_button.setGeometry(QtCore.QRect(590, 280, 131, 41))
        self.log_out_button.setFont(font)
        self.log_out_button.setObjectName("pushButton_5")
        self.log_out_button.clicked.connect(Controller.show_login_page_reset)
        
        self.edit_student_button = QtWidgets.QPushButton(self.centralwidget)
        self.edit_student_button.setGeometry(QtCore.QRect(590, 160, 131, 41))
        self.edit_student_button.setFont(font)
        self.edit_student_button.setObjectName("pushButton_2")
        self.edit_student_button.clicked.connect(self.edit_student_details)
        
        self.change_user_password_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_user_password_button.setGeometry(QtCore.QRect(580, 240, 151, 41))
        self.change_user_password_button.setFont(font)
        self.change_user_password_button.setObjectName("pushButton_5")
        self.change_user_password_button.clicked.connect(Controller.change_password)
        
        self.open_readme_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_readme_button.setGeometry(QtCore.QRect(740, 10, 40, 41))
        self.open_readme_button.setFont(font)
        self.open_readme_button.setObjectName("pushButton_7")
        self.open_readme_button.clicked.connect(self.open_readme)
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(520, 370, 211, 21))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 400, 191, 16))
        
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(520, 430, 221, 16))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        
        self.student_line_edit = QtWidgets.QLineEdit(MainWindow)
        self.student_line_edit.setGeometry(QtCore.QRect(110, 370, 211, 20))
        self.student_line_edit.setObjectName("student_line_edit")
        
        self.label_5 = QtWidgets.QLabel(MainWindow)  
        self.label_5.setGeometry(QtCore.QRect(40, 370, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label")
        
        self.student_id_edit = QtWidgets.QLineEdit(MainWindow)
        self.student_id_edit.setGeometry(QtCore.QRect(110, 400, 113, 20))
        self.student_id_edit.setObjectName("student_id_edit")
        self.onlyInt = QtGui.QIntValidator()
        self.student_id_edit.setValidator(self.onlyInt) 
        
        self.label_6 = QtWidgets.QLabel(MainWindow)
        self.label_6.setGeometry(QtCore.QRect(20, 400, 101, 21))
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_2")
        
        self.label_7 = QtWidgets.QLabel(MainWindow)
        self.label_7.setGeometry(QtCore.QRect(40, 430, 71, 21))
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_3")
        
        self.grade_box = QtWidgets.QSpinBox(MainWindow)
        self.grade_box.setGeometry(QtCore.QRect(110, 430, 50, 30))
        self.grade_box.setObjectName("grade_box")
        self.grade_box.setMinimum(9)
        self.grade_box.setMaximum(12)  

        MainWindow.setCentralWidget(self.centralwidget)      
        self.retranslate_Ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow) 
        
    def get_values(self):
        global account
        
        if self.student_line_edit.text() == "" or self.student_id_edit.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Fill all of the student lines please!")
            Fail = msg.exec() 
            
        else:
            #retrieves text from line edit
            student_name = self.student_line_edit.text()
            student_id = self.student_id_edit.text()
            Grade = self.grade_box.value()
            cursor.execute('SELECT * FROM log WHERE student_id = %s and user_id = %s', (student_id, account[0]))
            existing_student_id = cursor.fetchone()
            cursor.execute('SELECT * FROM log WHERE student_name = %s and user_id = %s', (student_name, account[0]))
            existing_student = cursor.fetchone()
            #check to see if the student exists or if the student selected_student_id exists
            
            if existing_student_id:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Student already exists")
                Fail = msg.exec()
                
            elif existing_student:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Student already exists on your account. Try adjusting the name")
                Fail = msg.exec() 
                
            else:
                #if it passes all the if and elif statements then the values can be inserted into the datatable
                cursor.execute("INSERT INTO log (user_id, student_id, student_name, Grade) VALUES (%s, %s, %s, %s)", (account[0], student_id, student_name, Grade))
                db.commit()
                cursor.execute("SELECT student_name FROM log WHERE user_id = %s and student_id = %s ", (account[0], student_id))
                entries = cursor.fetchall()
                entry = [x[0] for x in entries]
                self.student_combo_box.addItem(entry[0])
                #entry is added
                self.student_line_edit.setText("")
                self.student_id_edit.setText("")
                msg = QMessageBox()
                msg.setWindowTitle("Done")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Student has been added")
                execute = msg.exec()   
                
    def remove_values(self):
        #checks to see the current value of the line edit and then checks if that current value exists in the database, if it does then it removes the value entirely
        global account
        index = self.student_combo_box.currentIndex()  
        name = self.student_combo_box.currentText()
        if name == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("No user to remove")
            Register_fail = msg.exec() 
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Remove student?")
            msgBox.setWindowTitle("Are you sure?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            return_value = msgBox.exec()
            
            if return_value == QMessageBox.Yes:    
                cursor.execute("SELECT student_id FROM log WHERE student_name = %s ", (name,))
                IDs = cursor.fetchall()
                selected_student_id = [x[0] for x in IDs]
                
                try:
                    cursor.execute("DELETE FROM log WHERE student_id = %s", (selected_student_id[0],))
                    db.commit()
                    cursor.execute("DELETE FROM log WHERE student_name = %s and user_id = %s", (name, account[0]))
                    db.commit()
                    self.student_combo_box.removeItem(index)
                    self.student_line_edit.setText("")
                    self.student_id_edit.setText("")
                    msg = QMessageBox()
                    msg.setWindowTitle("Done")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Student has been removed")
                    execute = msg.exec()
                    
                except:
                    #there was a really weird glitch/error where the data for a student was removed but the student would still be on the student_combo_box, so I simply made some sort of error handler that closes the page and reopens it.
                    Controller.show_login_page_reset()
                    Controller.show_navigation_page()
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Something must of went wrong")
                    execute = msg.exec()   
                    
    def add_hours_for_student(self):
        #opens the hour log, it allows the name variable to get the name value from the combotext in order to be used to fetch data from the database. Its why this one is soooo special
        global name, selected_student_id
        name = self.student_combo_box.currentText()
        cursor.execute("SELECT student_id FROM log WHERE student_name = %s and user_id = %s and student_id is NOT NULL", (name, account[0]))
        selected_student_id = cursor.fetchone()
        
        if name == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("No Student available")
            Fail = msg.exec()  
            
        else:
            Controller.open_hour_logger()
            
    def edit_student_details(self):
        #similar to the add hours for student funciton above except for editing students.
        global name, selected_student_id
        name = self.student_combo_box.currentText()
        cursor.execute("SELECT student_id FROM log WHERE student_name = %s and user_id = %s and student_id is NOT NULL", (name, account[0]))
        selected_student_id = cursor.fetchone()
        
        if name == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("No Student available")
            Fail = msg.exec()
            
        else:
            Controller.open_edit_student()   
            
    def print_values(self):
        #used for getting reports such as total hours or catergories or etc.
        name = self.student_combo_box.currentText()
        global account
        if name == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("No Student exist yet, be sure to add more students to get your report!")
            Fail = msg.exec()   
            
        else:
            cursor.execute("SELECT time FROM log WHERE student_name = %s and user_id = %s and time is NOT NULL", (name, account[0]))
            Logss = cursor.fetchall()
            cursor.execute('SELECT time FROM log WHERE user_id = %s and time is NOT NULL', (account[0],))
            #calculating total hours for all students, I put two ss for the tuples.
            total_account_hourss = cursor.fetchall()
            total_account_hours = [x[0] for x in total_account_hourss]
            Min_total = str((sum(total_account_hours) - int(sum(total_account_hours)))*60)
            #calculating total hours for current student
            Logs = [x[0] for x in Logss]
            min_log_total = str(((sum(Logs) - int(sum(Logs)))*60))
            
            if sum(Logs) >= 50 and sum(Logs) < 200 :
                Catergory = "CSA Community"
                
            elif sum(Logs) >= 200 and sum(Logs) < 500 :
                Catergory = "CSA Service"
                
            elif sum(Logs) >= 500:
                Catergory = "CSA Achivement"
                
            else:
                Catergory = "N/A"
                
            msg = QMessageBox()
            msg.setWindowTitle("Your report")
            Text = ("Total time for current student: {} Hours {} Minutes \nTotal time for all students: {} Hours {} Minutes \nCatergory for current student: {}".format(int(sum(Logs)), int(float(min_log_total)), int(sum(total_account_hours)), int(float(Min_total)), Catergory))
            msg.setText(Text)
            Report = msg.exec()            
            
    def open_readme(self):
        try:
            os.system("notepad.exe README.txt")
            
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Note")
            Text = ("Help file does not exist. Please redownload the file or move the file into the same directory")
            msg.setText(Text)
            info = msg.exec()                   
           
    def retranslate_Ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Be sure to check out fbla-pbl.org!"))
        self.label.setText(_translate("MainWindow", "Select Student:"))
        self.log_hour_button.setText(_translate("MainWindow", "Log Hours"))
        self.remove_student_button.setText(_translate("MainWindow", "Remove Student"))
        self.add_student_button.setText(_translate("MainWindow", "Add student"))
        self.view_report_button.setText(_translate("MainWindow", "View Report"))
        self.log_out_button.setText(_translate("MainWindow", "Log out"))
        self.edit_student_button.setText(_translate("MainWindow", "Edit Student"))
        self.open_readme_button.setText(_translate("MainWindow", "Help"))
        self.change_user_password_button.setText(_translate("MainWindow", "Change Password"))
        self.label_2.setText(_translate("MainWindow", "CSA Community = 50 Hours "))
        self.label_3.setText(_translate("MainWindow", "CSA Service = 200 Hours"))
        self.label_4.setText(_translate("MainWindow", "CSA Achivement = 500 Hours"))
        self.label_5.setText(_translate("MainWindow", "Student:"))
        self.label_6.setText(_translate("MainWindow", "Student ID:"))
        self.label_7.setText(_translate("MainWindow", "Grade"))  

class UIRegisterForm(object):
    def setup_Ui(self, Form):
        Form.setObjectName("Form")
        Form.resize(531, 345)
        self.username_edit = QtWidgets.QLineEdit(Form)
        self.username_edit.setGeometry(QtCore.QRect(170, 70, 261, 31))
        self.username_edit.setObjectName("username_edit")
        
        self.password_edit = QtWidgets.QLineEdit(Form)
        self.password_edit.setGeometry(QtCore.QRect(170, 140, 261, 31))
        self.password_edit.setObjectName("password_edit")
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.confirm_password_edit = QtWidgets.QLineEdit(Form)
        self.confirm_password_edit.setGeometry(QtCore.QRect(170, 210, 261, 31))
        self.confirm_password_edit.setObjectName("confirm_password_edit")
        self.confirm_password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.confirm_button = QtWidgets.QPushButton(Form)
        self.confirm_button.setGeometry(QtCore.QRect(160, 280, 93, 28))
        self.confirm_button.setObjectName("confirm_button")
        self.confirm_button.clicked.connect(self.get_values)
        
        self.see_password_button = QtWidgets.QPushButton(Form)
        self.see_password_button.setGeometry(QtCore.QRect(260, 280, 93, 28))
        self.see_password_button.setObjectName("see_password")
        self.see_password_button.clicked.connect(self.see_password)
        
        self.cancel_button = QtWidgets.QPushButton(Form)
        self.cancel_button.setGeometry(QtCore.QRect(360, 280, 93, 28))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.cancel)
        
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 70, 71, 20))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(90, 140, 61, 20))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 210, 111, 20))
        self.label_3.setObjectName("label_3")
        self.retranslate_Ui(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)  
        #Gets current value of the line edits from the register fourm and sets them to new variables, the database commands check to see if the account name is already taken, if not, it inserts the new values into the table,
        
    def get_values(self):
        if self.password_edit.text() == "" or self.username_edit.text() == "" or self.confirm_password_edit.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setIcon(QMessageBox.Information)
            msg.setText("You're missing a field")
            Register_fail = msg.exec()   
            
        else:   
            #Gets values and creates a brand new account 
            if self.password_edit.text() == self.confirm_password_edit.text():
                new_user_cred = self.username_edit.text()
                new_pass_cred = self.password_edit.text()
                values = (new_user_cred, new_pass_cred)
                cursor.execute('SELECT * FROM users WHERE username = %s', (new_user_cred, ))
                existing_user_account = cursor.fetchone()
                #Checks if the user exists in the first place.
                if existing_user_account:
                    msg = QMessageBox()
                    msg.setWindowTitle("Error")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Account already taken!")
                    Register_fail = msg.exec()
                    
                else:
                    query = "INSERT INTO users (username, password) VALUES (%s, ENCODE(%s, 'secret'))"
                    cursor.execute(query, values)
                    db.commit()
                    msg = QMessageBox()
                    msg.setWindowTitle("Nice!")
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Success, your username is" + " " + new_user_cred)
                    Register = msg.exec() 
                    Controller.close_register_window()
                    Controller.show_login_page()
                    
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setIcon(QMessageBox.Information)
                msg.setText("The passwords do not match")
                Register_fail = msg.exec() 
                
    def see_password(self):
        current_pass_cred = self.password_edit.text()
        msg = QMessageBox()
        msg.setWindowTitle(" ")
        msg.setIcon(QMessageBox.Information)
        msg.setText("{}".format(current_pass_cred))
        Register_fail = msg.exec()     
                
    def cancel(self):
        Controller.close_register_window()
        Controller.show_login_page()        
                   
    def retranslate_Ui(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Make a new account", "Form"))
        self.confirm_button.setText(_translate("Make a new account", "Confirm"))
        self.cancel_button.setText(_translate("Make a new account", "Cancel"))
        self.see_password_button.setText(_translate("Make a new account", "See Password"))
        self.label.setText(_translate("Make a new account", "Username"))
        self.label_2.setText(_translate("Make a new account", "Password"))
        self.label_3.setText(_translate("Make a new account", "Confirm Password"))
        
#Main Window setup.   
class UILoginWindow(object):
    def setup_Ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.login_line = QtWidgets.QLineEdit(self.centralwidget)
        self.login_line.setGeometry(QtCore.QRect(260, 310, 241, 31))
        self.login_line.setObjectName("location_edit")
        self.login_line.setPlaceholderText('Username')
        
        self.password_line = QtWidgets.QLineEdit(self.centralwidget)
        self.password_line.setGeometry(QtCore.QRect(260, 340, 241, 31))
        self.password_line.setObjectName("lineEdit_2")
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setPlaceholderText('Password')
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 320, 81, 19))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 350, 71, 20))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(260, 250, 251, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 50, 351, 201))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("fbla_logo"))
        self.label_4.setObjectName("label_4")
        
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(240, 390, 88, 27))
        self.login_button.setObjectName("pushButton")
        self.login_button.clicked.connect(self.handle_login)
        
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(335, 390, 88, 27))
        self.register_button.setObjectName("pushButton_2")
        self.register_button.clicked.connect(Controller.open_register_window)
        
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(430, 390, 88, 27))
        self.cancel_button.setObjectName("pushButton_3")
        self.cancel_button.clicked.connect(app.quit)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 761, 26))
        self.menu_bar.setObjectName("menu_bar")
        MainWindow.setMenuBar(self.menu_bar)
        
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        
        self.retranslate_Ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslate_Ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Have you done your fair share for the community?"))
        self.label.setText(_translate("MainWindow", "Username:"))
        self.label_2.setText(_translate("MainWindow", "Password:"))
        self.login_button.setText(_translate("MainWindow", "Login"))
        self.register_button.setText(_translate("MainWindow", "Register"))
        self.cancel_button.setText(_translate("MainWindow", "Exit"))
        self.label_3.setText(_translate("MainWindow", "            Community Service Awards   "))
        
        #handles login by decoding the passwords, checking to see if its correct, then encoding it back.    
    def handle_login(self):
        global account
        login_name = self.login_line.text()
        login_pass = self.password_line.text()
        cursor.execute("UPDATE users SET password = DECODE(password, 'secret')")
        cursor.execute('SELECT * FROM users WHERE BINARY username = %s and BINARY password = %s', (login_name, login_pass))
        account = cursor.fetchone()   
        #Checks for the proper account
        if account:            
            Controller.show_navigation_page()
            
        else:
            self.login_failed()
            
        cursor.execute("UPDATE users SET password = ENCODE(password, 'secret')") 
        
    def login_failed(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Invalid credentials")
        Login_Fail = msg.exec() 
        
#Controller function acts as a nagivator for the windows, whenever a button is clicked on the functions, one of the controller's definitions will activate. it prevents the nonexistent varibale errors from happening. A true hero indeed.
#Note: All Controller functions are written the same. The self.X.show() is named differently to seperate from the other variable names I used.
class Controller:
    def __init__(self):
        pass
    
    def show_login_page(self):
        self.Loginpage = QtWidgets.QMainWindow()
        self.ui = UILoginWindow()
        self.ui.setup_Ui(self.Loginpage)
        self.Loginpage.show()
        
    def show_navigation_page(self):
        self.Navigationpage = QtWidgets.QMainWindow()
        self.ui = UINavigationPage()
        self.ui.setup_Ui(self.Navigationpage)
        self.Loginpage.hide()
        self.Navigationpage.show() 
        
    def show_login_page_reset(self):
        #The purpose of this function is that it makes it possible to switch between the MainWindows without a non existent variable error.
        self.Loginpage = QtWidgets.QMainWindow()
        self.ui = UILoginWindow()
        self.ui.setup_Ui(self.Loginpage)
        self.Navigationpage.close()
        self.Loginpage.show()   
        
    def open_register_window(self):
        self.Register = QtWidgets.QMainWindow()
        self.ui = UIRegisterForm()
        self.ui.setup_Ui(self.Register)
        self.Register.setWindowTitle("Make a new account")
        self.Register.show()
        self.Loginpage.close()
        
    def close_register_window(self):
        self.Register.close()
        self.Loginpage.show()
        
    def open_hour_logger(self):
        self.HourLogger = QtWidgets.QMainWindow()
        self.ui = UILog()
        self.ui.setup_Ui(self.HourLogger)
        self.HourLogger.setWindowTitle("Be proud of yourself for getting some work done!")
        self.HourLogger.show()
        self.Navigationpage.close()
        
    def close_hour_logger(self):
        self.Navigationpage = QtWidgets.QMainWindow()
        self.ui = UINavigationPage()
        self.ui.setup_Ui(self.Navigationpage)        
        self.HourLogger.close()
        self.Navigationpage.show()

    def close_hour_logger_reset(self):
        #Same purpose, hour logger couldn't be reclosed without a variable error after once. This functino exists to counter this situation
        self.HourLogger.close()
        
    def open_edit_student(self):
        self.EditStudent = QtWidgets.QDialog()
        self.ui = UIChangeStudent()
        self.ui.setup_Ui(self.EditStudent)
        self.EditStudent.setWindowTitle("Edit")  
        self.EditStudent.show()
        self.Navigationpage.close()
        
    def close_edit_student(self):
        self.EditStudent.close()
        self.Navigationpage.show()
        
    def change_password(self):
        self.ChangePassword = QtWidgets.QMainWindow()
        self.ui = UIPasswordChange()
        self.ui.setup_Ui(self.ChangePassword)
        self.ChangePassword.show()
        self.Navigationpage.close()
    
    def close_change_password(self):
        self.ChangePassword.close()
        self.Navigationpage.show()

#Reset functions are meant to help the program reopen a window without a nonexist variable existing, this allows the function to the open the window if the user decides to press cancel or changes his mind.        
        
#The purpose of this function is to run the program. When the program's name is "main" it runs itself.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Windows')
    Controller = Controller()
    Controller.show_login_page()        
    sys.exit(app.exec_())
    