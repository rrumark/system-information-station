# Arayüzü için gerekli kütüphane/modül
import sys                                                          # Programın devamlılığı için
from PyQt5.QtWidgets import *                                       # Arayüz elemanlarına erişmek için (Qwidget, QLabel ... vb.)
from PyQt5.QtGui import *                                           # Arayüz elemanlarına erişmek için (QIcon ... vb.)
from PyQt5.QtCore import *                                          # Arayüz elemanlarına erişmek için (QAction, QToolbar ... vb.)


# Grafikler için gerekli kütüphane/modül
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg    # Grafik işlemleri için gerekli
from matplotlib.figure import Figure                                # Grafik işlemleri için gerekli
import numpy as np                                                  # Grafik işlemleri için gerekli
import time                                                         # Grafik kısmında verilerin zamana göre çizdirmek için



# My Classes
from SystemInfo import System_information                           # Home sayfası için oluşturduğumuz sınıf
from SystemInfo import CPU_information                              # CPU sayfası için oluşturduğumuz sınıf
from SystemInfo import GPU_information                              # GPU sayfası için oluşturduğumuz sınıf
from SystemInfo import Memory_information                           # RAM sayfası için oluşturduğumuz sınıf
from SystemInfo import Disk_information                             # DISK sayfası için oluşturduğumuz sınıf
from SystemInfo import Network_information                          # NETWORK sayfası için oluşturduğumuz sınıf




# Elde ettiğimiz verileri görsellerştirip,
# arayüzüne entegre etmemizi sağlayan sınıf
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



# Bu sınıfın içerisinde arayüzde bulunan elemanların tasarımsal özelliklerini tanımlıyoruz.
# Bu sınıfı oluşturmamızın sebebi, arayüz elemanlarının tasarımlarını fonksiyon oluşturarak tek seferde 
# değişiklik yapılmasına olanak sağlar.
class StyleClass:

    def LeftMenuStyle(self, menu):
        menu.setStyleSheet("QToolButton{ width: 100px; padding: 1; margin: 1; color: #F5F7FA; Background-color: #002941; }"
                                        "QToolBar{Background-color: #002941; border: 0px solid black;}"
                                        "QToolButton::section{Background-color: #001635; color: #F5F7FA;}"
                                        "QToolButton::hover{Background-color: #001635; color: #F5F7FA;}")
 
    def LabelButtonStyle(self,Label):
        Label.setStyleSheet("font-size: 12pt; border-radius: 10px; color: #F5F7FA; background-color: #104e8b;")
        


    def WidgetinLabelStyle(self,Widget):
        Widget.setStyleSheet("font-size: 12pt; border-radius: 5px; color: #F5F7FA; background-color: #104e8b;")
        
    



class Main(QMainWindow):

    # Class çalıştırıldığında __init__ içerisindeki işlemler otomatik
    # olarak gerçekleşir.
    def __init__(self): 
        super(Main,self).__init__()
        
        self.setWindowTitle("System Information Station") # Pencere başlığı 
        self.setMinimumSize(1280, 720) # Pencere boyutu

        self.Key = True # 
        app.aboutToQuit.connect(self.closeEvent) # Programdan çıkış yapıldığında 


        # Oluşturduğumuz sınıfların programımızın
        # içerisinde belirlediğimiz değişkenlere atıyoruz.
        self.Style = StyleClass() 
        self.SysInfo = System_information()
        self.CPUInfo = CPU_information()
        self.GPUInfo = GPU_information()
        self.RAMInfo = Memory_information()
        self.DiskInfo = Disk_information()
        self.NetworkInfo = Network_information()
       
        

        self.Interface() # Arayüzün temel iskeletinin oluşturulduğu fonksiyon.

        
        # Pages Functions
        self.Home_Page_Func()
        self.CPU_Page_Func()
        self.GPU_Page_Func()
        self.RAM_Page_Func()
        self.DISK_Page_Func()
        self.NETWORK_Page_Func()

        
        self.show() # Pencerenin açılmasını sağlıyor

        self.Live_LoadPercentage() # 

        
    # Yardımcı Fonksiyonlar

    # Bu fonksiyon her sayfanın içerisinde bulunan arayüzü
    # elemanlarını istenilen şekilde yerleştirip arayüze entegre etmemizi sağlar
    def createLabelinWidget(self, nameText, resultText = " "):

        resultText = ": " + resultText
        nameLabel = QLabel()
        resultLabel = QLabel()
        nameLabel.setFixedWidth(200)
        

        widget = QWidget()
        widget.setFixedHeight(50)

        nameLabel.setText(nameText)
        resultLabel.setText(resultText)

        HBox = QHBoxLayout()
        HBox.addWidget(nameLabel)
        HBox.addWidget(resultLabel)

        widget.setLayout(HBox)
        
        self.Style.WidgetinLabelStyle(widget)

        return widget


        


    # Burada arayüzün temel iskelet işlemleri
    # olacak. (Left menu, tabWidget,
    # interface pages (CPU, GPU, RAM ...))
    def Interface(self):
        # Interface Pages
        self.Home_Widget = QWidget()
        self.CPU_Widget = QWidget()
        # self.CPU_Widget.setStyleSheet("Background-color: blue;")
        self.GPU_Widget = QWidget()
        # self.GPU_Widget.setStyleSheet("Background-color: red;")
        self.RAM_Widget = QWidget()
        # self.RAM_Widget.setStyleSheet("Background-color: green;")
        self.DISK_Widget = QWidget()
        self.NETWORK_Widget = QWidget()


        # QStackedWidget : Home, CPU, GPU, RAM ... sayfalarının içerisine entegre ediyoruz.
        # Daha sonra bu sayfaları QAction kullanarak soldaki menüdeki buttonlar ile değiştiriyoruz.
        self.Main_StackedWidget = QStackedWidget()

        self.Main_StackedWidget.addWidget(self.Home_Widget)     # 0 index
        self.Main_StackedWidget.addWidget(self.CPU_Widget)      # 1 index
        self.Main_StackedWidget.addWidget(self.GPU_Widget)      # 2 index
        self.Main_StackedWidget.addWidget(self.RAM_Widget)      # 3 index
        self.Main_StackedWidget.addWidget(self.DISK_Widget)     # 4 index
        self.Main_StackedWidget.addWidget(self.NETWORK_Widget)  # 5 index
        

        
        
        # Left Menu (ToolBar) : Sol menünün olduğu öğe, içerisine QActionlar eklenerek
        # interaktif şekilde çağırılmasını sağlar.
        self.LeftMenu_ToolBar = QToolBar(self)                                  # ToolBar tanımladık
        self.LeftMenu_ToolBar.setMovable(False)                                 # Sol menünün farklı bir konuma taşınmasını engeller
        self.LeftMenu_ToolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)   #
        self.LeftMenu_ToolBar.setIconSize(QSize ( 32, 32 ))                     #
        self.Style.LeftMenuStyle(self.LeftMenu_ToolBar)                         #


            

        self.addToolBar(Qt.LeftToolBarArea , self.LeftMenu_ToolBar)             # Arayüze sol menü ekliyor

        # ToolBar içerisine Action (Button) ekeleme
        self.Home_Act = QAction(QIcon("icons/home.png"), "'    Home", self)
        self.LeftMenu_ToolBar.addAction(self.Home_Act)

        self.CPU_Act = QAction(QIcon("icons/cpu.png"), "'    CPU", self)
        self.LeftMenu_ToolBar.addAction(self.CPU_Act)

        self.GPU_Act = QAction(QIcon("icons/gpu.png"), "'    GPU", self)
        self.LeftMenu_ToolBar.addAction(self.GPU_Act)

        self.RAM_Act = QAction(QIcon("icons/ram.png"), "'    RAM", self)
        self.LeftMenu_ToolBar.addAction(self.RAM_Act)

        self.DISK_Act = QAction(QIcon("icons/disk.png"), "'    DISK", self)
        self.LeftMenu_ToolBar.addAction(self.DISK_Act)

        self.NETWORK_Act = QAction(QIcon("icons/network.png"), "'    NETWORK", self)
        self.LeftMenu_ToolBar.addAction(self.NETWORK_Act)

        # Actionların boyutlandırılması
        for action in self.LeftMenu_ToolBar.actions():
            widget = self.LeftMenu_ToolBar.widgetForAction(action)
            widget.setFixedSize(175,75)

        # Actionları fonksiyon bağlama
        self.Home_Act.triggered.connect(self.Main_StackedWidget0)
        self.CPU_Act.triggered.connect(self.Main_StackedWidget1)
        self.GPU_Act.triggered.connect(self.Main_StackedWidget2)
        self.RAM_Act.triggered.connect(self.Main_StackedWidget3)
        self.DISK_Act.triggered.connect(self.Main_StackedWidget4)
        self.NETWORK_Act.triggered.connect(self.Main_StackedWidget5)


        # Arayüze ekleme yaptık
        self.setCentralWidget(self.Main_StackedWidget)

    def Main_StackedWidget0(self): # Home sayfası için
        self.Main_StackedWidget.setCurrentIndex(0)

    def Main_StackedWidget1(self): # CPU sayfası için
        self.Main_StackedWidget.setCurrentIndex(1)

    def Main_StackedWidget2(self): # GPU sayfası için
        self.Main_StackedWidget.setCurrentIndex(2)

    def Main_StackedWidget3(self): # RAM sayfası için
        self.Main_StackedWidget.setCurrentIndex(3)

    def Main_StackedWidget4(self): # DISK sayfası için
        self.Main_StackedWidget.setCurrentIndex(4)

    def Main_StackedWidget5(self): # NETWORK sayfası için
        self.Main_StackedWidget.setCurrentIndex(5)

    # Home sayfasının dizaynı 
    def Home_Page_Func(self):
        
        text = ["Bilgisayar adı",
                "İşletim sistemi",
                "İşletim sistemi türü",
                "Versiyon",
                "Ram bilgisi"]

        VBox0 = QVBoxLayout()
        VBox0.addWidget(self.createLabelinWidget(text[0], self.SysInfo.get_PCName()))
        VBox0.addWidget(self.createLabelinWidget(text[1], self.SysInfo.get_WindowsName()))
        VBox0.addWidget(self.createLabelinWidget(text[2], self.SysInfo.get_SystemType()))
        VBox0.addWidget(self.createLabelinWidget(text[3], self.SysInfo.get_WindowsVersion()))
        VBox0.addWidget(self.createLabelinWidget(text[4], self.SysInfo.get_TotalMemory()))
        VBox0.addStretch()

        self.Home_Widget.setLayout(VBox0)


        
    def Live_LoadPercentage(self):
        start_timi = time.time() # Başlangıç zamanı
        fark = 0 # Programın başladığı zaman ile çalışmaya başladığı andaki geçen süre 
        i = 1

        CPUx_values, CPUy_values = list(), list()

        RAMx_values, RAMy_values = list(), list()

        while self.Key:
            # Programın içerisinde herhangi bir değerin
            # değiştiğinde programın arayüzünün yenilemesini sağlar
            QApplication.processEvents() 

            now = time.time()

            fark = now - start_timi

            if fark >= i:
                
                #### CPU
                QApplication.processEvents()
                textCPULoadPercentage = self.CPUInfo.get_LoadPercentage() # CPU Yük Miktarını veren fonk.
                self.CPU_LoadPercentage_resultLabel.setText(": " + textCPULoadPercentage + " %")

                CPUx_values.append(i)
                CPUy_values.append(float(textCPULoadPercentage))
                ###

                ### Memory
                QApplication.processEvents()
                textRAM_LoadPercentage = self.RAMInfo.get_Percentage() # RAM Yük Miktarını veren fonk.
                self.RAM_LoadPercentage_resultLabel.setText(": " + textRAM_LoadPercentage + " %")

                RAMx_values.append(i)
                RAMy_values.append(float(textRAM_LoadPercentage))
                ###



                
                if len(CPUx_values) >= 60:

                    # CPU
                    CPUx_values.pop(0)
                    CPUy_values.pop(0)

                    # Memory
                    RAMx_values.pop(0)
                    RAMy_values.pop(0)





                i += 1

            ## CPU Grafik işlemleri başlangıç
            self.CPU_LoadGraph = MplCanvas(self, width=100, height=4, dpi=100)
            self.CPU_LoadGraph.axes.fill_between(CPUx_values, CPUy_values)
            self.CPU_LoadGraph.axes.plot(CPUx_values, CPUy_values, color="#000099", linestyle="dashed", linewidth=1, markersize=1)
            self.CPU_LoadGraph.axes.set_title("Kullanım Yüzdesi")
            self.CPU_LoadGraph.axes.get_xaxis().set_visible(False)
            self.CPU_LoadGraph.axes.set_ylim(0, 100)

            self.CPU_LoadGraph.axes.set_yticks(np.arange(0, 101, 5))
            self.CPU_LoadGraph.axes.grid(which='major', alpha=1)

            self.CPU_GraphWidget1.setCentralWidget(self.CPU_LoadGraph)
            ## CPU Grafik işlemleri son



            ## RAM Grafik işlemleri başlangıç
            self.RAM_LoadGraph = MplCanvas(self, width=100, height=4, dpi=100)
            self.RAM_LoadGraph.axes.fill_between(RAMx_values, RAMy_values)
            self.RAM_LoadGraph.axes.plot(RAMx_values, RAMy_values, color="#000099", linestyle="dashed", linewidth=1, markersize=1)
            self.RAM_LoadGraph.axes.set_title("Kullanım Yüzdesi")
            self.RAM_LoadGraph.axes.get_xaxis().set_visible(False)
            self.RAM_LoadGraph.axes.set_ylim(0, 100)

            self.RAM_LoadGraph.axes.set_yticks(np.arange(0, 101, 5))
            self.RAM_LoadGraph.axes.grid(which='major', alpha=1)

            self.RAM_GraphWidget1.setCentralWidget(self.RAM_LoadGraph)
            ## RAM Grafik işlemleri son





    def closeEvent(self, event):
        self.Key = False
        print("Program sonlandı")
        self.close()
        event.accept()


    def CPU_Page_Func(self):
        QApplication.processEvents()

        text = ["İşlemci",
                "Çekirdek Sayısı",
                "Kullanım Yüzdesi",
                "Temel Hız",
                "Mantıksal İşlemci Sayısı",
                "Hız"]

        self.CPU_GraphWidget1 = QMainWindow() # Grafiğin konumladırılacağı MainWindow
        
       
        
        nameLabel = QLabel()
        nameLabel.setFixedWidth(200)

        self.CPU_LoadPercentage_resultLabel = QLabel() # ResultLabel
        
        


        #### Cpu Load Percentage
        widget = QWidget()
        widget.setFixedHeight(50)

        nameLabel.setText(text[2])

        HBox = QHBoxLayout()
        HBox.addWidget(nameLabel)
        HBox.addWidget(self.CPU_LoadPercentage_resultLabel)

        widget.setLayout(HBox)
        
        self.Style.WidgetinLabelStyle(widget)
        #### 
        



        VBox0 = QVBoxLayout()
        VBox0.addWidget(self.createLabelinWidget(text[0], self.CPUInfo.get_CPUName()))
        VBox0.addWidget(self.createLabelinWidget(text[1], self.CPUInfo.get_NumberOfCores()))
        VBox0.addWidget(widget)

        VBox1 = QVBoxLayout()
        VBox1.addWidget(self.createLabelinWidget(text[3], self.CPUInfo.get_CPUMaxSpeed()))
        VBox1.addWidget(self.createLabelinWidget(text[4], self.CPUInfo.get_NumberOfLogicalCores()))
        VBox1.addWidget(self.createLabelinWidget(text[5], self.CPUInfo.get_CPUSpeed()))


        HBox0 = QHBoxLayout()
        HBox0.addLayout(VBox0)
        HBox0.addLayout(VBox1)

        VBox2 = QVBoxLayout()
        VBox2.addLayout(HBox0)
        VBox2.addWidget(self.CPU_GraphWidget1)



        self.CPU_Widget.setLayout(VBox2)
       


    def GPU_Page_Func(self):
        

        self.GPU_ComboBox = QComboBox()
        self.GPU_ComboBox.addItems(self.GPUInfo.get_GPUNameList())

        self.GPU_MainWindow = QMainWindow()
        
        HBox0 = QHBoxLayout()
        HBox0.addWidget(self.GPU_ComboBox)
        HBox0.addStretch()

        VBox0 = QVBoxLayout()
        VBox0.addLayout(HBox0)
        VBox0.addWidget(self.GPU_MainWindow)

        


        self.GPU_Widget.setLayout(VBox0)

        self.GPU_Replacement()
        self.GPU_ComboBox.activated.connect(self.GPU_Replacement)



    def GPU_Replacement(self):

        text = ["Marka/Model",
                "Bellek Miktarı",
                "Ekran Yenileme Hızı",
                "Grafik Mimarisi"]

        name = self.GPU_ComboBox.currentText()  # anahtar kelime (key)
        values = self.GPUInfo.get_Values()      # Sözlük (dict)
        valueList = values[name]

        tempWidget = QWidget()

        VBox0 = QVBoxLayout()
        VBox0.addWidget(self.createLabelinWidget(text[0], valueList[0]))
        VBox0.addWidget(self.createLabelinWidget(text[1], valueList[1]))
        VBox0.addWidget(self.createLabelinWidget(text[2], valueList[2]))
        VBox0.addWidget(self.createLabelinWidget(text[3], valueList[3]))
        VBox0.addStretch()

        tempWidget.setLayout(VBox0)


        self.GPU_MainWindow.setCentralWidget(tempWidget)



    def RAM_Page_Func(self):

        QApplication.processEvents()

        text = ["Marka/Model",
                "Toplam",
                "Kullanılan Bellek",
                "Kullanılabilir Bellek",
                "Parça Numarası",
                "Hız",
                "Maksimum Hız",
                "Kullanım Yüzdesi"]

        self.RAM_GraphWidget1 = QMainWindow()

        
        nameLabel = QLabel()
        self.RAM_LoadPercentage_resultLabel = QLabel()
        nameLabel.setFixedWidth(200)



        #### Ram Load Percentage
        widget = QWidget()
        widget.setFixedHeight(50)

        nameLabel.setText(text[7])

        HBox = QHBoxLayout()
        HBox.addWidget(nameLabel)
        HBox.addWidget(self.RAM_LoadPercentage_resultLabel)

        widget.setLayout(HBox)
        
        self.Style.WidgetinLabelStyle(widget)
        #### 
        



        VBox0 = QVBoxLayout()
        VBox0.addWidget(self.createLabelinWidget(text[0], self.RAMInfo.get_Model()))        # Marka/Model
        VBox0.addWidget(self.createLabelinWidget(text[1], self.RAMInfo.get_Total()))        # Toplam
        VBox0.addWidget(self.createLabelinWidget(text[2], self.RAMInfo.get_Used()))         # Kullanılan Bellek
        VBox0.addWidget(self.createLabelinWidget(text[3], self.RAMInfo.get_Available()))    # Kullanılabilir Bellek

        VBox1 = QVBoxLayout()
        VBox1.addWidget(self.createLabelinWidget(text[4], self.RAMInfo.get_PartNumer()))    # Parça Numarası
        VBox1.addWidget(self.createLabelinWidget(text[5], self.RAMInfo.get_Speed()))        # Hız
        VBox1.addWidget(self.createLabelinWidget(text[6], self.RAMInfo.get_MaxSpeed()))     # Maksimum Hız
        VBox1.addWidget(widget) # Kullanım yüzdesinin yazıldığı yer                         # Kullanım Yüzdesi

        HBox0 = QHBoxLayout()
        HBox0.addLayout(VBox0)
        HBox0.addLayout(VBox1)

        VBox2 = QVBoxLayout()
        VBox2.addLayout(HBox0)
        VBox2.addWidget(self.RAM_GraphWidget1)



        self.RAM_Widget.setLayout(VBox2)



            










    def DISK_Page_Func(self):


        self.Disk_ComboBox = QComboBox()
        self.Disk_ComboBox.addItems(self.DiskInfo.get_DeviceIDList())

        self.Disk_MainWindow = QMainWindow()

        HBox0 = QHBoxLayout()
        HBox0.addWidget(self.Disk_ComboBox)
        HBox0.addStretch()

        VBox0 = QVBoxLayout()
        VBox0.addLayout(HBox0)
        VBox0.addWidget(self.Disk_MainWindow)


        self.DISK_Widget.setLayout(VBox0)

        self.DISK_Replacement()
        self.Disk_ComboBox.activated.connect(self.DISK_Replacement)


    def DISK_Replacement(self):
        
        text = ["Disk",
                "Toplam Alan",
                "Kullanılan Alan",
                "Tür",
                "Dosya Sistemi",
                "Kullanılabilir Alan"]

        name = self.Disk_ComboBox.currentText()
        values = self.DiskInfo.get_Values()

        self.Disk_ComboBox.clear()
        self.Disk_ComboBox.addItems(self.DiskInfo.get_DeviceIDList())

        try:
            valueList = values[name]

            self.Disk_GraphWidget = QMainWindow()

            self.Disk_Graph = MplCanvas(self, width=100, height=4, dpi=100)
            self.Disk_Graph.axes.barh(y = [text[5], text[2]], height = 0.5,
                                    width = [valueList[6], valueList[7]],
                                    color = ["#1E90FF", "#FF1493"])

            self.Disk_Graph.axes.set_xlim(0, 100),

            self.Disk_GraphWidget.setCentralWidget(self.Disk_Graph)

 

            tempWidget = QWidget()
            
            VBox0 = QVBoxLayout()
            VBox0.addWidget(self.createLabelinWidget(text[0], valueList[0]))
            VBox0.addWidget(self.createLabelinWidget(text[1], valueList[1]))
            VBox0.addWidget(self.createLabelinWidget(text[2], valueList[2]))
            # VBox0.addStretch()

            VBox1 = QVBoxLayout()
            VBox1.addWidget(self.createLabelinWidget(text[3], valueList[3]))
            VBox1.addWidget(self.createLabelinWidget(text[4], valueList[4]))
            VBox1.addWidget(self.createLabelinWidget(text[5], valueList[5]))
            # VBox1.addStretch()

            HBox0 = QHBoxLayout()
            HBox0.addLayout(VBox0)
            HBox0.addLayout(VBox1)

            VBox2 = QVBoxLayout()
            VBox2.addLayout(HBox0)
            VBox2.addWidget(self.Disk_GraphWidget)


            tempWidget.setLayout(VBox2)

            self.Disk_MainWindow.setCentralWidget(tempWidget)


        except:

            print(" \"{}\" böyle bir disk bulunamamaktadır.\n".format(name[0]+":"))
   

    def NETWORK_Page_Func(self):

        

        self.Network_Mainwindow = QMainWindow()
        self.Network_RefleshButton = QPushButton()
        self.Network_RefleshButton.setText("Reflesh")

        HBox0 = QHBoxLayout()
        HBox0.addStretch()
        HBox0.addWidget(self.Network_RefleshButton)

        VBox0 = QVBoxLayout()
        VBox0.addWidget(self.Network_Mainwindow)
        VBox0.addLayout(HBox0)
        VBox0.addStretch()

        self.NETWORK_Widget.setLayout(VBox0)
        
        self.NETWORK_Replacement()
        self.Network_RefleshButton.clicked.connect(self.NETWORK_Replacement)


    def NETWORK_Replacement(self):
  

        text = ["Name",
                "Description",
                "Physical Address",
                "State",
                "SSID",
                "BSSID",
                "Radio Type",
                "Signal",
                "Profile",
                "Reflesh"]


        valueList = self.NetworkInfo.get_Values()

        tempWidget = QWidget()

        VBox0 = QVBoxLayout()
        VBox0.addWidget(self.createLabelinWidget(text[0], valueList["Name"]))
        VBox0.addWidget(self.createLabelinWidget(text[1], valueList["Description"]))
        VBox0.addWidget(self.createLabelinWidget(text[2], valueList["Physical address"]))
        VBox0.addWidget(self.createLabelinWidget(text[3], valueList["State"]))
        VBox0.addWidget(self.createLabelinWidget(text[4], valueList["SSID"]))
        VBox0.addWidget(self.createLabelinWidget(text[5], valueList["BSSID"]))
        VBox0.addWidget(self.createLabelinWidget(text[6], valueList["Radio type"]))
        VBox0.addWidget(self.createLabelinWidget(text[7], valueList["Signal"]))
        VBox0.addWidget(self.createLabelinWidget(text[8], valueList["Profile"]))
        VBox0.addStretch()

    
        tempWidget.setLayout(VBox0)


        self.Network_Mainwindow.setCentralWidget(tempWidget)


























if __name__ == '__main__':
    app = QApplication(sys.argv)
    MAIN = Main()
    sys.exit(app.exec_())