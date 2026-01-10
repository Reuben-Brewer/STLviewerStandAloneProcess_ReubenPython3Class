# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 01/09/2026

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

#########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
#########################################################

#########################################################
from STLviewerStandAloneProcess_ReubenPython3Class import *
from UDPdataExchanger_ReubenPython3Class import *
#########################################################

#########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import math
import traceback
import re
import keyboard
import signal #for CTRLc_HandlerFunction
import numpy
from scipy.spatial.transform import Rotation as R
#########################################################

#########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

##########################################################################################################
##########################################################################################################

########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
##########################################################################################################
def CTRLc_RegisterHandlerFunction():

    CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
    #print("CurrentHandlerRegisteredForSIGINT: " + str(CurrentHandlerRegisteredForSIGINT))

    defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

    if CurrentHandlerRegisteredForSIGINT in defaultish: # Only install if it's default/ignored (i.e., nobody set it yet)
        signal.signal(signal.SIGINT, CTRLc_HandlerFunction)
        print("test_program_for_STLviewerStandAloneProcess_ReubenPython3Class.py, CTRLc_RegisterHandlerFunction event fired!")

    else:
        print("test_program_for_STLviewerStandAloneProcess_ReubenPython3Class.py, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
##########################################################################################################
##########################################################################################################

########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
##########################################################################################################
def CTRLc_HandlerFunction(signum, frame):

    print("CTRLc_HandlerFunction event firing!")

    ExitProgram_Callback()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def quat_from_axis_angle_deg(axis, angle_degrees):
    axis = numpy.array(axis, dtype=float)
    axis = axis / numpy.linalg.norm(axis)

    angle = numpy.deg2rad(angle_degrees)     # convert to radians
    half = angle / 2.0

    w = numpy.cos(half)
    s = numpy.sin(half)

    x, y, z = axis * s

    return [w, x, y, z]
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]

            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0

                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % PeriodicInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue

                A = abs(MaxValue - MinValue)
                P = Period

                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":

                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)

                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            return -11111.0
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
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ResetMinAndMax_ButtonResponse():
    global ResetMinAndMax_EventNeedsToBeFiredFlag
    
    ResetMinAndMax_EventNeedsToBeFiredFlag = 1

    #print("ResetMinAndMax_ButtonResponse event fired!")

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global STLviewerStandAloneProcess_Object
    global USE_STLviewerStandAloneProcess_FLAG
    global STLviewerStandAloneProcess_OPEN_FLAG
    global SHOW_IN_GUI_STLviewerStandAloneProcess_FLAG

    global UDPdataExchanger_Object
    global UDPdataExchanger_OPEN_FLAG
    global SHOW_IN_GUI_UDPdataExchanger_FLAG
    global UDPdataExchanger_MostRecentDict
    global UDPdataExchanger_MostRecentDict_Label

    if USE_GUI_FLAG == 1:

        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if UDPdataExchanger_OPEN_FLAG == 1 and SHOW_IN_GUI_UDPdataExchanger_FLAG == 1:
                UDPdataExchanger_Object.GUI_update_clock()
            #########################################################

            #########################################################
            #if USE_STLviewerStandAloneProcess_FLAG == 1 and STLviewerStandAloneProcess_OPEN_FLAG == 1 and SHOW_IN_GUI_STLviewerStandAloneProcess_FLAG == 1:
                #pass #DO NOT CALL STLviewerStandAloneProcess_Object.GUI_update_clock() as the plotter is firing its own, internal root.after callbacks faster than in this parent root GUI loop.
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
            #########################################################

        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("Exiting all threads in test_program_for_STLviewerStandAloneProcess_ReubenPython3Class.")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds

    global UDPdataExchanger_Object
    global UDPdataExchanger_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    #################################################
    #################################################

    #################################################
    #################################################
    AllButtonsGuiFrame = Frame(root)
    AllButtonsGuiFrame.grid(row=0, column=0, padx=1, pady=1, rowspan=1, columnspan=1, sticky='w')
    #################################################
    #################################################

    #################################################
    #################################################
    ResetMinAndMax_Button = Button(AllButtonsGuiFrame, text='ResetMinAndMax', state="normal", width=20, font=("Helvetica", 8), command=lambda i=1: ResetMinAndMax_ButtonResponse())
    ResetMinAndMax_Button.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    if UDPdataExchanger_OPEN_FLAG == 1:
        UDPdataExchanger_Object.CreateGUIobjects(TkinterParent=AllButtonsGuiFrame)
    #################################################
    #################################################

    #################################################
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0
    #################################################
    #################################################

    #################################################
    #################################################
    CTRLc_RegisterHandlerFunction()
    #################################################
    #################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_STLviewerStandAloneProcess_FLAG
    USE_STLviewerStandAloneProcess_FLAG = 1

    global USE_UDPdataExchanger_FLAG
    USE_UDPdataExchanger_FLAG = 1

    global TEST_WATCHDOG_FLAG
    TEST_WATCHDOG_FLAG = 0

    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_STLviewerStandAloneProcess_FLAG
    SHOW_IN_GUI_STLviewerStandAloneProcess_FLAG = 1

    global SHOW_IN_GUI_UDPdataExchanger_FLAG
    SHOW_IN_GUI_UDPdataExchanger_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_UDPdataExchanger
    global GUI_COLUMN_UDPdataExchanger
    global GUI_PADX_UDPdataExchanger
    global GUI_PADY_UDPdataExchanger
    global GUI_ROWSPAN_UDPdataExchanger
    global GUI_COLUMNSPAN_UDPdataExchanger
    GUI_ROW_UDPdataExchanger = 1

    GUI_COLUMN_UDPdataExchanger = 0
    GUI_PADX_UDPdataExchanger = 1
    GUI_PADY_UDPdataExchanger = 1
    GUI_ROWSPAN_UDPdataExchanger = 1
    GUI_COLUMNSPAN_UDPdataExchanger = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global root

    global root_Xpos
    root_Xpos = 0

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1820

    global root_height
    root_height = 400

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    
    global CurrentTime_CalculatedFromMainThread
    CurrentTime_CalculatedFromMainThread = -11111.0

    global StartingTime_CalculatedFromMainThread
    StartingTime_CalculatedFromMainThread = -11111.0

    global LoopCounter_CalculatedFromMainThread
    LoopCounter_CalculatedFromMainThread = 0

    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["GUI", "Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput_Type_1
    PeriodicInput_Type_1 = "Sine"

    global PeriodicInput_MinValue_1
    PeriodicInput_MinValue_1 = 0.0

    global PeriodicInput_MaxValue_1
    PeriodicInput_MaxValue_1 = 90.0

    global PeriodicInput_Period_1
    PeriodicInput_Period_1 = 5.0

    global PeriodicInput_CalculatedValue_1
    PeriodicInput_CalculatedValue_1 = 0.0

    global ResetMinAndMax_EventNeedsToBeFiredFlag
    ResetMinAndMax_EventNeedsToBeFiredFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global STLviewerStandAloneProcess_Object

    global STLviewerStandAloneProcess_OPEN_FLAG
    STLviewerStandAloneProcess_OPEN_FLAG = -1

    global STLviewerStandAloneProcess_MostRecentDict
    STLviewerStandAloneProcess_MostRecentDict = dict()

    global STLviewerStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    STLviewerStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_CalculatedFromMainThread_STLviewerStandAloneProcess
    LastTime_CalculatedFromMainThread_STLviewerStandAloneProcess = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global UDPdataExchanger_Object

    global UDPdataExchanger_OPEN_FLAG
    UDPdataExchanger_OPEN_FLAG = 0

    global UDPdataExchanger_MostRecentDict
    UDPdataExchanger_MostRecentDict = dict()

    global UDPdataExchanger___UDP_RxOrTxRole
    UDPdataExchanger___UDP_RxOrTxRole = "tx"

    global UDPdataExchanger___IPV4_address
    UDPdataExchanger___IPV4_address = "127.0.0.10"

    global UDPdataExchanger___IPV4_Port
    UDPdataExchanger___IPV4_Port = 7

    global UDPdataExchanger___UDP_BufferSizeInBytes
    UDPdataExchanger___UDP_BufferSizeInBytes = 100

    global UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds #FOR INDIVIDUAL BYTES ON THE UDP PORT, NOT FOR ENTIRE MESSAGES (LIKE THE WATCHDOG)
    UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds = 0.1

    global UDPdataExchanger___WatchdogTimerExpirationDurationSeconds
    UDPdataExchanger___WatchdogTimerExpirationDurationSeconds = 3.0
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global STLviewerStandAloneProcess_GUIparametersDict
    STLviewerStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                        ("NumberOfPrintLines", 10),
                                                        ("GraphCanvasWidth", 1280),
                                                        ("GraphCanvasHeight", 700),
                                                        ("GraphCanvasWindowStartingX", 0),
                                                        ("GraphCanvasWindowStartingY", 410),
                                                        ("GraphCanvasWindowTitle", "My plotting example!"),
                                                        ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])

    global STLviewerStandAloneProcess_SetupDict
    STLviewerStandAloneProcess_SetupDict = dict([("GUIparametersDict", STLviewerStandAloneProcess_GUIparametersDict),
                                                ("STLfileFullPath", "teapot.stl"), #teapot, bunny, cube
                                                ("ParentPID", os.getpid()),
                                                ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", 5.0),
                                                ("UDPdataExchanger___IPV4_address", UDPdataExchanger___IPV4_address),
                                                ("UDPdataExchanger___IPV4_Port", UDPdataExchanger___IPV4_Port),
                                                ("UDPdataExchanger___UDP_BufferSizeInBytes", UDPdataExchanger___UDP_BufferSizeInBytes),
                                                ("UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds", UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds), #FOR INDIVIDUAL BYTES ON THE UDP PORT, NOT FOR ENTIRE MESSAGES (LIKE THE WATCHDOG)
                                                ("UDPdataExchanger___WatchdogTimerExpirationDurationSeconds", UDPdataExchanger___WatchdogTimerExpirationDurationSeconds),
                                                ("UDPdataExchanger___MainThread_TimeToSleepEachLoop", 0.030),])
    
    if USE_STLviewerStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            STLviewerStandAloneProcess_Object = STLviewerStandAloneProcess_ReubenPython3Class(STLviewerStandAloneProcess_SetupDict)
            STLviewerStandAloneProcess_OPEN_FLAG = STLviewerStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG
            
        except:
            exceptions = sys.exc_info()[0]
            print("STLviewerStandAloneProcess_Object, exceptions: %s" % exceptions)
            #traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_STLviewerStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if STLviewerStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open STLviewerStandAloneProcess_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global UDPdataExchanger_GUIparametersDict
    UDPdataExchanger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_UDPdataExchanger_FLAG),
                                                ("EnableInternal_MyPrint_Flag", 0),
                                                ("NumberOfPrintLines", 10),
                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                ("GUI_ROW", GUI_ROW_UDPdataExchanger),
                                                ("GUI_COLUMN", GUI_COLUMN_UDPdataExchanger),
                                                ("GUI_PADX", GUI_PADX_UDPdataExchanger),
                                                ("GUI_PADY", GUI_PADY_UDPdataExchanger),
                                                ("GUI_ROWSPAN", GUI_ROWSPAN_UDPdataExchanger),
                                                ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_UDPdataExchanger)])

    global UDPdataExchanger_SetupDict
    UDPdataExchanger_SetupDict = dict([("GUIparametersDict", UDPdataExchanger_GUIparametersDict),
                                        ("NameToDisplay_UserSet", "UDPdataExchanger"),
                                        ("UDP_RxOrTxRole", "tx"),
                                        ("IPV4_address", UDPdataExchanger___IPV4_address),
                                        ("IPV4_Port", UDPdataExchanger___IPV4_Port),
                                        ("UDP_BufferSizeInBytes", UDPdataExchanger___UDP_BufferSizeInBytes),
                                        ("UDP_TimeoutAtPortLevelInSeconds", UDPdataExchanger___UDP_TimeoutAtPortLevelInSeconds), #FOR INDIVIDUAL BYTES ON THE UDP PORT, NOT FOR ENTIRE MESSAGES (LIKE THE WATCHDOG)
                                        ("WatchdogTimerExpirationDurationSeconds", UDPdataExchanger___WatchdogTimerExpirationDurationSeconds),
                                        ("MainThread_TimeToSleepEachLoop", 0.030)])

    if USE_UDPdataExchanger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            UDPdataExchanger_Object = UDPdataExchanger_ReubenPython3Class(UDPdataExchanger_SetupDict)
            UDPdataExchanger_OPEN_FLAG = UDPdataExchanger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("UDPdataExchanger_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_UDPdataExchanger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if UDPdataExchanger_OPEN_FLAG != 1:
                print("Failed to open UDPdataExchanger_ReubenPython3ClassObject.")
                #ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################  KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("$$$$$$$$$$$$$$ Starting test_program_for_STLviewerStandAloneProcess_ReubenPython3Class.py $$$$$$$$$$$$$$")
        StartingTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        #################################################
        #################################################
        CurrentTime_CalculatedFromMainThread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromMainThread
        LoopCounter_CalculatedFromMainThread = LoopCounter_CalculatedFromMainThread + 1

        if CurrentTime_CalculatedFromMainThread > 60.0:
            ExitProgram_Callback()
        #################################################
        #################################################

        #################################################
        #################################################
        PeriodicInput_CalculatedValue_1 = GetLatestWaveformValue(CurrentTime_CalculatedFromMainThread, 
                                                                PeriodicInput_MinValue_1,
                                                                PeriodicInput_MaxValue_1,
                                                                PeriodicInput_Period_1, 
                                                                PeriodicInput_Type_1)
        #################################################
        #################################################

        #################################################
        #################################################
        if STLviewerStandAloneProcess_OPEN_FLAG == 1:

            #################################################
            if ResetMinAndMax_EventNeedsToBeFiredFlag == 1:
                STLviewerStandAloneProcess_Object.SendResetMinAndMaxCommandToStandAloneProcess()
                ResetMinAndMax_EventNeedsToBeFiredFlag = 0
            #################################################

        #################################################
        #################################################
        
        #################################################  SET's
        #################################################
        if STLviewerStandAloneProcess_OPEN_FLAG == 1:

            #################################################
            try:
                STLviewerStandAloneProcess_MostRecentDict = STLviewerStandAloneProcess_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in STLviewerStandAloneProcess_MostRecentDict:
                    STLviewerStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = STLviewerStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if STLviewerStandAloneProcess_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_CalculatedFromMainThread - LastTime_CalculatedFromMainThread_STLviewerStandAloneProcess >= STLviewerStandAloneProcess_GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"]/1000.0 + 0.001:

                            QuaternionToApply = quat_from_axis_angle_deg([0, 0, 1], PeriodicInput_CalculatedValue_1)

                            if UDPdataExchanger_OPEN_FLAG == 1:
                                UDPdataExchanger_Object.SendDictFromExternalProgram(dict([("Time", CurrentTime_CalculatedFromMainThread), ("Quaternion", QuaternionToApply)]))
                            else:
                                STLviewerStandAloneProcess_Object.ExternalUpdateRotationQuaternion(QuaternionToApply)

                            LastTime_CalculatedFromMainThread_STLviewerStandAloneProcess = CurrentTime_CalculatedFromMainThread
            #################################################

            #################################################
            except:
                exceptions = sys.exc_info()[0]
                print("STLviewerStandAloneProcess, exceptions: %s" % exceptions)
                traceback.print_exc()
            #################################################

        #################################################
        #################################################

        time.sleep(0.030)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("$$$$$$$$$$$$$$ Ending test_program_for_STLviewerStandAloneProcess_ReubenPython3Class.py $$$$$$$$$$$$$$")

    #################################################
    #################################################
    if UDPdataExchanger_OPEN_FLAG == 1:
        UDPdataExchanger_Object.ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if STLviewerStandAloneProcess_OPEN_FLAG == 1:

        if TEST_WATCHDOG_FLAG == 0:
            STLviewerStandAloneProcess_Object.ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
