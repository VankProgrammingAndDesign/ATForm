# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

from json import load
import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from modules.dbHandler import *
from modules.ticket import Ticket
from widgets import *

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Autotask Assistant"
        description = "Making Autotask Easier"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        #widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)
    
        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.preRepairVerify_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        widgets.preRepairVerify_table.horizontalHeader().hide()

        header = widgets.pickeableParts_table.horizontalHeader()

        header = widgets.pickeableParts_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        
        widgets.pickeableParts_table.horizontalHeader().hide()
        widgets.pickeableParts_table.verticalHeader().hide()

        widgets.preRepairVerify_table.insertColumn(0)
        
        widgets.pickSummary_table.setColumnCount(0)
        widgets.pickSummary_table.horizontalHeader().hide()
        widgets.pickSummary_table.verticalHeader().hide()

        header = widgets.pickSummary_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        widgets.preNotesInformation_table.setColumnCount(0)
        widgets.preNotesInformation_table.horizontalHeader().hide()
        widgets.preNotesInformation_table.verticalHeader().hide()

        header = widgets.preNotesInformation_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # BUTTONS CLICK
        # Add for each clickable button
        # ///////////////////////////////////////////////////////////////
        
        # userSelection
        widgets.login_btn.clicked.connect(self.buttonClick)

        # ticketSearchAndVerify
        widgets.clearInfo_btn.clicked.connect(self.buttonClick)
        widgets.ticketSearch_btn.clicked.connect(self.buttonClick)
        widgets.verifyInfo_btn.clicked.connect(self.buttonClick)
        
        #pickParts
        widgets.pickParts_btn.clicked.connect(self.buttonClick)

        #pickSummary
        widgets.confirmPick_btn.clicked.connect(self.buttonClick)

        #notesSelection
        widgets.addInspectionLine_btn.clicked.connect(self.buttonClick)
        widgets.addRepairLine_btn.clicked.connect(self.buttonClick)
        widgets.addVerificationLine_btn.clicked.connect(self.buttonClick)
        widgets.copyNotes_btn.clicked.connect(self.buttonClick)
        widgets.confirmNotes_btn.clicked.connect(self.buttonClick)

        #ticketSummary
        widgets.finalizeTicket_btn.clicked.connect(self.buttonClick)


        #widgets..clicked.connect(self.buttonClick)

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)

        #Fill Users
        users = getAllUsers()
        for user in users:
            widgets.user_comboBox.addItem(user)

        

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.userSelection)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    
    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()


        def tryLogin(self):
            selectedUser = widgets.user_comboBox.currentText()
            pinEntry = widgets.pin_entry.text()
            actualPin = getUsersPin(selectedUser)
            print("Trying login for: " + selectedUser)
            print("Pin Entry: " + pinEntry)
            print("Actual Pin: " + actualPin)

            if(pinEntry == actualPin):
                print("Login Succesful")
                widgets.stackedWidget.setCurrentWidget(widgets.ticketSearchAndVerify)
            else:
                print("Unsuccesful Login")
            
        def searchForTicket(self):
            #TODO ticket entry error handling
            #TODO no ticket found handling

            #find ticket based on user entry
            self.currentTicket = Ticket(getTicketInfo(widgets.ticketSearch_entry.text()))
            widgets.preRepairVerify_table.setItem(0,0, QTableWidgetItem(self.currentTicket.ticketNum)) #Ticket Number
            widgets.preRepairVerify_table.setItem(0,1, QTableWidgetItem(self.currentTicket.model)) #Model
            widgets.preRepairVerify_table.setItem(0,2, QTableWidgetItem(self.currentTicket.deviceSN))#Serial Number
            #Sub issue
            #Description
            #School
            self.currentTicket.status

        def clearSearch(self):
            widgets.preRepairVerify_table.clearContents()
            widgets.ticketSearch_entry.clear()
        
        def loadPickeableParts(self):
            widgets.pickeableParts_table.setColumnCount(0)  #clear all columns
            widgets.pickeableParts_table.setRowCount(0)  #clear all rows
            widgets.pickeableParts_table.insertColumn(0)    #Part Category
            widgets.pickeableParts_table.insertColumn(1)    #Checkbox
            widgets.pickeableParts_table.insertColumn(2)    #Autotask Entry
            widgets.pickeableParts_table.insertColumn(3)    #Stock
            parts = self.currentTicket.parts

            #Grabs stock info
            stock = getPartStocks(parts.values())

            #Insert part names and categories into table
            self.checkboxes =[]
            for cat in parts:
                cb = QCheckBox()
                self.checkboxes.append(cb)
                rowPosition = widgets.pickeableParts_table.rowCount()
                widgets.pickeableParts_table.insertRow(rowPosition)
                widgets.pickeableParts_table.setItem(rowPosition , 0, QTableWidgetItem(cat))    #Category
                widgets.pickeableParts_table.setCellWidget(rowPosition, 1, cb)                  #Checkbox
                widgets.pickeableParts_table.setItem(rowPosition , 2, QTableWidgetItem(parts[cat])) #Part Name
                widgets.pickeableParts_table.setItem(rowPosition , 3, QTableWidgetItem(stock[parts[cat]])) #Part Stock
            
        def getPickedParts(self):
            widgets.pickSummary_table.setColumnCount(0)  #clear all columns
            widgets.pickSummary_table.setRowCount(0)  #clear all rows
            widgets.pickSummary_table.insertColumn(0)    #Part Category
            widgets.pickSummary_table.insertColumn(1)    #Autotask Entry
            widgets.pickSummary_table.insertColumn(2)    #Stock
            
            partsToPick={}
            checkboxes = self.checkboxes
            parts = self.currentTicket.parts

            #loop through checkboxes and locate parts to pick
            for cb,cat in zip(checkboxes,parts):
                if(cb.isChecked()):
                    partsToPick[cat] = parts[cat]
            self.partsToPick = partsToPick
            stock = getPartStocks(partsToPick.values())

            #Loop through partsToPick and add to pickSummary_table
            for cat,part in zip(partsToPick,stock):
                rowPosition = widgets.pickSummary_table.rowCount()
                widgets.pickSummary_table.insertRow(rowPosition)
                widgets.pickSummary_table.setItem(rowPosition, 0, QTableWidgetItem(cat))
                widgets.pickSummary_table.setItem(rowPosition, 1, QTableWidgetItem(partsToPick[cat]))
                widgets.pickSummary_table.setItem(rowPosition, 2, QTableWidgetItem("Stock available: " + stock[part]))
                    
        def loadPreNotesInfo(self):
            widgets.preNotesInformation_table.setColumnCount(0)  #clear all columns
            widgets.preNotesInformation_table.setRowCount(0)  #clear all rows
            widgets.preNotesInformation_table.insertColumn(0)    #Part Category
            widgets.preNotesInformation_table.insertColumn(1)    #Autotask Entry
            widgets.preNotesInformation_table.insertColumn(2)    #Stockd
            
            pickedParts={}
            pickedParts=self.pickedParts
            stock = getPartStocks(pickedParts.values())

            #Loop through pickedParts and add to preNotesInformation_table
            for cat,part in zip(pickedParts,stock):
                rowPosition = widgets.preNotesInformation_table.rowCount()
                widgets.preNotesInformation_table.insertRow(rowPosition)
                widgets.preNotesInformation_table.setItem(rowPosition, 0, QTableWidgetItem(cat))
                widgets.preNotesInformation_table.setItem(rowPosition, 1, QTableWidgetItem(pickedParts[cat]))
                widgets.preNotesInformation_table.setItem(rowPosition, 2, QTableWidgetItem("Stock available: " + stock[part]))

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.userSelection)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        # if btnName == "btn_new":
        #     widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
        #     UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
        #     btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "login_btn":
            tryLogin(self)

        if btnName == "ticketSearch_btn":
            searchForTicket(self)
            #TODO handle no partList found errors
            #TODO link to return key

        if btnName == "clearInfo_btn":
            clearSearch(self) 

        if btnName == "verifyInfo_btn":
            widgets.stackedWidget.setCurrentWidget(widgets.pickParts) #Advance to pickParts
            loadPickeableParts(self)
            #TODO make button unclickeable if ticketSearch_btn has not been pressed. 
            #TODO link to return key

        if btnName == "pickParts_btn":
            getPickedParts(self)
            widgets.stackedWidget.setCurrentWidget(widgets.pickSummary) #Advance to pickSummary
            
        if btnName == "confirmPick_btn":
            self.pickedParts=self.partsToPick
            loadPreNotesInfo(self)
            widgets.stackedWidget.setCurrentWidget(widgets.notesSelection) #Advance to notesSelection

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
