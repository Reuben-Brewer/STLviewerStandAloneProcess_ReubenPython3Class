# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com,
www.reubotics.com

Apache 2 License
Software Revision B, 12/22/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
try:
    from GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class import *
    GetCPUandMemoryUsageOfProcessByPID_ModuleImportedFlag = 1

except:
    GetCPUandMemoryUsageOfProcessByPID_ModuleImportedFlag = 0
    print("Error: the module 'GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class' cvould not be imported.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
from UDPdataExchanger_ReubenPython3Class import *
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
import os
import sys
import time
import datetime
import multiprocessing
import collections
from copy import *  # for deepcopy(dict)
import inspect  # To enable 'TellWhichFileWereIn'
import traceback
import math
from decimal import Decimal
import threading
import platform
import psutil
import pexpect
import subprocess
import signal  #for CTRLc_HandlerFunction
import queue as Queue
from queue import Empty #For draining the queue

from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk

##########################################################################################################
from importlib.metadata import version, PackageNotFoundError

def PrintPythonDistributionVersion(DistributionName): #This is the distribution NOT module; For instance, the distribution "numpy-stl" is for the module "stl".
    try:
        print(DistributionName + ", version==" + str(version(DistributionName)))

    except PackageNotFoundError:
        print(DistributionName + " not installed.")
##########################################################################################################

##########################################################################################################
import numpy
PrintPythonDistributionVersion("numpy")

import PIL
from PIL import Image, ImageTk
PrintPythonDistributionVersion("Pillow")

import stl
from stl import mesh
PrintPythonDistributionVersion("numpy-stl")

import moderngl
PrintPythonDistributionVersion("moderngl")
##########################################################################################################

##########################################################################################################
import platform

if platform.system() == "Windows":
    import ctypes

    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1)  # Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################################################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
class STLviewerStandAloneProcess_ReubenPython3Class(Frame):  # Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict):

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if sys.version_info[0] < 3:
            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: Only Python 3 is supported, not 2.")
            return
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            
            multiprocessing_StartMethod = multiprocessing.get_start_method()
            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: multiprocessing.get_start_method(): " + str(multiprocessing_StartMethod))
            
            if multiprocessing_StartMethod != "spawn":
                print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: Issuing multiprocessing.set_start_method('spawn', force=True).")
                multiprocessing.set_start_method('spawn', force=True)  # 'spawn' is required for all Linux flavors, with 'force=True' required specicially by Ubuntu (not Raspberry Pi).
                
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: multiprocessing.set_start_method('spawn', force=True) Exceptions: %s" % exceptions)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        '''
        From: https://docs.python.org/3/library/multiprocessing.html#multiprocessing-programming
        Spawn
        The parent process starts a fresh python interpreter process.
        The child process will only inherit those resources necessary to run the process object’s run() method.
        In particular, unnecessary file descriptors and handles from the parent process will not be inherited.
        Starting a process using this method is rather slow compared to using fork or forkserver.
        Available on Unix and Windows. The default on Windows and macOS.
        '''

        self.MultiprocessingQueue_Rx = multiprocessing.Queue()  # NOT a regular Queue.queue
        self.MultiprocessingQueue_Tx = multiprocessing.Queue()  # NOT a regular Queue.queue
        self.job_for_another_core = multiprocessing.Process(target=self.StandAlonePlottingProcess, args=(self.MultiprocessingQueue_Rx, self.MultiprocessingQueue_Tx, SetupDict))  # args=(self.MultiprocessingQueue_Rx,)
        self.job_for_another_core.start()

        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_RegisterHandlerFunction(self):

        CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
        defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

        if CurrentHandlerRegisteredForSIGINT in defaultish:  # Only install if it's default/ignored (i.e., nobody set it yet)
            signal.signal(signal.SIGINT, self.CTRLc_HandlerFunction)
            print("STLviewerStandAloneProcess_ReubenPython3Class, CTRLc_RegisterHandlerFunction event fired!")

        else:
            print("STLviewerStandAloneProcess_ReubenPython3Class, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_HandlerFunction(self, signum, frame):

        print("STLviewerStandAloneProcess_ReubenPython3Class, CTRLc_HandlerFunction event firing!")

        self.SendEndCommandToStandAloneProcess()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __ProcessVariablesThatCanNOTbeLiveUpdated(self, SetupDict, PrintInfoForDebuggingFlag = 0):

        return 1 #Can add variables here later as needed.

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __ProcessVariablesThatCanBeLiveUpdated(self, SetupDict, PrintInfoForDebuggingFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.SetupDict = SetupDict
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.RootGeometryHasBeenModifiedFlag = 1 #By default, ALWAYS fire this event when we enter this function.
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if "GUIparametersDict" in SetupDict:
                GUIparametersDict = SetupDict["GUIparametersDict"]

                ##########################################
                ##########################################
                if "GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents" in GUIparametersDict:
                    self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"], 0.0, 1000.0))
                else:
                    self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents = 30  # Will get us around 30Hz actual when plottting 2 curves with 100 data points each and 35 tick marks on each axis

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents: " + str(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "EnableInternal_MyPrint_Flag" in GUIparametersDict:
                    self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", GUIparametersDict["EnableInternal_MyPrint_Flag"])
                else:
                    self.EnableInternal_MyPrint_Flag = 0

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "PrintToConsoleFlag" in GUIparametersDict:
                    self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", GUIparametersDict["PrintToConsoleFlag"])
                else:
                    self.PrintToConsoleFlag = 1

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "NumberOfPrintLines" in GUIparametersDict:
                    self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
                else:
                    self.NumberOfPrintLines = 10

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWidth" in GUIparametersDict:
                    self.GraphCanvasWidth = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWidth", GUIparametersDict["GraphCanvasWidth"], 480.0, 1000000.0))
                else:
                    self.GraphCanvasWidth = 640

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWidth: " + str(self.GraphCanvasWidth))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasHeight" in GUIparametersDict:
                    self.GraphCanvasHeight = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasHeight", GUIparametersDict["GraphCanvasHeight"], 240.0, 1000000.0))
                else:
                    self.GraphCanvasHeight = 480

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasHeight: " + str(self.GraphCanvasHeight))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWindowTitle" in GUIparametersDict:
                    self.GraphCanvasWindowTitle = str(GUIparametersDict["GraphCanvasWindowTitle"])
                else:
                    self.GraphCanvasWindowTitle = "STLviewerStandAloneProcess_ReubenPython3Class"

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWindowTitle: " + self.GraphCanvasWindowTitle)
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWindowStartingX" in GUIparametersDict:
                    self.GraphCanvasWindowStartingX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWindowStartingX", GUIparametersDict["GraphCanvasWindowStartingX"], 0.0, 1000000.0))
                else:
                    self.GraphCanvasWindowStartingX = 0.0

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWindowStartingX: " + str(self.GraphCanvasWindowStartingX))
                ##########################################
                ##########################################

                ##########################################
                ##########################################
                if "GraphCanvasWindowStartingY" in GUIparametersDict:
                    self.GraphCanvasWindowStartingY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GraphCanvasWindowStartingY", GUIparametersDict["GraphCanvasWindowStartingY"], 0.0, 1000000.0))
                else:
                    self.GraphCanvasWindowStartingY = 0.0

                if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: GraphCanvasWindowStartingY: " + str(self.GraphCanvasWindowStartingY))
                ##########################################
                ##########################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################
            ##########################################
            if "ParentPID" in SetupDict:
                self.ParentPID = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("ParentPID", SetupDict["ParentPID"], 0.0, 100000000.0))
            else:
                self.ParentPID = -11111

            if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: ParentPID: " + str(self.ParentPID))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "STLfileFullPath" in SetupDict:
                self.STLfileFullPath = str(SetupDict["STLfileFullPath"])
            else:
                self.STLfileFullPath = "cube.stl"

            if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: STLfileFullPath: " + str(self.STLfileFullPath))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess" in SetupDict:
                self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess",
                                                                                                                                                       SetupDict["WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess"], 0.0, 1000.0)
            else:
                self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess = 0.0

            if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess: " + str(self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "StandAlonePlottingProcess_TimeToSleepEachLoop" in SetupDict:

                ##########################################
                if self.OSnameStr == "windows":
                    self.StandAlonePlottingProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAlonePlottingProcess_TimeToSleepEachLoop", SetupDict["StandAlonePlottingProcess_TimeToSleepEachLoop"], 0.001, 1.0)
                ##########################################

                ##########################################
                elif self.OSnameStr == "pi":
                    self.StandAlonePlottingProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAlonePlottingProcess_TimeToSleepEachLoop", SetupDict["StandAlonePlottingProcess_TimeToSleepEachLoop"], 0.005, 1.0)  # Pi can't handle below 0.005
                ##########################################

                ##########################################
                else:
                    self.StandAlonePlottingProcess_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("StandAlonePlottingProcess_TimeToSleepEachLoop", SetupDict["StandAlonePlottingProcess_TimeToSleepEachLoop"], 0.001, 1.0)
                ##########################################

            else:
                self.StandAlonePlottingProcess_TimeToSleepEachLoop = 0.030

            if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: StandAlonePlottingProcess_TimeToSleepEachLoop: " + str(self.StandAlonePlottingProcess_TimeToSleepEachLoop))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "KeepPlotterWindowAlwaysOnTopFlag" in SetupDict:
                self.KeepPlotterWindowAlwaysOnTopFlag = self.PassThrough0and1values_ExitProgramOtherwise("KeepPlotterWindowAlwaysOnTopFlag", SetupDict["KeepPlotterWindowAlwaysOnTopFlag"])
            else:
                self.KeepPlotterWindowAlwaysOnTopFlag = 0

            if PrintInfoForDebuggingFlag == 1: print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class __init__: KeepPlotterWindowAlwaysOnTopFlag: " + str(self.KeepPlotterWindowAlwaysOnTopFlag))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag" in SetupDict:
                self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag = self.PassThrough0and1values_ExitProgramOtherwise("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", SetupDict["RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag"])
            else:
                self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag = 0

            if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag: " + str(self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "AllowResizingOfWindowFlag" in SetupDict:
                self.AllowResizingOfWindowFlag = self.PassThrough0and1values_ExitProgramOtherwise("AllowResizingOfWindowFlag", SetupDict["AllowResizingOfWindowFlag"])
            else:
                self.AllowResizingOfWindowFlag = 1

            if PrintInfoForDebuggingFlag == 1: print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: AllowResizingOfWindowFlag: " + str(self.AllowResizingOfWindowFlag))
            ##########################################
            ##########################################
            
            ##########################################
            ##########################################
            if "UDPdataExchanger___IPV4_address" in SetupDict:
                self.UDPdataExchanger___IPV4_address = str(SetupDict["UDPdataExchanger___IPV4_address"])

            else:
                self.UDPdataExchanger___IPV4_address = "127.0.0.1"

            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: UDPdataExchanger___IPV4_address: " + str(self.UDPdataExchanger___IPV4_address))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "UDPdataExchanger___IPV4_Port" in SetupDict:
                self.UDPdataExchanger___IPV4_Port = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDPdataExchanger___IPV4_Port", SetupDict["UDPdataExchanger___IPV4_Port"], 1, 65535)) #port 0 doesn't work

            else:
                self.UDPdataExchanger___IPV4_Port = 1

            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: UDPdataExchanger___IPV4_Port: " + str(self.UDPdataExchanger___IPV4_Port))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "UDPdataExchanger___UDP_BufferSizeInBytes" in SetupDict:
                self.UDPdataExchanger___UDP_BufferSizeInBytes = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDPdataExchanger___UDP_BufferSizeInBytes", SetupDict["UDPdataExchanger___UDP_BufferSizeInBytes"], 1, 1500)) #Max-packet-size is 1500 in-practice (maximum transmission unit (MTU) to prevent packet-fragmenting), 65507 bytes in theory-only

            else:
                self.UDPdataExchanger___UDP_BufferSizeInBytes = 64

            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: UDPdataExchanger___UDP_BufferSizeInBytes: " + str(self.UDPdataExchanger___UDP_BufferSizeInBytes))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds" in SetupDict:
                self.UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds", SetupDict["UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds"], 0.0, 1000000.0)

            else:
                self.UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds = 1.0

            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated:  UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds: " + str(self.UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "UDPdataExchanger___MainThread_TimeToSleepEachLoop" in SetupDict:
                self.UDPdataExchanger___MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDPdataExchanger___MainThread_TimeToSleepEachLoop", SetupDict["UDPdataExchanger___MainThread_TimeToSleepEachLoop"], 0.001, 100000)

            else:
                self.UDPdataExchanger___MainThread_TimeToSleepEachLoop = 0.002

            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated:  UDPdataExchanger___MainThread_TimeToSleepEachLoop: " + str(self.UDPdataExchanger___MainThread_TimeToSleepEachLoop))
            ##########################################
            ##########################################

            ##########################################
            ##########################################
            if "UDPdataExchanger___WatchdogTimerExpirationDurationSeconds" in SetupDict:
                self.UDPdataExchanger___WatchdogTimerExpirationDurationSeconds = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UDPdataExchanger___WatchdogTimerExpirationDurationSeconds", SetupDict["UDPdataExchanger___WatchdogTimerExpirationDurationSeconds"], 0.000, 100000.0)

            else:
                self.UDPdataExchanger___WatchdogTimerExpirationDurationSeconds = 0.25

            print("UDPdataExchanger_ReubenPython3Class __init__: UDPdataExchanger___WatchdogTimerExpirationDurationSeconds: " + str(self.UDPdataExchanger___WatchdogTimerExpirationDurationSeconds))
            ##########################################
            ##########################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            return 1

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("STLviewerStandAloneProcess_ReubenPython3Class __init__, __ProcessVariablesThatCanBeLiveUpdated: exceptions: %s" % exceptions)
            #traceback.print_exc()
            return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def GetCPUandMemoryUsageOfProcessByPID(self, Process_PID, PrintInfoForDebuggingFlag=0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            ProcessObject = psutil.Process(Process_PID)

            if self.GetCPUandMemoryUsageOfProcessByPID_MeasurementWarmedUpFlag == 0:
                ProcessObject.cpu_percent(interval=0.1)  # First call returns 0.0 but wamrs up the measurement.
                self.GetCPUandMemoryUsageOfProcessByPID_MeasurementWarmedUpFlag = 1

            CPUusage_Percent = ProcessObject.cpu_percent(interval=0.0)  # Use a short interval, 0.0 for non-blocking

            MemoryInfo = ProcessObject.memory_info()
            MemoryUsage_MB = MemoryInfo.rss / (1024 * 1024)  # Convert to MB

            MemoryUsage_Percent = ProcessObject.memory_percent()

            DictToReturn = dict([("CPUusage_Percent", round(CPUusage_Percent, 5)),
                                 ("MemoryUsage_Percent", round(MemoryUsage_Percent, 5)),
                                 ("MemoryUsage_MB", round(MemoryUsage_MB, 5))])

            ##########################################################################################################
            ##########################################################################################################
            if PrintInfoForDebuggingFlag == 1:
                print("GetCPUandMemoryUsageOfProcessByPID: For Process_PID = " + str(Process_PID) + "DictToReturn = " + str(DictToReturn))
            ##########################################################################################################
            ##########################################################################################################

            return DictToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetCPUandMemoryUsageOfProcessByPID, exceptions: %s" % exceptions)
            # traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    @staticmethod
    def GetOSnameStr(PrintInfoForDebuggingFlag=0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if platform.system() == "Linux":

                if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
                    OSnameStr = "pi"

                else:
                    OSnameStr = "linux"
            ##########################################################################################################

            ##########################################################################################################
            elif platform.system() == "Windows":
                OSnameStr = "windows"
            ##########################################################################################################

            ##########################################################################################################
            elif platform.system() == "Darwin":
                OSnameStr = "mac"
            ##########################################################################################################

            ##########################################################################################################
            else:
                OSnameStr = "other"
            ##########################################################################################################

            ##########################################################################################################
            if PrintInfoForDebuggingFlag == 1:
                print("GetOSnameStr: The OS is: " + OSnameStr)
            ##########################################################################################################

            ##########################################################################################################
            return OSnameStr
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        except:

            exceptions = sys.exc_info()[0]
            print("STLviewerStandAloneProcess_ReubenPython3Class: GetOSnameStr, exceptions: %s" % exceptions)
            # traceback.print_exc()
            return ""

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def WatchdogTimerCheck(self):

        #############################################
        if self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess > 0.0:
            self.TimeIntoWatchdogTimer = self.CurrentTime_CalculatedFromStandAlonePlottingProcess - self.LastTime_CalculatedFromStandAlonePlottingProcess

            if self.TimeIntoWatchdogTimer >= self.WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess:
                print("***** STLviewerStandAloneProcess_ReubenPython3Class, Watchdog fired! *****")
                #self.EXIT_PROGRAM_FLAG = 1
        #############################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def StandAlonePlottingProcess(self, MultiprocessingQueue_Rx_Local, MultiprocessingQueue_Tx_Local, SetupDict):

        print("Entering STLviewerStandAloneProcess_ReubenPython3Class StandAlonePlottingProcess.")

        ##########################################
        self.EXIT_PROGRAM_FLAG = 0
        self.GUI_ready_to_be_updated_flag = 0
        ##########################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        SuccessFlag = self.__ProcessVariablesThatCanNOTbeLiveUpdated(SetupDict, PrintInfoForDebuggingFlag = 1)
        if SuccessFlag != 1:
            self.EXIT_PROGRAM_FLAG = 1

        self.RootGeometryHasBeenModified_HasThisEventFiredBeforeFlag = 0
        self.__ProcessVariablesThatCanBeLiveUpdated(SetupDict, PrintInfoForDebuggingFlag = 1)
        if SuccessFlag != 1:
            self.EXIT_PROGRAM_FLAG = 1

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################
        self.OSnameStr = STLviewerStandAloneProcess_ReubenPython3Class.GetOSnameStr()
        self.SelfPID = os.getpid()
        ##########################################

        ##########################################
        self.PrintToGui_Label_TextInputHistory_List = [" "] * self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        ##########################################

        ##########################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150)  # RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        ##########################################

        ##########################################
        self.GraphBoxOutline_X0 = 50  # Offset from the Canvas object so that there's room for the axis-labels
        self.GraphBoxOutline_Y0 = 50  # Offset from the Canvas object so that there's room for the axis-labels
        ##########################################

        ##########################################
        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.StartingTime_CalculatedFromGUIthread = -11111.0
        self.LoopFrequency_CalculatedFromGUIthread = -11111.0
        self.LoopDeltaT_CalculatedFromGUIthread = -11111.0
        ##########################################

        ##########################################
        self.CurrentTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LastTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.StartingTime_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LoopFrequency_CalculatedFromStandAlonePlottingProcess = -11111.0
        self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess = -11111.0

        self.TimeIntoWatchdogTimer = 0.0
        ##########################################

        ##########################################
        self.StandAlonePlottingProcess_ReadyForWritingFlag = 0
        ##########################################

        ##########################################
        self.MemoryUsageOfProcessByPID_Dict = dict([("CPUusage_Percent", -1),
                                                    ("MemoryUsage_Percent", -1),
                                                    ("MemoryUsage_MB", -1)])
        ##########################################

        ##########################################
        self.Quaternion = [0, 0, 0, 1]
        ##########################################

        ##########################################
        self.MostRecentDataDict = dict()
        ##########################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################
        self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG = 0
        ##########################################

        ##########################################
        try:
            if GetCPUandMemoryUsageOfProcessByPID_ModuleImportedFlag == 1 and self.EXIT_PROGRAM_FLAG == 0:
                self.GetCPUandMemoryUsageOfProcessByPID_Object = GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class(dict([("Process_PID_Integer", self.SelfPID)]))
                self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG = self.GetCPUandMemoryUsageOfProcessByPID_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("STLviewerStandAloneProcess_ReubenPython3Class, StandAlonePlottingProcess, GetCPUandMemoryUsageOfProcessByPID_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.CTRLc_RegisterHandlerFunction()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## unicorn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        #################################################
        #################################################
        self.UDPdataExchanger_OPEN_FLAG = 0
        self.UDPdataExchanger_MostRecentDict = dict()
        #################################################
        #################################################

        #################################################
        #################################################

        #################################################
        self.UDPdataExchanger___USE_UDPdataExchanger_FLAG = 1
        self.SHOW_IN_GUI_UDPdataExchanger_FLAG = 1
        #################################################

        #################################################
        self.UDPdataExchanger_GUIparametersDict = dict([("USE_GUI_FLAG", self.UDPdataExchanger___USE_UDPdataExchanger_FLAG and self.SHOW_IN_GUI_UDPdataExchanger_FLAG),
                                                       ("EnableInternal_MyPrint_Flag", 0),
                                                       ("NumberOfPrintLines", 10),
                                                       ("UseBorderAroundThisGuiObjectFlag", 0),
                                                       ("GUI_ROW", 0),
                                                       ("GUI_COLUMN", 0),
                                                       ("GUI_PADX", 1),
                                                       ("GUI_PADY", 1),
                                                       ("GUI_ROWSPAN", 1),
                                                       ("GUI_COLUMNSPAN", 1)])
        #################################################

        #################################################
        self.UDPdataExchanger_SetupDict = dict([("GUIparametersDict", self.UDPdataExchanger_GUIparametersDict),
                                                ("NameToDisplay_UserSet", "UDPdataExchanger"),
                                                ("UDP_RxOrTxRole", "rx"),
                                                ("IPV4_address", self.UDPdataExchanger___IPV4_address),
                                                ("IPV4_Port", self.UDPdataExchanger___IPV4_Port),
                                                ("UDP_BufferSizeInBytes", self.UDPdataExchanger___UDP_BufferSizeInBytes),
                                                ("UDP_TimeoutAtPortLevelInSeconds", self.UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds),
                                                ("WatchdogTimerExpirationDurationSeconds", self.UDPdataExchanger___WatchdogTimerExpirationDurationSeconds),
                                                ("MainThread_TimeToSleepEachLoop", self.UDPdataExchanger___MainThread_TimeToSleepEachLoop)])
        #################################################

        #################################################
        if self.UDPdataExchanger___USE_UDPdataExchanger_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:
            try:
                self.UDPdataExchanger_Object = UDPdataExchanger_ReubenPython3Class(self.UDPdataExchanger_SetupDict)
                self.UDPdataExchanger_OPEN_FLAG = self.UDPdataExchanger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

                #################################################
                if self.UDPdataExchanger_OPEN_FLAG != 1:
                    print("WARNING: STLviewerStandAloneProcess_ReubenPython3Class, StandAlonePlottingProcess: Failed to open UDPdataExchanger_ReubenPython3ClassObject.")
                else:
                    print("STLviewerStandAloneProcess_ReubenPython3Class, StandAlonePlottingProcess: opened UDPdataExchanger_ReubenPython3ClassObject.")
                #################################################

            except:
                exceptions = sys.exc_info()[0]
                print("STLviewerStandAloneProcess_ReubenPython3Class, StandAlonePlottingProcess, UDPdataExchanger_ReubenPython3ClassObject __init__: exceptions: %s" % exceptions)
                traceback.print_exc()
        #################################################

        #################################################
        #################################################

        #################################################
        #################################################
        if self.EXIT_PROGRAM_FLAG == 0:
            self.StartGUI()
        #################################################
        #################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.StartingTime_CalculatedFromStandAlonePlottingProcess = self.getPreciseSecondsTimeStampString()
        self.LastTime_CalculatedFromStandAlonePlottingProcess = self.StartingTime_CalculatedFromStandAlonePlottingProcess
        self.StandAlonePlottingProcess_ReadyForWritingFlag = 1


        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromStandAlonePlottingProcess = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromStandAlonePlottingProcess
                
                self.WatchdogTimerCheck()
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG == 1:
                    GetCPUandMemoryUsageOfProcessByPID_MostRecentDict = self.GetCPUandMemoryUsageOfProcessByPID_Object.GetMostRecentDataDict()

                    if "MemoryUsageOfProcessByPID_Dict" in GetCPUandMemoryUsageOfProcessByPID_MostRecentDict:
                        self.MemoryUsageOfProcessByPID_Dict = GetCPUandMemoryUsageOfProcessByPID_MostRecentDict["MemoryUsageOfProcessByPID_Dict"]
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.UDPdataExchanger_OPEN_FLAG == 1:

                    try:
                        self.UDPdataExchanger_MostRecentDict = self.UDPdataExchanger_Object.GetMostRecentDataDict()
                        #print("self.UDPdataExchanger_MostRecentDict: " + str(self.UDPdataExchanger_MostRecentDict))

                        if "MostRecentMessage_Rx_Dict" in self.UDPdataExchanger_MostRecentDict:
                            if "Quaternion" in self.UDPdataExchanger_MostRecentDict["MostRecentMessage_Rx_Dict"]:
                                self.Quaternion = self.UDPdataExchanger_MostRecentDict["MostRecentMessage_Rx_Dict"]["Quaternion"]

                    except:
                        exceptions = sys.exc_info()[0]
                        print("STLviewerStandAloneProcess_ReubenPython3Class, StandAlonePlottingProcess, self.UDPdataExchanger_Object.GetMostRecentDataDict(): exceptions: %s" % exceptions)
                        traceback.print_exc()
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                while not MultiprocessingQueue_Rx_Local.empty():

                    ##########################################################################################################
                    ##########################################################################################################
                    self.UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess() #ONLY UPDATE IF WE GET A DATA PACKET
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    inputDict = MultiprocessingQueue_Rx_Local.get(FALSE)  # for queue, non-blocking with "FALSE" argument, could also use MultiprocessingQueue_Rx_Local.get_nowait() for non-blocking
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    if "YaxisAutoscaleFlag" in inputDict: #Check if a SetupDict is being passed-in
                        self.__ProcessVariablesThatCanBeLiveUpdated(inputDict, PrintInfoForDebuggingFlag=0)
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    else:

                        ##########################################################################################################
                        if "EndStandAloneProcessFlag" in inputDict:
                            self.EXIT_PROGRAM_FLAG = 1
                        ##########################################################################################################

                        ##########################################################################################################
                        if "ResetMinAndMax" in inputDict:
                            self.ResetMinAndMax()
                        ##########################################################################################################

                        ##########################################################################################################
                        else: #MAIN DATA PLOTTING CALL

                            if "Quaternion" in inputDict:

                                self.Quaternion = inputDict["Quaternion"]

                        ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.MostRecentDataDict = dict([("StandAlonePlottingProcess_ReadyForWritingFlag", self.StandAlonePlottingProcess_ReadyForWritingFlag)])

                MultiprocessingQueue_Tx_Local.put(self.MostRecentDataDict.copy())
                # MultiprocessingQueue_Tx_Local.put(deepcopy(self.MostRecentDataDict)) #deepcopy is required (beyond .copy() ) because self.MostRecentDataDict contains a dict.
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                time.sleep(self.StandAlonePlottingProcess_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            except:
                exceptions = sys.exc_info()[0]
                print("STLviewerStandAloneProcess_ReubenPython3Class, StandAlonePlottingProcess, exceptions: %s" % exceptions)
                traceback.print_exc()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            if self.GetCPUandMemoryUsageOfProcessByPID_OPEN_FLAG == 1:
                self.GetCPUandMemoryUsageOfProcessByPID_Object.ExitProgram_Callback()
        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            if self.UDPdataExchanger_OPEN_FLAG == 1:
                self.UDPdataExchanger_Object.ExitProgram_Callback()
        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## Drain all remaining items in Queues OR ELSE THIS THREAD WON'T DRAIN.
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            while True:
                try:
                    DummyToDrainRemainingItemsInRxQueue = self.MultiprocessingQueue_Rx.get_nowait()

                except Empty:
                    break
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            while True:
                try:
                    DummyToDrainRemainingItemsInTxQueue = self.MultiprocessingQueue_Tx.get_nowait()

                except Empty:
                    break
            ##########################################################################################################
            ##########################################################################################################

            self.job_for_another_core.close()
            self.job_for_another_core.join()

        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        print("Exited STLviewerStandAloneProcess_ReubenPython3Class.")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendEndCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("EndStandAloneProcessFlag", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def SendResetMinAndMaxCommandToStandAloneProcess(self):

        try:
            self.MultiprocessingQueue_Rx.put(dict([("ResetMinAndMax", 1)]))
        except:
            pass

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ExternalUpdateRotationQuaternion(self, Quaternion):

        if isinstance(Quaternion, list) != 1:
           print("ExternalUpdateRotationQuaternion: Error, input must be a list.")
           return

        if len(Quaternion) != 4:
            print("ExternalUpdateRotationQuaternion: Error, input must be a list of length 4.")
            return

        ###########################################
        self.MultiprocessingQueue_Rx.put(dict([("Quaternion", Quaternion)]))
        ###########################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ExternalUpdateSetupDict(self, SetupDict):

        if isinstance(SetupDict, dict) == 1:

            self.MultiprocessingQueue_Rx.put(SetupDict)

        else:
            self.MultiprocessingQueue_Rx.put(dict())

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def Quaternion_Normalize(self, q):

        w, x, y, z = q
        m = math.sqrt(w * w + x * x + y * y + z * z)

        if m == 0:
            return (1, 0, 0, 0)

        return (w / m, x / m, y / m, z / m)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def Quaterionion_FromAxisAngleRepresentation(self, axis, angle):

        ax, ay, az = axis
        n = math.sqrt(ax * ax + ay * ay + az * az)

        if n == 0:
            return (1, 0, 0, 0)

        ax, ay, az = ax / n, ay / n, az / n
        s = math.sin(angle / 2)

        return (math.cos(angle / 2), ax * s, ay * s, az * s)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def Quaternion_MultiplyViaHamiltonProduct(self, q2, q1):

        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        return (w2 * w1 - x2 * x1 - y2 * y1 - z2 * z1,
                w2 * x1 + x2 * w1 + y2 * z1 - z2 * y1,
                w2 * y1 - x2 * z1 + y2 * w1 + z2 * x1,
                w2 * z1 + x2 * y1 - y2 * x1 + z2 * w1)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    """
    Objects You Can Reuse (Shared for All STL Files)
    These can be created once and reused for all models:
    self.ModernGL_Context → the rendering context (ModernGL requires only one)
    Shader programs (self.ModernGL_Program) → if all STL models use the same vertex/fragment shader logic
    Projection matrix (self.proj_uniform) → usually shared across the scene
    View matrix (self.view_uniform) → shared camera
    
    Each STL file (i.e., each 3D object) must have its own set of GPU resources to allow independent positioning/rotation. You’ll need:
        Vertex buffer (VBO)	Each STL file has its own vertex data
        Vertex array object (VAO)	Tied to the VBO and shader attributes
        Model quaternion	Each object must rotate independently
        model_quat_uniform reference	To update the model rotation per object
        Draw call	Each object must be rendered separately
    """
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def LoadSTLfileAndSmoothNormals(self):

        m = mesh.Mesh.from_file(self.STLfileFullPath)
        verts = m.vectors.reshape(-1, 3).astype(numpy.float32)

        # Smooth normals
        norms = numpy.zeros_like(verts)
        tris = verts.reshape(-1, 3, 3)
        for i, tri in enumerate(tris):
            v1 = tri[1] - tri[0]
            v2 = tri[2] - tri[0]
            n = numpy.cross(v1, v2)
            ln = numpy.linalg.norm(n)
            if ln > 0:
                n /= ln
            idx = i * 3
            norms[idx + 0] += n
            norms[idx + 1] += n
            norms[idx + 2] += n

        ln = numpy.linalg.norm(norms, axis=1)
        ln[ln == 0] = 1
        norms /= ln[:, None]

        # Uniform scale normalization (NO axis hacking)
        mn = verts.min(axis=0)
        mx = verts.max(axis=0)
        center = (mn + mx) / 2.0
        size = (mx - mn).max()

        verts = (verts - center) / (size / 1.8)

        # Interleave
        inter = numpy.hstack([verts, norms]).astype(numpy.float32)
        self.ModernGL_VertexBufferObject_VBO = self.ModernGL_Context.buffer(inter.tobytes())
        self.vertex_count = len(verts)
        
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    # ---------------------------------------------------------
    # SHADERS (PERSPECTIVE + QUAT + LIGHTING)
    # ---------------------------------------------------------

    def CreateProgram(self):

        # ---------------------------------------------------------
        # MAIN PROGRAM (for STL model)
        # NOTE: The following code is actual GLSL (OpenGL Shading Language) source code provided as multi-line Python strings (""" ... """). This code is fully active and gets compiled into a ModernGL shader program.
        # It is NOT commented out and must remain here.
        # In GLSL, lines beginning with # such as #version 330 are preprocessor directives, not comments. They serve a crucial role in setting the shader version or defining macros, similar to #include or #define in C/C++.

        # ---------------------------------------------------------
        self.ModernGL_Program = self.ModernGL_Context.program(
            vertex_shader="""
                #version 330

                in vec3 in_pos;
                in vec3 in_normal;

                uniform vec4 QuaternionOfModel;
                uniform vec4 QuaternionOfView;
                uniform mat4 ProjectionMatrix;
                uniform mat4 ViewMatrix;

                out vec3 v_normal;
                out vec3 v_world;

                vec4 Quaternion_MultiplyViaHamiltonProduct(vec4 q2, vec4 q1){
                    return vec4(
                        q2.x*q1.x - q2.y*q1.y - q2.z*q1.z - q2.w*q1.w,
                        q2.x*q1.y + q2.y*q1.x + q2.z*q1.w - q2.w*q1.z,
                        q2.x*q1.z - q2.y*q1.w + q2.z*q1.x + q2.w*q1.y,
                        q2.x*q1.w + q2.y*q1.z - q2.z*q1.y + q2.w*q1.x
                    );
                }

                vec3 quat_rot(vec3 p, vec4 q){
                    float w = q.x;
                    vec3 v = q.yzw;
                    vec3 t = 2.0 * cross(v, p);
                    return p + w * t + cross(v, t);
                }

                void main() {
                    vec4 q = normalize(Quaternion_MultiplyViaHamiltonProduct(QuaternionOfView, QuaternionOfModel));

                    vec3 p = quat_rot(in_pos,    q);
                    vec3 n = quat_rot(in_normal, q);

                    v_world  = p;
                    v_normal = n;

                    gl_Position = ProjectionMatrix * ViewMatrix * vec4(p, 1.0);
                }
            """,

            fragment_shader="""
                #version 330

                in vec3 v_normal;
                in vec3 v_world;

                out vec4 f_color;

                void main() {
                    vec3 N = normalize(v_normal);
                    vec3 L = normalize(vec3(0.4, 0.6, 1.0));

                    float diff = max(dot(N, L), 0.0);
                    vec3 diffuse = diff * vec3(0.95, 0.95, 1.0);
                    vec3 ambient = vec3(0.15, 0.15, 0.18);

                    f_color = vec4(diffuse + ambient, 1.0);
                }
            """
        )

        self.QuaternionOfModel_uniform = self.ModernGL_Program["QuaternionOfModel"]
        self.QuaternionOfView_uniform = self.ModernGL_Program["QuaternionOfView"]
        self.ProjectionMatrix_uniform = self.ModernGL_Program["ProjectionMatrix"]
        self.ViewMatrix_uniform = self.ModernGL_Program["ViewMatrix"]

        self.QuaternionOfModel_uniform.value = self.QuaternionOfModel
        self.QuaternionOfView_uniform.value = self.QuaternionOfView

        # ---------------------------------------------------------
        # AXES PROGRAM (simple colored lines)
        # ---------------------------------------------------------
        self.ModernGL_Program_Axes = self.ModernGL_Context.program(
            vertex_shader="""
                #version 330

                in vec3 in_pos;
                in vec3 in_color;

                uniform vec4 QuaternionOfView;
                uniform mat4 ProjectionMatrix;
                uniform mat4 ViewMatrix;

                out vec3 v_color;

                vec3 quat_rot(vec3 p, vec4 q){
                    float w = q.x;
                    vec3 v = q.yzw;
                    vec3 t = 2.0 * cross(v, p);
                    return p + w * t + cross(v, t);
                }

                void main()
                {
                    vec3 p = quat_rot(in_pos, QuaternionOfView);
                    gl_Position = ProjectionMatrix * ViewMatrix * vec4(p, 1.0);
                    v_color = in_color;
                }
            """,

            fragment_shader="""
                #version 330

                in vec3 v_color;
                out vec4 f_color;

                void main()
                {
                    f_color = vec4(v_color, 1.0);
                }
            """
        )

        self.Axes_ProjectionMatrix_uniform = self.ModernGL_Program_Axes["ProjectionMatrix"] #In OpenGL and ModernGL, a "uniform" is a special kind of variable in a shader program. It is constant during the drawing of a frame, and it is set from the CPU side (Python in this case), and read-only on the GPU (shader).
        self.Axes_ViewMatrix_uniform = self.ModernGL_Program_Axes["ViewMatrix"] #In OpenGL and ModernGL, a "uniform" is a special kind of variable in a shader program. It is constant during the drawing of a frame, and it is set from the CPU side (Python in this case), and read-only on the GPU (shader).
        self.Axes_QuaternionOfView_uniform = self.ModernGL_Program_Axes["QuaternionOfView"] #In OpenGL and ModernGL, a "uniform" is a special kind of variable in a shader program. It is constant during the drawing of a frame, and it is set from the CPU side (Python in this case), and read-only on the GPU (shader).

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CreateVertexArrayObject(self):

        self.ModernGL_VertexArrayObject_VAO = self.ModernGL_Context.vertex_array(self.ModernGL_Program, [(self.ModernGL_VertexBufferObject_VBO, "3f4 3f4", "in_pos", "in_normal")])
        
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    # ---------------------------------------------------------
    # This function returns a perspective projection matrix. It's used to transform 3D coordinates from camera space into clip space — this is what makes distant objects look smaller, mimicking human vision.
    # ---------------------------------------------------------

    def CalculateProjectionMatrix(self):

        fov = math.radians(55)
        aspect = self.GraphCanvasWidth / self.GraphCanvasHeight

        near = 0.05 #Clipping plane
        far = 200.0 #Clipping plane

        f = 1.0 / math.tan(fov / 2.0)

        ProjectionMatrix = numpy.array([[f/aspect, 0, 0,                       0],
                                    [0,         f, 0,                       0],
                                    [0,         0, (far+near)/(near-far),   (2*far*near)/(near-far)],
                                    [0,         0, -1,                      0]],
                            dtype=numpy.float32).T

        return ProjectionMatrix
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    # ---------------------------------------------------------
    # This function returns a view (camera) matrix, which transforms world coordinates into camera (view) space — like moving or rotating the world around the camera.
    # ---------------------------------------------------------

    def CalculateViewMatrix(self):
        # Simple camera: back along +Z

        ViewMatrix = numpy.array([[1, 0, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 1, -self.dist],
                               [0, 0, 0, 1]],
                    dtype=numpy.float32).T

        return ViewMatrix
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    # ---------------------------------------------------------
    # PUBLIC API: SET MODEL QUATERNION
    # ---------------------------------------------------------

    def SetModelQuaternion(self, QuaternionListWXYZ=[1.0, 0.0, 0.0, 0.0]):

        if isinstance(QuaternionListWXYZ, list) != 1:
            print("SetModelQuaternion: Error, QuaternionListWXYZ must be a list.")
            return

        if len(QuaternionListWXYZ) != 4:
            print("SetModelQuaternion: Error, QuaternionListWXYZ must be a list of length 4.")
            return

        w = QuaternionListWXYZ[0]
        x = QuaternionListWXYZ[1]
        y = QuaternionListWXYZ[2]
        z = QuaternionListWXYZ[3]

        q = self.Quaternion_Normalize((w, x, y, z))
        self.QuaternionOfModel = q
        self.QuaternionOfModel_uniform.value = q

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be 0 or 1 (value was " +
                      str(InputNumber_ConvertedToFloat) +
                      ").")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        # We used to use this method, but it gave us the root calling file, not the class calling file
        # absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py", "")

        return filename
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def getTimeStampString(self):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

        return st
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        try:
            if self.MultiprocessingQueue_Tx.empty() != 1:
                return self.MultiprocessingQueue_Tx.get(FALSE)
            else:
                return dict()

        except:
            exceptions = sys.exc_info()[0]
            print("STLviewerStandAloneProcess_ReubenPython3Class, GetMostRecentDataDict, Exceptions: %s" % exceptions)
            # traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromGUIthread(self):

        try:
            self.LoopDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            ##########################
            if self.LoopDeltaT_CalculatedFromGUIthread != 0.0:
                self.LoopFrequency_CalculatedFromGUIthread = 1.0 / self.LoopDeltaT_CalculatedFromGUIthread
            ##########################

            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromGUIthread ERROR, exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess(self):

        try:
            self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess = self.CurrentTime_CalculatedFromStandAlonePlottingProcess - self.LastTime_CalculatedFromStandAlonePlottingProcess

            ##########################
            if self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess != 0.0:
                self.LoopFrequency_CalculatedFromStandAlonePlottingProcess = 1.0 / self.LoopDeltaT_CalculatedFromStandAlonePlottingProcess
            ##########################

            self.LastTime_CalculatedFromStandAlonePlottingProcess = self.CurrentTime_CalculatedFromStandAlonePlottingProcess

        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("UpdateFrequencyCalculation_CalculatedFromStandAlonePlottingProcess ERROR, exceptions: %s" % exceptions)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for STLviewerStandAloneProcess_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1

        self.SendEndCommandToStandAloneProcess()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self):

        self.GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread)  # 05/10/2023, MUST LAUNCH THIS WAY, CANNOT DO 'self.GUI_Thread() as with other classes'
        self.GUI_Thread_ThreadingObject.setDaemon(True)  # Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        self.GUI_Thread_ThreadingObject.start()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def RootConfigurationUpdate(self):

        ###################################################
        ###################################################
        self.root.title(self.GraphCanvasWindowTitle)
        self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)
        self.root.geometry('%dx%d+%d+%d' % (self.GraphCanvasWidth + 700, self.GraphCanvasHeight + 80, self.GraphCanvasWindowStartingX, self.GraphCanvasWindowStartingY))  # +50 for Debug_Label
        self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.root.resizable(bool(self.AllowResizingOfWindowFlag), bool(self.AllowResizingOfWindowFlag))  #horizontal, vertical
        self.root.overrideredirect(bool(self.RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag))  # Removes title bar, border, and close-button. Disallows movement of the window.
        self.root.wm_attributes('-topmost', bool(self.KeepPlotterWindowAlwaysOnTopFlag))
        ###################################################
        ###################################################

        ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
        ###################################################
        default_font = tkFont.nametofont("TkDefaultFont")  # TkTextFont, TkFixedFont
        default_font.configure(size=8)
        self.root.option_add("*Font", default_font)
        ###################################################
        ###################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ###################################################
        ###################################################
        self.root = Tk()
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.myFrame = Frame(self.root, bg="white")
        self.myFrame.grid()
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.RootConfigurationUpdate()
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.CanvasForDrawingGraph = Canvas(self.myFrame, width=self.GraphCanvasWidth, height=self.GraphCanvasHeight, bg="white")
        self.CanvasForDrawingGraph["highlightthickness"] = 0  # Remove light grey border around the Canvas
        self.CanvasForDrawingGraph["bd"] = 0  # Setting "bd", along with "highlightthickness" to 0 makes the Canvas be in the (0,0) pixel location instead of offset by those thicknesses
        '''
        From https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget
        The short answer is, the Canvas has two components which affect the edges: the border (borderwidth attribute) and highlight ring (highlightthickness attribute).
        If you have a border width of zero and a highlight thickness of zero, the canvas coordinates will begin at 0,0. Otherwise, these two components of the canvas infringe upon the coordinate space.
        What I most often do is set these attributes to zero. Then, if I actually want a border I'll put that canvas inside a frame and give the frame a border.
        '''

        self.CanvasForDrawingGraph.bind("<ButtonPress-1>", lambda event: self.OnCanvasMouseDownCallbackFunction(event))
        self.CanvasForDrawingGraph.bind("<B1-Motion>", lambda event: self.OnCanvasMouseDragCallbackFunction(event))
        self.CanvasForDrawingGraph.bind("<MouseWheel>", lambda event: self.OnCanvasMouseWheelCallbackFunction(event))

        self.CanvasForDrawingGraph.grid(row=0, column=0, padx=0, pady=0)
        self._canvas_image_id = None
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.Debug_Label = Label(self.myFrame, text="Debug_Label", width=150, bg="white")
        self.Debug_Label.grid(row=1, column=0, padx=0, pady=0, columnspan=1, rowspan=1, sticky="w")
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.PlotControlsFrame = Frame(self.myFrame, bg="white")
        self.PlotControlsFrame.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="w")
        ###################################################
        ###################################################

        self.ButtonWidth = 15

        ###################################################
        ###################################################
        self.ResetMinAndMax_Button = Button(self.PlotControlsFrame, text='ResetMinMax', state="normal", width=self.ButtonWidth, font=("Helvetica", 8), command=lambda i=1: self.ResetMinAndMax_ButtonResponse())
        self.ResetMinAndMax_Button.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.UDPdataExchanger_Frame = Frame(self.myFrame, bg="white")
        self.UDPdataExchanger_Frame.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1, sticky="w")
        ###################################################
        ###################################################

        ###################################################
        ###################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=100, bg="white")
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=0, pady=0, columnspan=1, rowspan=1)
        ###################################################
        ###################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if self.UDPdataExchanger_OPEN_FLAG == 1:
            self.UDPdataExchanger_Object.CreateGUIobjects(TkinterParent=self.UDPdataExchanger_Frame)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## unicorn
        ##########################################################################################################
        ##########################################################################################################

        # Model + view rotation
        self.QuaternionOfModel = (1, 0, 0, 0)
        self.QuaternionOfView = (1, 0, 0, 0)

        # Camera
        self.yaw = 0.0
        self.pitch = 0.0
        self.dist = 4.0  # camera distance

        # Mouse tracking
        self._last_x = None
        self._last_y = None

        # ModernGL setup
        self.ModernGL_Context = moderngl.create_standalone_context()
        self.ModernGL_Context.enable(moderngl.DEPTH_TEST)  # <-- CRITICAL: enable depth test
        self.ModernGL_Context.disable(moderngl.CULL_FACE)  # draw both sides

        self.ModernGL_FrameBufferObject_FBO = self.ModernGL_Context.simple_framebuffer((self.GraphCanvasWidth, self.GraphCanvasHeight))
        self.ModernGL_FrameBufferObject_FBO.use()

        # Geometry + GPU objects
        self.LoadSTLfileAndSmoothNormals()
        self.CreateProgram()
        self.CreateVertexArrayObject()

        self._photo = None

        self.CreateAxes()
        self.CreateGrid()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ###################################################
        ###################################################
        self.StartingTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()

        self.GUI_ready_to_be_updated_flag = 1

        self.root.mainloop()  # THIS MUST BE THE LAST LINE IN THE GUI THREAD SETUP BECAUSE IT'S BLOCKING!!!!
        ###################################################
        ###################################################

        #################################################
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ResetMinAndMax_ButtonResponse(self):

        self.ResetMinAndMax()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ResetMinAndMax(self):

        print("ResetMinAndMax event fired!")

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def OnCanvasMouseDownCallbackFunction(self, event):

        self._last_x = event.x
        self._last_y = event.y

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def OnCanvasMouseDragCallbackFunction(self, event):

        dx = event.x - self._last_x
        dy = event.y - self._last_y
        self._last_x = event.x
        self._last_y = event.y

        self.yaw   += dx * 0.01
        self.pitch += dy * 0.01
        self.pitch = max(-1.4, min(1.4, self.pitch))

        qy = self.Quaterionion_FromAxisAngleRepresentation((0, 1, 0), self.yaw)
        qx = self.Quaterionion_FromAxisAngleRepresentation((1, 0, 0), self.pitch)

        ########################################################################################################## THIS LINES FEEDS DIRECTLY INTO THE SHADRER TO APPLY THE ROTATION QUATERNION
        ##########################################################################################################
        ##########################################################################################################
        self.QuaternionOfView = self.Quaternion_Normalize(self.Quaternion_MultiplyViaHamiltonProduct(qy, qx))
        self.QuaternionOfView_uniform.value = self.QuaternionOfView
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def OnCanvasMouseWheelCallbackFunction(self, event):

        self.dist -= event.delta * 0.005
        self.dist = max(1.5, min(10.0, self.dist))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CreateAxes(self):

        AX = 1.8  # axis half-length matching model normalization

        axis_data = numpy.array([
            # X axis (red)
            0, 0, 0, 1, 0, 0,
            AX, 0, 0, 1, 0, 0,

            # Y axis (green)
            0, 0, 0, 0, 1, 0,
            0, AX, 0, 0, 1, 0,

            # Z axis (blue)
            0, 0, 0, 0, 0, 1,
            0, 0, AX, 0, 0, 1,
        ], dtype="f4")

        self.ModernGL_VertexBufferObject_VBO_Axes = self.ModernGL_Context.buffer(axis_data.tobytes())
        self.ModernGL_VertexArrayObject_VAO_Axes = self.ModernGL_Context.vertex_array(self.ModernGL_Program_Axes, [(self.ModernGL_VertexBufferObject_VBO_Axes, "3f4 3f4", "in_pos", "in_color")])

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CreateGrid(self):
        grid_data = []
        color = [0.3, 0.3, 0.3]  # Dark gray

        for i in range(-5, 6): #Grid from -5 to 5

            # X parallel lines
            grid_data.extend([-5, i, 0] + color)
            grid_data.extend([5, i, 0] + color)

            # Y parallel lines
            grid_data.extend([i, -5, 0] + color)
            grid_data.extend([i, 5, 0] + color)
            
        grid_data = numpy.array(grid_data, dtype='f4')
        
        self.ModernGL_VertexBufferObject_VBO_grid = self.ModernGL_Context.buffer(grid_data.tobytes())
        self.ModernGL_VertexArrayObject_VAO_grid = self.ModernGL_Context.vertex_array(self.ModernGL_Program_Axes, [(self.ModernGL_VertexBufferObject_VBO_grid, "3f4 3f4", "in_pos", "in_color")])

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## Def GUI
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __GUI_update_clock(self):  # THIS FUNCTION NEEDS TO BE CALLED INTERNALLY BY THE CLASS, NOT EXTERNALLY LIKE WE NORMALLY DO BECAUSE WE'RE FIRING THESE ROOT.AFTER CALLBACKS FASTER THAN THE PARENT ROOT GUI

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            if self.EXIT_PROGRAM_FLAG == 0:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.GUI_ready_to_be_updated_flag == 1:

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromGUIthread
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    if self.RootGeometryHasBeenModifiedFlag == 1:

                        self.RootConfigurationUpdate()

                        if self.RootGeometryHasBeenModified_HasThisEventFiredBeforeFlag == 1:
                            pass

                        self.RootGeometryHasBeenModified_HasThisEventFiredBeforeFlag = 1
                        self.RootGeometryHasBeenModifiedFlag = 0
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ########################################################################################################## unicorn
                    ##########################################################################################################
                    ##########################################################################################################
                    self.SetModelQuaternion(self.Quaternion)

                    self.ModernGL_FrameBufferObject_FBO.use()
                    self.ModernGL_Context.clear(0.1, 0.1, 0.1, 1.0)  # clears color + depth

                    ProjectionMatrix_data = self.CalculateProjectionMatrix().flatten().tolist()
                    ViewMatrix_data = self.CalculateViewMatrix().flatten().tolist()

                    self.ProjectionMatrix_uniform.value = ProjectionMatrix_data
                    self.ViewMatrix_uniform.value = ViewMatrix_data

                    self.Axes_ProjectionMatrix_uniform.value = ProjectionMatrix_data
                    self.Axes_ViewMatrix_uniform.value = ViewMatrix_data
                    self.Axes_QuaternionOfView_uniform.value = self.QuaternionOfView

                    self.ModernGL_Context.disable(moderngl.DEPTH_TEST) #disable depth testing only for the axes
                    self.ModernGL_VertexArrayObject_VAO_grid.render(mode=moderngl.LINES)
                    self.ModernGL_VertexArrayObject_VAO_Axes.render(mode=moderngl.LINES)
                    self.ModernGL_Context.enable(moderngl.DEPTH_TEST)

                    self.ModernGL_VertexArrayObject_VAO.render()

                    data = self.ModernGL_FrameBufferObject_FBO.read(components=3)
                    img = Image.frombytes("RGB", (self.GraphCanvasWidth, self.GraphCanvasHeight), data)
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)

                    self._photo = ImageTk.PhotoImage(img)

                    if self._canvas_image_id is None:
                        self._canvas_image_id = self.CanvasForDrawingGraph.create_image(0, 0, anchor="nw", image=self._photo)
                    else:
                        self.CanvasForDrawingGraph.itemconfig(self._canvas_image_id, image=self._photo)

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    self.Debug_Label["text"] = "P.PID = " + str(self.ParentPID) + \
                                                ", SelfPID = " + str(self.SelfPID) + \
                                                ", Time: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromGUIthread, 0, 1) + \
                                                ", Freq: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.LoopFrequency_CalculatedFromGUIthread, 2, 3) + \
                                                ", CPU %: " + str(self.MemoryUsageOfProcessByPID_Dict["CPUusage_Percent"]) + \
                                                ", MEM %: " + str(self.MemoryUsageOfProcessByPID_Dict["MemoryUsage_Percent"]) + \
                                                ", #: " + str(len(self.CanvasForDrawingGraph.find_all())) + \
                                                ", Watchdog: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.TimeIntoWatchdogTimer, 0, 3) + \
                                                ", Quaternion: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Quaternion, 0, 3) +\
                                                "\nUDP: "
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    try:
                        if self.UDPdataExchanger_OPEN_FLAG == 1 and self.SHOW_IN_GUI_UDPdataExchanger_FLAG == 1:
                            self.UDPdataExchanger_Object.GUI_update_clock()
                    except:
                        exceptions = sys.exc_info()[0]
                        print("__GUI_update_clock, exceptions: %s" % exceptions)
                        traceback.print_exc()
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    self.UpdateFrequencyCalculation_CalculatedFromGUIthread()
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents, self.__GUI_update_clock)
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("__GUI_update_clock, exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            # input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0))  # Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string)  # Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
