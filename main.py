from db import createDB
import sys
from PyQt5 import QtWidgets
from PyQt5.QtSql import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from datetime import date
today = str(date.today())

class AdminLogin(QDialog):
    def __init__(self):
        super(AdminLogin,self).__init__()
        loadUi("adminlogin.ui",self)
        self.createDB()
        self.LoginButton.clicked.connect(self.loginfunction)
        self.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.InvalidShowlabel.setVisible(False)

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

    def loginfunction(self):
        useid=self.UserIdLineEdit.text()
        passwor=self.PasswordLineEdit.text()
        print("Successfully logged in with email: ", useid, "and password:", passwor)
        self.query.exec_("select * from admin where userid='%s' and password='%s'"%(useid,passwor))
        self.query.first()
        if self.query.value("userid") != None and self.query.value("password") != None:
            print("login successful")
            homepage=HomePage()
            widget.addWidget(homepage)
            widget.setCurrentIndex(widget.currentIndex()+1)

        elif useid=="superadmin" and passwor=="superadmin":
            admincontrol=AdminControl()
            widget.addWidget(admincontrol)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.InvalidShowlabel.setVisible(True)

class AdminControl(QDialog):
    def __init__(self):
        super(AdminControl,self).__init__()
        loadUi("admincontrol.ui",self)
        self.createDB()
        self.ConfirmLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.CPassLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UserIdLabel.setVisible(False)
        self.PasswordLabel.setVisible(False)
        self.CUserIdLabel.setVisible(False)
        self.ConfirmPassLabel.setVisible(False)
        self.UseridLineEdit.setVisible(False)
        self.ConfirmLineEdit.setVisible(False)
        self.CPassLineEdit.setVisible(False)
        self.DeleteButton.setVisible(False)
        self.AddButton.setVisible(False)
        self.InvalidLabel.setVisible(False)
        self.InvalidLabel2.setVisible(False)
        self.SuccessLabel.setVisible(False)
        self.SuccessLabel2.setVisible(False)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.AddAdminButton.clicked.connect(self.AddAdminFunc)
        self.DeleteAdminButton.clicked.connect(self.DeleteAdminFunc)
        self.DeleteButton.clicked.connect(self.Delete)
        self.AddButton.clicked.connect(self.Add)

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()
    
    def AddAdminFunc(self):
        print("AddAdmin Clicked")
        self.UserIdLabel.setVisible(True)
        self.PasswordLabel.setVisible(True)
        self.ConfirmPassLabel.setVisible(True)
        self.UseridLineEdit.setVisible(True)
        self.ConfirmLineEdit.setVisible(True)
        self.CPassLineEdit.setVisible(True)
        self.AddButton.setVisible(True)
        self.CUserIdLabel.setVisible(False)
        self.DeleteButton.setVisible(False)
        self.InvalidLabel.setVisible(False)
        self.InvalidLabel2.setVisible(False)
        self.SuccessLabel.setVisible(False)
        self.SuccessLabel2.setVisible(False)
        self.UseridLineEdit.clear()
        self.ConfirmLineEdit.clear()
        self.CPassLineEdit.clear()

    def DeleteAdminFunc(self):
        print("DeleteAdmin Clicked")
        self.UserIdLabel.setVisible(True)
        self.PasswordLabel.setVisible(False)
        self.CUserIdLabel.setVisible(True)
        self.ConfirmPassLabel.setVisible(False)
        self.UseridLineEdit.setVisible(True)
        self.ConfirmLineEdit.setVisible(True)
        self.CPassLineEdit.setVisible(False)
        self.DeleteButton.setVisible(True)
        self.AddButton.setVisible(False)
        self.InvalidLabel.setVisible(False)
        self.InvalidLabel2.setVisible(False)
        self.SuccessLabel.setVisible(False)
        self.SuccessLabel2.setVisible(False)
        self.UseridLineEdit.clear()
        self.ConfirmLineEdit.clear()
        self.CPassLineEdit.clear()

    def Delete(self):
        if self.UseridLineEdit.text()!='' and self.ConfirmLineEdit.text()!='':
            if self.UseridLineEdit.text()==self.ConfirmLineEdit.text():
                duserid=self.UseridLineEdit.text()
                self.query.exec_("select id from admin where userid='%s'"%(duserid))
                self.query.first()
                if self.query.value("id")!=None:
                    self.query.exec_("delete from admin where userid='%s'"%(duserid))
                    self.SuccessLabel.setVisible(True)
                    self.InvalidLabel.setVisible(False)
                    print("delete commited")
                else:
                    self.InvalidLabel.setVisible(True)
                    self.SuccessLabel.setVisible(False)
            else:
                self.InvalidLabel.setVisible(True)
                self.SuccessLabel.setVisible(False)
        else:
            self.InvalidLabel.setVisible(True)
            self.SuccessLabel.setVisible(False)

    def Add(self):
        if self.UseridLineEdit.text()!='' and self.ConfirmLineEdit.text()!='' and self.CPassLineEdit!='':
            if self.CPassLineEdit.text()==self.ConfirmLineEdit.text():
                auserid=self.UseridLineEdit.text()
                apass=self.CPassLineEdit.text()
                self.query.exec_("select id from admin where userid='%s' and password='%s'"%(auserid,apass))
                self.query.first()
                if self.query.value("id")==None:
                    self.query.exec_("insert into admin (userid,password) values ('%s','%s')"%(auserid,apass))
                    self.SuccessLabel2.setVisible(True)
                    self.InvalidLabel2.setVisible(False)
                    print("addition commited")
                else:
                    self.InvalidLabel2.setVisible(True)
                    self.SuccessLabel2.setVisible(False)
            else:
                self.InvalidLabel2.setVisible(True)
                self.SuccessLabel2.setVisible(False)
        else:
            self.InvalidLabel2.setVisible(True)
            self.SuccessLabel2.setVisible(False)


class HomePage(QDialog):
    def __init__(self):
        super(HomePage,self).__init__()
        loadUi("home.ui",self)
        self.RegisterButton.clicked.connect(self.RegWinFunc)
        self.LogoutButton.clicked.connect(LogOutFunc)
        self.TransactionButton.clicked.connect(self.TransactionWin)
        self.MatchButton.clicked.connect(self.MatchWin)
        self.MatchBidButton.clicked.connect(self.MatchBidWin)
        self.SbNameButton.clicked.connect(self.SearchBNWin)
        self.SbIdButton.clicked.connect(self.SearchBIdWin)
        self.SbPhoneButton.clicked.connect(self.SearchBPNWin)
        self.SbStateButton.clicked.connect(self.SearchBSWin)
        self.AvailabilityButton.clicked.connect(self.AvailabiltyWin)
        self.TranHisBIdButton.clicked.connect(self.TransHisIdWin)
        self.TranHisBDateButton.clicked.connect(self.TransHisDateWin)
        self.UpdateUserButton.clicked.connect(self.UpdateUserWin)

    def RegWinFunc(self):
        print("Successfully logged in Reg Page ")
        regwindow=RegWindow()
        widget.addWidget(regwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def TransactionWin(self):
        print("Successfully logged in Transaction Page ")
        twindow=TransactionPage()
        widget.addWidget(twindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def AvailabiltyWin(self):
        print("Successfully logged in Availability Page ")
        availwindow=AvailabilityPage()
        widget.addWidget(availwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def MatchWin(self):
        print("Successfully logged in Match Page ")
        matchwindow=MatchPage()
        widget.addWidget(matchwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def MatchBidWin(self):
        print("Successfully logged in Match By id Page ")
        matchbidwindow=MatchBidPage()
        widget.addWidget(matchbidwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def SearchBIdWin(self):
        print("Successfully logged in Search By id Page ")
        sbidwindow=SearchBIdPage()
        widget.addWidget(sbidwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def SearchBNWin(self):
        print("Successfully logged in Search By name Page ")
        sbnwindow=SearchBNPage()
        widget.addWidget(sbnwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def SearchBPNWin(self):
        print("Successfully logged in Search By Phone Number Page ")
        sbpnwindow=SearchBPNPage()
        widget.addWidget(sbpnwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def SearchBSWin(self):
        print("Successfully logged in Search By State Page ")
        sbswindow=SearchBSPage()
        widget.addWidget(sbswindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def TransHisIdWin(self):
        print("Successfully logged in Transaction History by Id Page ")
        thidwindow=TransHisBIdPage()
        widget.addWidget(thidwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def TransHisDateWin(self):
        print("Successfully logged in Transaction History of a date Page ")
        thdwindow=TransHisBDatePage()
        widget.addWidget(thdwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def UpdateUserWin(self):
        print("Update User Window")
        upuswindow=UpdateUserPage()
        widget.addWidget(upuswindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
class RegWindow(QDialog):
    def __init__(self):
        super(RegWindow,self).__init__()
        loadUi("register.ui",self)
        self.SuccesReglabel.setVisible(False)
        self.MandatoryRegLabel.setVisible(False)
        self.AlreadyRegLabel.setVisible(False)
        self.LogoutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.SubmitRegButton.clicked.connect(self.SubmitRgFunc)
        self.createDB()


    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

    def SubmitRgFunc(self):
        rfname=self.FNameLineEdit.text()
        rfname=rfname.capitalize()
        rlname=self.LNameLineEdit.text()
        rlname=rlname.capitalize()
        rsex=self.SexComboBox.currentText()
        rphoneno=self.PhoneNumLineEdit.text()
        rbloodgr=self.BloodGpComboBox.currentText()
        rrhfac=self.RHFactorComboBox.currentText()
        rdob=self.DOBEdit.date()
        rdobf=('{0}-{1}-{2}'.format(rdob.year(), rdob.month(), rdob.day()))
        rstate=self.StateComboBox.currentText()
        rcity=self.CityLineEdit.text()
        rcity=rcity.capitalize()
        raddress=self.AddressLineEdit.text()

        print("Clicked Submit Registration")

        if rfname!="" and rlname!="" and rsex!=None and rphoneno!="" and rbloodgr!=None and rrhfac!=None and rdobf!=None and rstate!=None and rcity!="" and raddress!="":
            print("ALL FILLED")
            self.query.exec_("select * from users where fname='%s' and lname='%s' and phoneNo='%s'"%(rfname,rlname,rphoneno))
            self.query.first()
            if self.query.value("fname") != None:
                print("user exists")
                self.AlreadyRegLabel.setVisible(True)
                self.MandatoryRegLabel.setVisible(False)
                self.SuccesReglabel.setVisible(False)

            else:
                print("data entered")
                self.query.exec_("insert into users (fname, lname, sex, phoneNo, bloodGr, rhFac, dob, state, city, address) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(rfname,rlname,rsex,rphoneno,rbloodgr,rrhfac,rdobf,rstate,rcity,raddress))
                self.SuccesReglabel.setVisible(True)
                self.MandatoryRegLabel.setVisible(False)
                self.AlreadyRegLabel.setVisible(False)
            
        else:
           self.MandatoryRegLabel.setVisible(True)
           self.SuccesReglabel.setVisible(False)
           self.AlreadyRegLabel.setVisible(False)


class TransactionPage(QDialog):
    def __init__(self):
        super(TransactionPage,self).__init__()
        loadUi("Transaction.ui",self)
        self.createDB()
        self.SubmitTranButton.clicked.connect(self.TransFunc)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.InvalidLabel.setVisible(False)
        self.TrSucLabel.setVisible(False)
        self.DonorNELabel.setVisible(False)

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

    def TransFunc(self):
        print("Clicked Submit in Transaction Page ")
        didcheck=self.IdDlineEdit.text()
        ridcheck=self.IdRlineEdit.text()
        if didcheck!='' and didcheck.isnumeric()==True and self.UnitspinBox.value()!=0:
            tid=int(self.IdDlineEdit.text())
            tunit=self.UnitspinBox.value()
            ttype=self.TranTypecomboBox.currentText()
            self.query.exec_("select bloodGr,rhFac from users where id='%i'"%(tid))
            self.query.first()
            bgp=self.query.value("bloodGr")
            rhd=self.query.value("rhFac")
            self.query.exec_("select tDate from transactions where Donor_id='%i' and transType='Direct Donate' or Donor_id='%i' and transType='Donate to Blood Bank'"%(tid,tid))
            self.query.last()
            tldate=self.query.value("tDate")
            print(tldate)
            gapdays=None
            if tldate!=None:
                if int(today[:4])>int(tldate[:4]):
                    if today[5:7]=="01" and tldate[5:7]=="12":
                        gapdays=int(today[8:])-int(tldate[8:])
                    else:
                        gapdays=100
                elif int(today[:4])==int(tldate[:4]):
                    if int(today[5:7])-int(tldate[5:7])==1:
                        gapdays=int(today[8:])-int(tldate[8:])
                    elif int(today[5:7])==int(tldate[5:7]):
                        gapdays=-1
                    elif int(today[5:7])-int(tldate[5:7])<0:
                        print("error")
                    else:
                        gapdays=100
                else:
                    print("error")
            else:
                gapdays=100
            print(gapdays)

            if bgp!=None and ridcheck=='' and ttype=="Donate to Blood Bank":
                if gapdays>=0:
                    self.query.exec_("insert into transactions (tDate,units,transType,Donor_id) values ('%s','%i','%s','%i')"%(today,tunit,ttype,tid))
                    self.InvalidLabel.setVisible(False)
                    self.TrSucLabel.setVisible(True)
                    self.IdDlineEdit.clear()
                    self.IdRlineEdit.clear()
                    self.DonorNELabel.setVisible(False)
                    print(bgp)
                    self.query.exec_("select totalUnits from inventory where bloodGroup='%s' and rhFactor='%s'"%(bgp,rhd))
                    self.query.first()
                    Tunits=self.query.value("totalUnits")
                    print(Tunits)
                    Tunits+=tunit
                    self.query.exec_("update inventory set totalUnits= '%i' where bloodGroup='%s' and rhFactor='%s'"%(Tunits,bgp,rhd))
                elif gapdays<0:
                    self.InvalidLabel.setVisible(False)
                    self.TrSucLabel.setVisible(False)
                    self.DonorNELabel.setVisible(True)
                else:
                    self.InvalidLabel.setVisible(True)
                    self.TrSucLabel.setVisible(False)
                    self.DonorNELabel.setVisible(False)


            elif bgp!=None and ridcheck!='' and ridcheck.isnumeric()==True and ttype=="Receive from Blood Bank":
                trid=int(self.IdRlineEdit.text())
                self.query.exec_("select totalUnits from inventory where bloodGroup='%s' and rhFactor='%s'"%(bgp,rhd))
                self.query.first()
                Tunits=self.query.value("totalUnits")
                self.query.exec_("select bloodGr from users where id='%i'"%(trid))
                self.query.first()
                bgprcheck=self.query.value("bloodGr")
                if Tunits>=tunit and bgprcheck!=None:
                    self.query.exec_("insert into transactions (tDate,units,transType,Donor_id,Recipient_id) values ('%s','%i','%s','%i','%i')"%(today,tunit,ttype,tid,trid))
                    Tunits-=tunit
                    self.query.exec_("update inventory set totalUnits= '%i' where bloodGroup='%s' and rhFactor='%s'"%(Tunits,bgp,rhd))
                    self.InvalidLabel.setVisible(False)
                    self.TrSucLabel.setVisible(True)
                    self.IdDlineEdit.clear()
                    self.IdRlineEdit.clear()
                    self.DonorNELabel.setVisible(False)
                else:
                    self.InvalidLabel.setVisible(True)
                    self.TrSucLabel.setVisible(False)
                    self.DonorNELabel.setVisible(False)
            elif bgp!=None and ridcheck!='' and ridcheck.isnumeric()==True and ttype=="Direct Donate":
                trid=int(self.IdRlineEdit.text())
                self.query.exec_("select bloodGr from users where id='%i'"%(trid))
                self.query.first()
                bgprcheck=self.query.value("bloodGr")
                if bgprcheck!=None:
                    if gapdays>=0:
                        self.query.exec_("insert into transactions (tDate,units,transType,Donor_id,Recipient_id) values ('%s','%i','%s','%i','%i')"%(today,tunit,ttype,tid,trid))
                        self.InvalidLabel.setVisible(False)
                        self.TrSucLabel.setVisible(True)
                        self.IdDlineEdit.clear()
                        self.IdRlineEdit.clear()
                        self.DonorNELabel.setVisible(False)
                    elif gapdays<0:
                        self.InvalidLabel.setVisible(False)
                        self.TrSucLabel.setVisible(False)
                        self.DonorNELabel.setVisible(True)
                else:
                    self.InvalidLabel.setVisible(True)
                    self.TrSucLabel.setVisible(False)
                    self.DonorNELabel.setVisible(False)
            else:
                self.InvalidLabel.setVisible(True)
                self.TrSucLabel.setVisible(False)
                self.DonorNELabel.setVisible(False)
        else:
            self.InvalidLabel.setVisible(True)
            self.TrSucLabel.setVisible(False)
            self.DonorNELabel.setVisible(False)

class MatchPage(QDialog):
    def __init__(self):
        super(MatchPage,self).__init__()
        loadUi("match.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.SearchMFunc)

    def SearchMFunc(self):
        print("Clicked Search Match")
        bg=self.BloodGpComboBox.currentText()
        rh=self.RHFactorComboBox.currentText()
        st=self.StateComboBox.currentText()
        print(bg)
        print(rh)
        print(st)
        if st=="----":
            if bg=="A+":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
            elif bg=="A-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
            elif bg=="B+":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
            elif bg=="B-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
            elif bg=="AB+":
                self.query.exec_("select * from users where rhFac='%s'"%(rh))
            elif bg=="AB-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
            elif bg=="O+":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
            elif bg=="O-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s'"%(bg,rh))
            self.query.first()
            if self.query.value("id")!=None:
                counter=0
                while self.query.value("id")!=None:
                    self.query.next()
                    counter+=1
                rowcount=0
                self.tableWidget.setRowCount(counter)
                if bg=="A+":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                elif bg=="A-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                elif bg=="B+":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                elif bg=="B-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                elif bg=="AB+":
                    self.query.exec_("select * from users where rhFac='%s'"%(rh))
                elif bg=="AB-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                elif bg=="O+":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                elif bg=="O-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s'"%(bg,rh))
                self.query.first()
                while self.query.value("id")!=None:
                    self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                    self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                    self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                    self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                    self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                    self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                    self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                    self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                    self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                    self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                    self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                    self.query.next()
                    rowcount+=1
                print(counter)
                self.tableWidget.setVisible(True)
                self.DataNFLabel.setVisible(False)
            else:
                self.DataNFLabel.setVisible(True)
                self.tableWidget.setVisible(False)
        else:
            if bg=="A+":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
            elif bg=="A-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
            elif bg=="B+":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
            elif bg=="B-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
            elif bg=="AB+":
                self.query.exec_("select * from users where rhFac='%s' and state='%s'"%(rh,st))
            elif bg=="AB-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
            elif bg=="O+":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
            elif bg=="O-":
                self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s'"%(bg,rh,st))
            self.query.first()
            if self.query.value("id")!=None:
                counter=0
                while self.query.value("id")!=None:
                    self.query.next()
                    counter+=1
                rowcount=0
                self.tableWidget.setRowCount(counter)
                if bg=="A+":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                elif bg=="A-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                elif bg=="B+":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                elif bg=="B-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                elif bg=="AB+":
                    self.query.exec_("select * from users where rhFac='%s' and state='%s'"%(rh,st))
                elif bg=="AB-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                elif bg=="O+":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                elif bg=="O-":
                    self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s'"%(bg,rh,st))
                self.query.first()
                while self.query.value("id")!=None:
                    self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                    self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                    self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                    self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                    self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                    self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                    self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                    self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                    self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                    self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                    self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                    self.query.next()
                    rowcount+=1
                print(counter)
                self.tableWidget.setVisible(True)
                self.DataNFLabel.setVisible(False)
            else:
                self.DataNFLabel.setVisible(True)
                self.tableWidget.setVisible(False)



    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

class MatchBidPage(QDialog):
    def __init__(self):
        super(MatchBidPage,self).__init__()
        loadUi("matchBid.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.SearchMidFunc)

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

    def SearchMidFunc(self):
        print("clicked submit in match by id")
        mid=self.IdLineEdit.text()
        st=self.StateComboBox.currentText()
        print(mid)
        print(st)
        if mid!='' and mid.isnumeric()==True:
            mid=int(mid)
            self.query.exec_("select bloodGr,rhFac from users where id='%i'"%(mid))
            self.query.first()
            if self.query.value("bloodGr")!=None:
                bg=self.query.value("bloodGr")
                rh=self.query.value("rhFac")
                print(bg)
                print(rh)
                if st=="----":
                    if bg=="A+":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                    elif bg=="A-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                    elif bg=="B+":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                    elif bg=="B-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                    elif bg=="AB+":
                        self.query.exec_("select * from users where rhFac='%s'"%(rh))
                    elif bg=="AB-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                    elif bg=="O+":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                    elif bg=="O-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s'"%(bg,rh))
                    self.query.first()
                    if self.query.value("id")!=None:
                        counter=0
                        while self.query.value("id")!=None:
                            self.query.next()
                            counter+=1
                        rowcount=0
                        self.tableWidget.setRowCount(counter)
                        if bg=="A+":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                        elif bg=="A-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                        elif bg=="B+":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O+' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                        elif bg=="B-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                        elif bg=="AB+":
                            self.query.exec_("select * from users where rhFac='%s'"%(rh))
                        elif bg=="AB-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='A-' and rhFac='%s' or bloodGr='B-' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh,rh,rh))
                        elif bg=="O+":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' or bloodGr='O-' and rhFac='%s'"%(bg,rh,rh))
                        elif bg=="O-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s'"%(bg,rh))
                        self.query.first()
                        while self.query.value("id")!=None:
                            self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                            self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                            self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                            self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                            self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                            self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                            self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                            self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                            self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                            self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                            self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                            self.query.next()
                            rowcount+=1
                        print(counter)
                        self.tableWidget.setVisible(True)
                        self.DataNFLabel.setVisible(False)
                    else:
                        self.DataNFLabel.setVisible(True)
                        self.tableWidget.setVisible(False)
                else:
                    if bg=="A+":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                    elif bg=="A-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                    elif bg=="B+":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                    elif bg=="B-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                    elif bg=="AB+":
                        self.query.exec_("select * from users where rhFac='%s' and state='%s'"%(rh,st))
                    elif bg=="AB-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                    elif bg=="O+":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                    elif bg=="O-":
                        self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s'"%(bg,rh,st))
                    self.query.first()
                    if self.query.value("id")!=None:
                        counter=0
                        while self.query.value("id")!=None:
                            self.query.next()
                            counter+=1
                        rowcount=0
                        self.tableWidget.setRowCount(counter)
                        if bg=="A+":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                        elif bg=="A-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                        elif bg=="B+":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O+' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                        elif bg=="B-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                        elif bg=="AB+":
                            self.query.exec_("select * from users where rhFac='%s' and state='%s'"%(rh,st))
                        elif bg=="AB-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='A-' and rhFac='%s' and state='%s' or bloodGr='B-' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st,rh,st,rh,st))
                        elif bg=="O+":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s' or bloodGr='O-' and rhFac='%s' and state='%s'"%(bg,rh,st,rh,st))
                        elif bg=="O-":
                            self.query.exec_("select * from users where bloodGr='%s' and rhFac='%s' and state='%s'"%(bg,rh,st))
                        self.query.first()
                        while self.query.value("id")!=None:
                            self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                            self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                            self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                            self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                            self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                            self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                            self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                            self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                            self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                            self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                            self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                            self.query.next()
                            rowcount+=1
                        print(counter)
                        self.tableWidget.setVisible(True)
                        self.DataNFLabel.setVisible(False)
                    else:
                        self.DataNFLabel.setVisible(True)
                        self.tableWidget.setVisible(False)
            else:
                self.DataNFLabel.setVisible(True)
                self.tableWidget.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)

class AvailabilityPage(QDialog):
    def __init__(self):
        super(AvailabilityPage,self).__init__()
        loadUi("availability.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.createDB()
        self.SearchAFunc()

    def SearchAFunc(self):
        print("Clicked Search Availability")
        self.query.exec_("select * from inventory")
        self.query.first()
        counter=0
        while self.query.value("bloodGr_id")!=None:
            self.query.next()
            counter+=1
        rowcount=0
        self.tableWidget.setRowCount(counter)
        self.query.exec_("select * from inventory")
        self.query.first()
        while self.query.value("bloodGr_id")!=None:
            self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr_id"))))
            self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGroup"))))
            self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("rhFactor"))))
            self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("totalUnits"))))
            self.query.next()
            rowcount+=1
        print(counter)

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()


class TransHisBIdPage(QDialog):
    def __init__(self):
        super(TransHisBIdPage,self).__init__()
        loadUi("transHistoryId.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.TransHisBIdFunc)

    def TransHisBIdFunc(self):
        print("Clicked Transaction History by id")
        thbid=self.IdlineEdit.text()
        print(thbid)
        if thbid.isnumeric()==True and thbid!='':
            thbid=int(thbid)
            self.query.exec_("select * from transactions where Donor_id='%i' and transType='Donate to Blood Bank' or Donor_id='%i' and transType='Direct Donate' or Recipient_id='%i' and transType='Receive from Blood Bank'"%(thbid,thbid,thbid))
            self.query.first()
            if self.query.value("transaction_id")!=None:
                counter=0
                while self.query.value("transaction_id")!=None:
                    self.query.next()
                    counter+=1
                rowcount=0
                self.tableWidget.setRowCount(counter)
                self.query.exec_("select * from transactions where Donor_id='%i' and transType='Donate to Blood Bank' or Donor_id='%i' and transType='Direct Donate' or Recipient_id='%i' and transType='Receive from Blood Bank'"%(thbid,thbid,thbid))
                self.query.first()
                while self.query.value("transaction_id")!=None:
                    self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("transaction_id"))))
                    self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("Donor_id"))))
                    self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("Recipient_id"))))
                    self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("units"))))
                    self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("transType"))))
                    self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("tDate"))))
                    self.query.next()
                    rowcount+=1
                print(counter)
                self.tableWidget.setVisible(True)
                self.DataNFLabel.setVisible(False)
            else:
                self.DataNFLabel.setVisible(True)
                self.tableWidget.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)
        
        

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()


class TransHisBDatePage(QDialog):
    def __init__(self):
        super(TransHisBDatePage,self).__init__()
        loadUi("TransHistoryDate.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.TransHisBDateFunc)

    def TransHisBDateFunc(self):
        print("Clicked Transaction History by Date")
        thbdate=self.dateEdit.date()
        if thbdate.month()<10 and thbdate.day()<10:
            thbdatef=('{0}-0{1}-0{2}'.format(thbdate.year(), thbdate.month(), thbdate.day()))
        elif thbdate.month()>=10 and thbdate.day()<10:
            thbdatef=('{0}-{1}-0{2}'.format(thbdate.year(), thbdate.month(), thbdate.day()))
        elif thbdate.month()<10 and thbdate.day()>=10:
            thbdatef=('{0}-0{1}-{2}'.format(thbdate.year(), thbdate.month(), thbdate.day()))
        else:
            thbdatef=('{0}-{1}-{2}'.format(thbdate.year(), thbdate.month(), thbdate.day()))
        print(thbdatef)
        self.query.exec_("select * from transactions where tDate='%s'"%(thbdatef))
        self.query.first()
        if self.query.value("transaction_id")!=None:
            counter=0
            while self.query.value("transaction_id")!=None:
                self.query.next()
                counter+=1
            rowcount=0
            self.tableWidget.setRowCount(counter)
            self.query.exec_("select * from transactions where tDate='%s'"%(thbdatef))
            self.query.first()
            while self.query.value("transaction_id")!=None:
                self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("transaction_id"))))
                self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("Donor_id"))))
                self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("Recipient_id"))))
                self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("units"))))
                self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("transType"))))
                self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("tDate"))))
                self.query.next()
                rowcount+=1
            print(counter)
            self.tableWidget.setVisible(True)
            self.DataNFLabel.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)
        
    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()


class SearchBIdPage(QDialog):
    def __init__(self):
        super(SearchBIdPage,self).__init__()
        loadUi("SearchBId.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.SearchBidFunc)

    def SearchBidFunc(self):
        print("Clicked Search by id")
        sbid=self.IdLineEdit.text()
        print(sbid)
        if sbid.isnumeric()==True:
            sbid=int(sbid)
            self.query.exec_("select * from users where id='%i'"%(sbid))
            self.query.first()
            if self.query.value("id")!=None:
                counter=0
                while self.query.value("id")!=None:
                    self.query.next()
                    counter+=1
                rowcount=0
                self.tableWidget.setRowCount(counter)
                self.query.exec_("select * from users where id='%i'"%(sbid))
                self.query.first()
                while self.query.value("id")!=None:
                    self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                    self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                    self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                    self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                    self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                    self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                    self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                    self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                    self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                    self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                    self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                    self.query.next()
                    rowcount+=1
                print(counter)
                self.tableWidget.setVisible(True)
                self.DataNFLabel.setVisible(False)
            else:
                self.DataNFLabel.setVisible(True)
                self.tableWidget.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)
        
    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()


class SearchBNPage(QDialog):
    def __init__(self):
        super(SearchBNPage,self).__init__()
        loadUi("SearchBN.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.SearchBnFunc)

    def SearchBnFunc(self):
        print("Clicked Search by name")
        sfn=self.FNameLineEdit.text()
        sfn=sfn.capitalize()
        sln=self.LNameLineEdit.text()
        sln=sln.capitalize()
        print(sfn)
        print(sln)
        self.query.exec_("select * from users where fname='%s' and lname='%s'"%(sfn,sln))
        self.query.first()
        if self.query.value("id")!=None:
            counter=0
            while self.query.value("id")!=None:
                self.query.next()
                counter+=1
            rowcount=0
            self.tableWidget.setRowCount(counter)
            self.query.exec_("select * from users where fname='%s' and lname='%s'"%(sfn,sln))
            self.query.first()
            while self.query.value("id")!=None:
                self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                self.query.next()
                rowcount+=1
            print(counter)
            self.tableWidget.setVisible(True)
            self.DataNFLabel.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)
        
    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()


class SearchBPNPage(QDialog):
    def __init__(self):
        super(SearchBPNPage,self).__init__()
        loadUi("SearchBPN.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.SearchBpnFunc)

    def SearchBpnFunc(self):
        print("Clicked Search by phone number")
        spn=self.PhoneNumLineEdit.text()
        print(spn)
        self.query.exec_("select * from users where phoneNo='%s'"%(spn))
        self.query.first()
        if self.query.value("id")!=None:
            counter=0
            while self.query.value("id")!=None:
                self.query.next()
                counter+=1
            rowcount=0
            self.tableWidget.setRowCount(counter)
            self.query.exec_("select * from users where phoneNo='%s'"%(spn))
            self.query.first()
            while self.query.value("id")!=None:
                self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                self.query.next()
                rowcount+=1
            print(counter)
            self.tableWidget.setVisible(True)
            self.DataNFLabel.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)
        
    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()


class SearchBSPage(QDialog):
    def __init__(self):
        super(SearchBSPage,self).__init__()
        loadUi("SearchBS.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.DataNFLabel.setVisible(False)
        self.tableWidget.setVisible(False)
        self.createDB()
        self.SearchButton.clicked.connect(self.SearchBsFunc)

    def SearchBsFunc(self):
        print("Clicked Search by state")
        sstate=self.StateComboBox.currentText()
        print(sstate)
        self.query.exec_("select * from users where state='%s'"%(sstate))
        self.query.first()
        if self.query.value("id")!=None:
            counter=0
            while self.query.value("id")!=None:
                self.query.next()
                counter+=1
            rowcount=0
            self.tableWidget.setRowCount(counter)
            self.query.exec_("select * from users where state='%s'"%(sstate))
            self.query.first()
            while self.query.value("id")!=None:
                self.tableWidget.setItem(rowcount,0,QtWidgets.QTableWidgetItem(str(self.query.value("id"))))
                self.tableWidget.setItem(rowcount,1,QtWidgets.QTableWidgetItem(str(self.query.value("fname"))))
                self.tableWidget.setItem(rowcount,2,QtWidgets.QTableWidgetItem(str(self.query.value("lname"))))
                self.tableWidget.setItem(rowcount,3,QtWidgets.QTableWidgetItem(str(self.query.value("sex"))))
                self.tableWidget.setItem(rowcount,4,QtWidgets.QTableWidgetItem(str(self.query.value("phoneNo"))))
                self.tableWidget.setItem(rowcount,5,QtWidgets.QTableWidgetItem(str(self.query.value("bloodGr"))))
                self.tableWidget.setItem(rowcount,6,QtWidgets.QTableWidgetItem(str(self.query.value("rhFac"))))
                self.tableWidget.setItem(rowcount,7,QtWidgets.QTableWidgetItem(str(self.query.value("dob"))))
                self.tableWidget.setItem(rowcount,8,QtWidgets.QTableWidgetItem(str(self.query.value("state"))))
                self.tableWidget.setItem(rowcount,9,QtWidgets.QTableWidgetItem(str(self.query.value("city"))))
                self.tableWidget.setItem(rowcount,10,QtWidgets.QTableWidgetItem(str(self.query.value("address"))))
                self.query.next()
                rowcount+=1
            print(counter)
            self.tableWidget.setVisible(True)
            self.DataNFLabel.setVisible(False)
        else:
            self.DataNFLabel.setVisible(True)
            self.tableWidget.setVisible(False)
        
    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

class UpdateUserPage(QDialog):
    def __init__(self):
        super(UpdateUserPage,self).__init__()
        loadUi("updateuser.ui",self)
        self.LogOutButton.clicked.connect(LogOutFunc)
        self.HomeButton.clicked.connect(HomeWinfunc)
        self.InvalidLabel.setVisible(False)
        self.SuccessLabel.setVisible(False)
        self.createDB()
        self.UpdateButton.clicked.connect(self.UpdateuserFunc)

    def createDB(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('bloodbank.db')

        if not self.db.open():
            print("Error connecting db")
        self.query = QSqlQuery()

    def UpdateuserFunc(self):
        print("Update user clicked")
        uuid=self.IdLineEdit.text()
        if uuid!='' and uuid.isnumeric()==True:
            uuid=int(uuid)
            self.query.exec_("select * from users where id='%i'"%(uuid))
            self.query.first()
            if self.query.value("id")!=None:
                pnu=self.PhoneNumLineEdit.text()
                su=self.StateComboBox.currentText()
                cu=self.CityLineEdit.text()
                cu=cu.capitalize()
                au=self.AddressLineEdit.text()
                if pnu!='':
                    self.query.exec_("update users set phoneNo= '%s' where id='%i'"%(pnu,uuid))
                    self.InvalidLabel.setVisible(False)
                    self.SuccessLabel.setVisible(True)
                if su!='----':
                    self.query.exec_("update users set state= '%s' where id='%i'"%(su,uuid))
                    self.InvalidLabel.setVisible(False)
                    self.SuccessLabel.setVisible(True)
                if cu!='':
                    self.query.exec_("update users set city= '%s' where id='%i'"%(cu,uuid))
                    self.InvalidLabel.setVisible(False)
                    self.SuccessLabel.setVisible(True)
                if au!='':
                    self.query.exec_("update users set address= '%s' where id='%i'"%(au,uuid))
                    self.InvalidLabel.setVisible(False)
                    self.SuccessLabel.setVisible(True)
            else:
                self.InvalidLabel.setVisible(True)
                self.SuccessLabel.setVisible(False)
        else:
            self.InvalidLabel.setVisible(True)
            self.SuccessLabel.setVisible(False)

def LogOutFunc():
    print("clicked logout")
    adminlogin=AdminLogin()
    widget.addWidget(adminlogin)
    widget.setCurrentIndex(widget.currentIndex()+1)

def HomeWinfunc():
    print("clicked home")
    home=HomePage()
    widget.addWidget(home)
    widget.setCurrentIndex(widget.currentIndex()+1)


if __name__ == '__main__':
    app=QApplication(sys.argv)
    mainwindow=AdminLogin()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(1150)
    widget.setFixedHeight(850)
    widget.show()
    app.exec_()