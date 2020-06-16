# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:34:19 2020

@author: wiesbrock
"""
from PyQt5.QtGui import QPalette, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QLineEdit, QLabel, 
                             QTextEdit, QMessageBox, QGridLayout,QFileDialog, QComboBox
                             ,QTabWidget)
import datetime
import sys
import uuid
import psycopg2
import shutil
import numpy as np
import glob
import csv
import pandas

unique_id=str(uuid.uuid4())
conn=psycopg2.connect(host="XXXXXXXXXXx",database="xxxxxxxxxxxx", user="xxxxxxxxxx", password="xxxxxxxxx")
cur = conn.cursor()
sql = "SELECT projectname FROM projects"
projects=cur.execute(sql)
result = cur.fetchall()

final_result = [list(i) for i in result]
final_result=np.unique(final_result)

subprojects=[]

class Example(QWidget):
    


    def __init__(self):
        super(Example,self).__init__()

        self.initUI()
        
    def choose_path_dst(self):
        direct=QFileDialog.getExistingDirectory(self, 'Open file', "C://")
        self.dst_line.setText('{}'.format(direct))
    
    def choose_path_src(self):
        direct=QFileDialog.getExistingDirectory(self, 'Open file', "C://")
        self.source_line.setText('{}'.format(direct))
        
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:

            event.ignore()
          
    def submit_data(self):
        experimenter=self.expEdit.text()
        date_time=self.date.text()
        project=self.comboBox.currentText()
        species=self.spec_line.text()
        comment=self.commentEdit.toPlainText()
        src=self.source_line.text()
        dst=self.dst_line.text()
        unique_id=self.id_line.text()
        
        file_list=glob.glob(src)
        
        for i in range(len(file_list)):
            shutil.move(file_list[i],dst)
'''            
        with open('log', 'rb') as myfile:
            informations=[]
            wr = csv.writer(myfile)
            informations=[date_time,project,species,unique_id,src,dst,experimenter,comment]
            print(informations)
            wr.writerow(informations)
'''        

        print("Succesful backup")
        
        conn=psycopg2.connect(host="xxxxxx",database="xxxxxxx", user="xxxx", password="xxxxxx")
        print("Login succesful")
        cur = conn.cursor()
        cur.execute("INSERT INTO datasets(dataset_id,source,destination,experimenter,project,mouse_id,date) VALUES(%s,%s,%s,%s,%s,%s,%s)",([unique_id,src,dst,experimenter,project,species,date_time]))
        print("Data is collected")
        conn.commit()
        cur.close()
        conn.close()
        print("Entry succesful")
        
    def update_subprojects(self):
        
       
        
        conn=psycopg2.connect(host="XXXXXXXXX",database="XXXXXXXX", user="XXXXXXXX", password="XXXXXXXXXX")
        cur=conn.cursor()
        text_box=self.comboBox.currentText()
        text_box="'"+text_box+"'"
        cur.execute('SELECT subproject FROM projects WHERE projectname={};'.format(text_box))
        subprojects=cur.fetchall()
        final_subprojects = [list(i) for i in subprojects]
        self.comboBox2.clear()
        
        for i in range(len(final_subprojects)):
            
            self.comboBox2.addItem(final_subprojects[i][0])
            
        self.comboBox2.update()
        
        
        

    def initUI(self):
       
        
        
        self.comboBox = QComboBox(self)
        for i in range(len(final_result)):
            self.comboBox.addItem(final_result[i])
          
        self.comboBox2=QComboBox(self)
        
        conn=psycopg2.connect(host="XXXXX",database="XXXXXX", user="XXXXXXXXX", password="XXXXXXXX")
        cur=conn.cursor()
        text_box=self.comboBox.currentText()
        text_box="'"+text_box+"'"
        cur.execute('SELECT subproject FROM projects WHERE projectname={};'.format(text_box))
        subprojects=cur.fetchall()
        final_subprojects = [list(i) for i in subprojects]
        
        for i in range(len(final_subprojects)):
            self.comboBox2.addItem(final_subprojects[i][0])
         
            
        self.okButton = QPushButton("Submit")
        self.cancelButton = QPushButton("Quit")
        self.updateButton=QPushButton("Update Projects")
        self.newprojectButton = QPushButton("New Project...")
        self.folder_source_Button = QPushButton("File...")
        self.folder_dst_Button = QPushButton("File...")
        self.id_line=QLabel(unique_id)
        self.id_label=QLabel("ID")
        self.subproject_label=QLabel("Subproject")
        self.source_line=QLineEdit(self)
        self.source=QLabel('Source')
        self.dst_line=QLineEdit(self)
        self.dst=QLabel('Destination')
        self.spec_line=QLineEdit(self)
        self.spec=QLabel('Species')
        self.commentEdit = QTextEdit(self)
        self.comment=QLabel('Comment')
        self.expEdit = QLineEdit(self)
        self.exp=QLabel('Experimenter')
        #self.projectEdit = QLineEdit(self)
        self.project=QLabel('Project')
        self.date=QLabel(str(datetime.datetime.now())[:-7])
        self.date_label=QLabel('Date and Time')
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(self.exp,0,0)
        grid.addWidget(self.expEdit,0,1)
       
        grid.addWidget(self.project,1,0)
        grid.addWidget(self.comboBox,1,1)
        grid.addWidget(self.newprojectButton,1,2)
        grid.addWidget(self.subproject_label,2,0)
        grid.addWidget(self.comboBox2,2,1)
        grid.addWidget(self.updateButton,2,2)
        self.updateButton.clicked.connect(self.update_subprojects)
        
        
        
        
        grid.addWidget(self.date_label,3,0)
        grid.addWidget(self.date,3,1)
        
        grid.addWidget(self.source,4,0)
        grid.addWidget(self.source_line,4,1)
        grid.addWidget(self.folder_source_Button,4,2)
        self.folder_source_Button.clicked.connect(self.choose_path_src)
        
        grid.addWidget(self.dst,5,0)
        grid.addWidget(self.dst_line,5,1)
        grid.addWidget(self.folder_dst_Button,5,2)
        self.folder_dst_Button.clicked.connect(self.choose_path_dst)
        
        grid.addWidget(self.spec,6,0)
        grid.addWidget(self.spec_line, 6,1)
        
        grid.addWidget(self.comment,7,0)
        grid.addWidget(self.commentEdit,7,1)
        
        grid.addWidget(self.id_label,8,0)
        grid.addWidget(self.id_line,8,1)

        grid.addWidget(self.okButton,9,0)
        self.okButton.clicked.connect(self.submit_data)
        grid.addWidget(self.cancelButton,9,1)
        self.cancelButton.clicked.connect(self.close)
        
        
        self.setLayout(grid)

        self.setGeometry(800, 300, 500, 300)
        self.setWindowTitle('Data Transfer Tool')
        self.setWindowIcon(QIcon('Desktop\RTG_Logo600x6002'))

        self.show()




def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    