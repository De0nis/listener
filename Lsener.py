"""
Need to install PyQt5 
this program will show you all open porst and program, who opend them
""" 
import sys,subprocess
from PyQt5.QtWidgets import  QApplication,QLabel,QRadioButton,QGridLayout,QWidget,QVBoxLayout,QScrollArea,QHBoxLayout
import socket
#visualisation module
resulttablemas = []
class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def getnames():
        resulttablemas = maintable.resulttablecreate()
        return resulttablemas
    def initUI(self):
        self.clbl = QLabel(self)
        self.clbl.move(40,0)
        self.clbl.setText('Type   local    Outer     Status    PID    Progam   Session  №   Memory')
        self.grid = QGridLayout()
        self.addComponents()
        layoutH = QHBoxLayout()  
        layoutV = QVBoxLayout()        
        scroll = QScrollArea()  
        self.widget = QWidget() 
        layoutH.addWidget(scroll)
        self.widget.setLayout(self.grid)
        scroll.setWidget(self.widget)
        scroll.setWidgetResizable(True) 
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)         
    def addComponents(self):
        resulttablemas = Interface.getnames()
        for i in range(len(resulttablemas)):
            s=str(resulttablemas[i])
            button = QRadioButton(s)
            self.grid.addWidget(button)
            button.toggled.connect(lambda: self.btnstate())
        self.move(300, 250)
        self.setWindowTitle('All opend ports')
        self.show()
    def btnstate(self):
        button = self.sender().text()
        z = (button.split())
        zm = z[1].replace(",", '')
        zo = zm.replace("'", '')
        zt = zo.split(':')
        if ((zt[0]=='0.0.0.0') or (zt[0]=='[')):
            zt[0]='127.0.0.1'
        print(zt[0])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addrr='127.0.0.1', int(zt[1])
        s.bind(addrr)
        conn, addr = s.accept()
        print ('connected:', addr)
        conn.close()
#Data structuring module
class maintable(Interface):
    def __init__(self):
        super().__init__()
        self.initUI()
    def getdata(command):
        df = subprocess.Popen(command , shell = True, stdout = subprocess.PIPE)
        data, error = df.communicate()  
        datarec = data.decode(encoding='cp866') 
        if (error) is not None:
            print('alert',error.decode(encoding='cp866') )
        return datarec
    def splitlist(listing):
        activelist = []	
        for i in range(len(listing)):
            activelist.append(listing[i].split())
        return activelist
    def activeconnectionlistget():
        activeconnections = maintable.getdata("netstat -a -n -o")
        clr = activeconnections.index('PID')
        activeconnections2 = ((activeconnections)[clr+3:]).lstrip().splitlines()
        connections=maintable.splitlist(activeconnections2)
        for i in range (len(connections)):   
            if (len(connections[i]))<5:
                connections[i].insert(3, 'not have') 
        return connections 
    def tasklistget():
        taskslist = maintable.getdata("tasklist")
        clr2 = taskslist.rindex('=')
        tasks2 = (taskslist[clr2+1:]).lstrip().splitlines()
        activetasks = maintable.splitlist(tasks2)
        return activetasks
    def txtfile(dir, data):
        texter=open(dir, 'w') 
        texter.write(data)
    def resulttablecreate():
        conn = maintable.activeconnectionlistget()
        tas = maintable.tasklistget()
        resulttable = []
        for i in range(len(conn)):
            for j in range(len(tas)):
                if ((conn[i][4]) == (tas[j][1])): 
                    resulttable.append(conn[i]+tas[j])
        for k in range(len(resulttable)):
             resulttable[k].pop(6)
             resulttable[k].insert(8,(resulttable[k][8])+(resulttable[k].pop(9))+(resulttable[k].pop(-1)))
             resulttable[k].pop(-1)
        return resulttable
    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
