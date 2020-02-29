
Hello! I see you have questions regarding the Program.py file or the FBLA application.

Most of the details of how the code works is in the py file which I will put with the application, they are marked in green.

*NOTE: THE PROGRAM WILL NOT RUN UNTIL YOU CLOSE THIS WINDOW.

HOW TO RUN THE APPLICATION
--------------------------
In order to run the application, make sure you have at least Python 3.7 installed onto your computer.
Be sure to install pip https://pip.pypa.io/en/stable/installing/

1. install MySQL, perferably 5.7. An important module to install would be the mysql.connector. (I reccomend that you surf the web for the mysql.connector: https://dev.mysql.com/downloads/installer/)

2.Create and run a server via localhost. 
3. install Pyqt5 using pip https://pypi.org/project/PyQt5/

4. If the program is a script, you can use the command prompt to do python [program name].py in its respective directory. You could also just click on the application if you have all the modules installed


HOW TO USE APPLICATION
-----------------------
Before you login, you have to register first. You must click on the register button to make your account.Unfourntaly, there is no account recovery option, so it is reccomended
that you write down the credentials somewhere safe.


NAVIGATION PAGE
--------------
Log Hours: Proceeds to log page

Edit Student: Provides the option to edit the selected student's information (Grade and Name). You cannot change a student's Id.

Remove Student: Removes student and their logs permentally.

View Report: Prints a report of your volunteer hours. It will tell you what catergory your district is in so far as listed on the page itself.

Change Password: WARNING BE CAREFUL WITH USING THIS OR ELSE YOU MAY GET LOCKED OUT OF YOUR ACCOUNT. PLEASAE WRITE DOWN ANY PASSWORD YOU CHANGE.

Log out: Logs out


HOW TO ADD STUDENT:
------
The edit lines below will provide you the ability to enter student credentials. Click on the "Add Student" button to add the student to your chapter.

*Note: Students cannot have the same existing ID or Name in your chapter.


LOG PAGE
-----
Add Hours: Simply fill the existing form on the top and press the "Add Hours" button. If there is already an existing log with the same Date and Location, it will add onto to 
the log.

Delete Hours: Select a row on the table-The numbers beside each row-and click on the "Delete Hours" button to remove the log permentally

View Info: Select a row on the table-The numbers beside each row-and click on the "Log Details" button to view more information of the log

Hours only/Hours:Mins: Changes the format of time viewed on the table. This is for perference of the user.

Exit: Exit

*All the data is automatically saved so you don't need to worry about having to update or clicking the X button on the window by accident.



APPLICATION NOTES
--------------------------
Most of the problems I had debugging the project was solved by the controller class.

cursor.execute will execute a command for Mysql. Here are all the commands http://g2pc1.bu.edu/~qzpeng/manual/MySQL%20Commands.htm

If a program crashes or doesn't respond, its best be that you restart the application.

In order to use the ui files, I installed pyuic5 and converted them into py files, then copied and pasted it into the Program file.

#there was a really weird glitch/error where the data for a student was removed but the student would still be on the comboBox, so I simply made some sort of error handler that closes the page and reopens it.

PLEASE SAVE YOUR REGISTER CREDENTIALS SOMEWHERE SAFE


Q&A
------------------------
Q: If a student leaves my chapter because he graduated how do I differiate from them?

A: For any student that leaves your chapter, you can simply change their names by going to Edit Student and adding (Deactivated) onto their names. An Example would be 
Yoshikage Kira had about 10 hours of volunteer work and he graduated. Simply change his name from Yoshikage Kira to Yoshikage Kira (Deactivated).

Q: Is there a way to change the Student ID?

A: Unfourntaly not, the Student ID is very vital to a student's identification.

Q: How do you prevent your credentials from being lost?

A: Write them down into a notebook, I did not spend money on internet secruity okay?

Q: What kind of database did you use?

A: Good question, read below.


DATABASES
-------------
All data is stored in a local mysql server on my computer. The passwords are encoded with a passcode.

How I worked with the database on this project was with using relational tables. I used two tables one for username storage and another for volunter hour storage.

When the user logs in, their user_id table "log" (Hour storage) is their respective auto incremented Id on the username storage. I use this user_id in junction with the 
student name to pull the stored volunteer hours that the students have done. 

Table setups (MYSQL):
------------
users:
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| id       | int(7)       | NO   | PRI | NULL    | auto_increment |
| username | varchar(255) | YES  |     | NULL    |                |
| password | varchar(255) | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+

log:
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| id           | int(7)       | NO   | PRI | NULL    | auto_increment |
| user_id      | int(7)       | YES  |     | NULL    |                |
| student_id   | varchar(255) | YES  |     | NULL    |                |
| student_name | varchar(255) | YES  |     | NULL    |                |
| Grade        | varchar(255) | YES  |     | NULL    |                |
| Date         | varchar(255) | YES  |     | NULL    |                |
| Location     | varchar(255) | YES  |     | NULL    |                |
| time         | decimal(6,2) | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+



FBLA
-------------------
https://www.fbla-pbl.org/competitive-event/coding-programming/


CREDITS
----------------------
PYQT5 https://pypi.org/project/PyQt5/
WING PERSONAL (latest release) https://wingware.com/downloads/wing-personal
Mysql https://www.mysql.com/
QT DESIGNER https://doc.qt.io/qt-5/qtdesigner-manual.html
Python 3.7
pyuic5 https://pypi.org/project/pyqt5-tools/
FBLA logo from https://www.juhsd.net/Page/929










