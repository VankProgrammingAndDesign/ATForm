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

        # EXTRA LEFT BOX
        #def openCloseLeftBox():
        #    UIFunctions.toggleLeftBox(self, True)
        #widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        #widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        #def openCloseRightBox():
        #    UIFunctions.toggleRightBox(self, True)
        #widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        #Fill Users
        users = getAllUsers()
        for user in users:
            widgets.user_comboBox.addItem(user)

        #Adjust preRepairVerify_table
        widgets.preRepairVerify_table.insertColumn(0)

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
            resultsTicket = Ticket(getTicketInfo(widgets.ticketSearch_entry.text()))
            widgets.preRepairVerify_table.setItem(0,0, QTableWidgetItem(resultsTicket.ticketNum)) #Ticket Number
            widgets.preRepairVerify_table.setItem(0,1, QTableWidgetItem(resultsTicket.model)) #Model
            widgets.preRepairVerify_table.setItem(0,2, QTableWidgetItem(resultsTicket.deviceSN))#Serial Number
            #Sub issue
            #Description
            #School
            resultsTicket.deviceSN
            resultsTicket.status

        def clearSearch(self):
            print("Clearing Search Screen")
            widgets.preRepairVerify_table.clearContents()
            widgets.ticketSearch_entry.clear()


        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.userSelection)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        # if btnName == "btn_widgets":
        #     widgets.stackedWidget.setCurrentWidget(widgets.widgets)
        #     UIFunctions.resetStyle(self, btnName)
        #     btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        # if btnName == "btn_new":
        #     widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
        #     UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
        #     btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "login_btn":
            tryLogin(self)

        if btnName == "ticketSearch_btn":
            searchForTicket(self)

        if btnName == "clearInfo_btn":
            clearSearch(self)

        if btnName == "verifyInfo_btn":
            widgets.stackedWidget.setCurrentWidget(widgets.pickParts)

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
    sys.exit(app.exec_())
