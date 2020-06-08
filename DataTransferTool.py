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
                             QTextEdit, QMessageBox, QGridLayout,QFileDialog, QComboBox)
import datetime
import sys
import uuid
import psycopg2
import shutil


unique_id=str(uuid.uuid4())
conn=psycopg2.connect(host="XXXXXXXX",database="XXXXXX", user="XXXXXXX", password="XXXXXXXX")
cur = conn.cursor()
sql = "SELECT projectname FROM projects"
projects=cur.execute(sql)
result = cur.fetchall()

final_result = [list(i) for i in result]

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
            
    def success(self, event):

        success = QMessageBox.question(self, 'Message',
                                     "The entry was successful. Do you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if success == QMessageBox.Yes:

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
        
        print(experimenter)
        print(date_time)
        print(project)
        print(species)
        print(comment)
        
        shutil.move(src,dst)
        f= open(dst+"\\log.csv","w+")
        f.write("Unique ID,Source,Destination,")
        f.close()
        f= open(dst+"\\log.csv","a+")
        f.write((str(date_time)+","+str(project)+","+str(species)+","+str(unique_id)+","+str(src)+","+str(dst)+","+str(experimenter)+","+str(comment)))
        f.close()

        print("Succesful backup")
        
        conn=psycopg2.connect(host="db.bio2.rwth-aachen.de",database="playground", user="wiesbrock", password="6O8$pMt8")
        print("Login succesful")
        cur = conn.cursor()
        cur.execute("INSERT INTO datasets(dataset_id,source,destination,experimenter,project,mouse_id,date) VALUES(%s,%s,%s,%s,%s,%s,%s)",([unique_id,src,dst,experimenter,project,species,date_time]))
        print("Data is collected")
        conn.commit()
        cur.close()
        conn.close()
        print("Entry succesful")
        self.success
        

    def initUI(self):
        self.comboBox = QComboBox(self)
        for i in range(len(final_result)):
            self.comboBox.addItem(final_result[i][0])
            
        okButton = QPushButton("Submit")
        cancelButton = QPushButton("Quit")
        newprojectButton = QPushButton("New Project...")
        folder_source_Button = QPushButton("File...")
        folder_dst_Button = QPushButton("File...")
        self.id_line=QLabel(unique_id)
        id_label=QLabel("ID")
        self.source_line=QLineEdit(self)
        source=QLabel('Source')
        self.dst_line=QLineEdit(self)
        dst=QLabel('Destination')
        self.spec_line=QLineEdit(self)
        spec=QLabel('Species')
        self.commentEdit = QTextEdit(self)
        comment=QLabel('Comment')
        self.expEdit = QLineEdit(self)
        exp=QLabel('Experimenter')
        self.projectEdit = QLineEdit(self)
        project=QLabel('Project')
        self.date=QLabel(str(datetime.datetime.now())[:-7])
        date_label=QLabel('Date and Time')
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(exp,0,0)
        grid.addWidget(self.expEdit,0,1)
        
        grid.addWidget(project,1,0)
        grid.addWidget(self.comboBox,1,1)
        grid.addWidget(newprojectButton,1,2)
        
        
        
        grid.addWidget(date_label,2,0)
        grid.addWidget(self.date,2,1)
        
        grid.addWidget(source,3,0)
        grid.addWidget(self.source_line,3,1)
        grid.addWidget(folder_source_Button,3,2)
        folder_source_Button.clicked.connect(self.choose_path_src)
        
        grid.addWidget(dst,4,0)
        grid.addWidget(self.dst_line,4,1)
        grid.addWidget(folder_dst_Button,4,2)
        folder_dst_Button.clicked.connect(self.choose_path_dst)
    
        grid.addWidget(spec,5,0)
        grid.addWidget(self.spec_line, 5,1)
        
        grid.addWidget(comment,6,0)
        grid.addWidget(self.commentEdit,6,1)
        
        grid.addWidget(id_label,7,0)
        grid.addWidget(self.id_line,7,1)
        
        grid.addWidget(okButton,8,0)
        okButton.clicked.connect(self.submit_data)
        grid.addWidget(cancelButton,8,1)
        cancelButton.clicked.connect(self.close)
        

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
    