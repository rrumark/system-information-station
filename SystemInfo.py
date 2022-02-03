import wmi
import subprocess
from win32com.client import GetObject
import platform # Pc name için
from PyQt5.QtWidgets import *
import psutil


class System_information():

    def __init__(self) -> None:
        self.comp = wmi.WMI()


    def get_WindowsName(self): # Windows Sürümü (Exp : Microsoft Windows 10 Pro)
            return "  " + [o.Caption for o in GetObject('winmgmts:').ExecQuery("Select * from Win32_OperatingSystem")][0]

    
    def get_TotalMemory(self): # Toplam Bellek Miktarı
        for os in self.comp.Win32_ComputerSystem():
            return "  {} GB".format(float(os.TotalPhysicalMemory)*10**(-9))


    def get_AvailableMemory(self): # Kulanılabilir Bellek Miktarı
        for os in self.comp.Win32_OperatingSystem():
            return "  {} GB".format(float(os.FreePhysicalMemory)*10**(-6))
        

    def get_PCName(self): # Bilgisayarın adını verir
        return "  " + platform.node()


    def get_WindowsVersion(self): # Windows Version Numarasını verir (Exp : )
        for os in self.comp.Win32_OperatingSystem():
            return "  {}".format(os.Version)

        
    def get_SystemType(self): # 64 byte, 32 byte işletim sistemi
        for os in self.comp.Win32_ComputerSystem():
            return "  {}".format(os.SystemType)





        

class CPU_information():
    

    def __init__(self) -> None:
        self.comp = wmi.WMI() 
        self.psutil_ = psutil

    def get_LoadPercentage(self): # CPU Yük Miktarı

        return str(self.psutil_.cpu_percent())

    def get_CPUName(self):
        for os in self.comp.Win32_Processor():
            return "  {}".format(os.Name)

    def get_NumberOfCores(self):
        
        return "  {}".format(self.psutil_.cpu_count(logical=False))

    def get_NumberOfLogicalCores(self):
        
        return "  {}".format(self.psutil_.cpu_count(logical=True))

    def get_CPUSpeed(self):
       
        return " {} MHz".format(self.psutil_.cpu_freq().current)

    def get_CPUMaxSpeed(self):
       
        return " {} MHz".format(self.psutil_.cpu_freq().max)
   
    def get_None(self):

        return " None "







class GPU_information():
    def __init__(self) -> None:
        self.comp = wmi.WMI()
    
        self.DeviceIDList = list()


    def get_GPUNameList(self): # Ekran kartlarının isimlerinin listesini döndürür
        CaptionList = list()

        for i in range(len(self.comp.Win32_VideoController())):
            CaptionList.append(self.comp.Win32_VideoController()[i].Caption)

        return CaptionList

    def get_Values(self): # Ekran kartlarının isme göre özellikleinin sözlük( dict() ) olarak döndürür

        valueDict = dict()

        for i in range(len(self.comp.Win32_VideoController())):

            Name = self.comp.Win32_VideoController()[i].Caption
            Memory = int(self.comp.Win32_VideoController()[i].AdapterRAM)/(10**9)
            RefreshRate = self.comp.Win32_VideoController()[i].CurrentRefreshRate
            Architecture  = self.comp.Win32_VideoController()[i].VideoArchitecture 
       


            valueDict[Name] = [" " + str(Name),
                               "{:.2f} GB".format(abs(Memory)),
                               " " + str(RefreshRate) + " Hz",
                               " DDR" + str(Architecture)]
             
        return valueDict
    


class Memory_information():
    def __init__(self) -> None:
        self.comp = wmi.WMI()
        self.psutil_ = psutil.virtual_memory()


    def get_Model(self): # Üretici
        for mem in self.comp.Win32_PhysicalMemory():
            return "  {}".format(mem.Manufacturer)


    def get_Total(self): # Ram miktarı

        return " {} GB".format(self.psutil_.total/(10**9))


    def get_Used(self): # Kullanılan ram miktarı

        return " {} GB".format(self.psutil_.used/(10**9))


    def get_Available(self): # Kullanılabilir ram miktarı
        return " {} GB".format(self.psutil_.available/(10**9))

        
    def get_PartNumer(self): # Parça numarası
        for mem in self.comp.Win32_PhysicalMemory():
            return "  {}".format(mem.PartNumber )


    def get_Speed(self): # Çalışma hızı
        for mem in self.comp.Win32_PhysicalMemory():
            return "  {} MHz".format(mem.ConfiguredClockSpeed  )

    def get_MaxSpeed(self): # Maksimum çalışma hızı
        for mem in self.comp.Win32_PhysicalMemory():
            return "  {} MHz".format(mem.Speed  )


    def get_Percentage(self): # Kullanım yüzdesi

        return str(psutil.virtual_memory().percent)

class Disk_information():
    def __init__(self) -> None:
        self.comp = wmi.WMI()
        self.psutil_ = psutil.disk_usage("/")


    def get_DeviceIDList(self): # C: driver, D: driver .... bunlarn listesini döndürür
        DeviceIDList = list()
        for i in range(len(self.comp.Win32_LogicalDisk())):
            DeviceIDList.append(self.comp.Win32_LogicalDisk()[i].DeviceID)

        return DeviceIDList


    def get_Values(self): # disk isimleri (C:, D:, E: ...) isme göre özellikleinin sözlük( dict() ) olarak döndürür

        valueDict = dict()

        for i in range(len(self.comp.Win32_LogicalDisk())):

            Name = self.comp.Win32_LogicalDisk()[i].Name
            FileSystem = self.comp.Win32_LogicalDisk()[i].FileSystem
            Total = int(self.comp.Win32_LogicalDisk()[i].Size)/(10**9)
            Type = self.comp.Win32_LogicalDisk()[i].Description 
            Free = int(self.comp.Win32_LogicalDisk()[i].FreeSpace)/(10**9)
            Used = Total - Free
            
            FreePercent = (100*Free)/Total
            UsedPercent = 100 - FreePercent

            valueDict[Name] = [str(Name)[0] + " Drive",
                              " {:.2f} GB".format(Total),
                              " {:.2f} GB".format(Used),
                              " " + str(Type),
                              " " + str(FileSystem),
                              " {:.2f} GB".format(Free),
                              FreePercent,
                              UsedPercent]
             
        return valueDict




class Network_information():
    def __init__(self) -> None:
        pass

        

    def get_Values(self):

        resultDict = dict()
        try:

        
            result = subprocess.run(["netsh","wlan", "show", "interface"], capture_output=True, text=True).stdout
            list1 = result.split("\n")
            lastList  = list()
            for i in range(24):
                list3 = list1[i].split("  ")
                text = ""
                for j in list3:
                    if j not in "  ":
                        text += j
                if text != "":
                    lastList.append(text.split(":"))
            
            lastList = lastList[1:]
            for i in range(len(lastList)):
                if lastList[i][0][-1] == " ":
                    lastList[i][0] = lastList[i][0][:-1]

            

            for i in lastList:
                resultDict[i[0]] = i[1:]
                
            for i in resultDict:
                text = resultDict[i][0]
                
                if len(resultDict[i]) > 1:
                    for j in range(1, len(resultDict[i])):
                        text += ":" + resultDict[i][j] 
                        
                    resultDict[i] = text
                    
                else:
                    
                    resultDict[i] = resultDict[i][0]

        except:
            keyList = ["Name", "Description", "GUID", "Physical address",
                       "State", "SSID", "BSSID", "Network type", "Radio type",
                       "Authentication","Cipher","Connection mode", "Channel",
                       "Receive rate (Mbps)", "Transmit rate (Mbps)", "Signal", "Profile"] 

            for i in keyList:
                resultDict[i] = "No connection"

        return resultDict

