#=============================================#
#                                             #
#                 导入所需模块                 #
#                                             #
#=============================================#

import cv2
import time
import random
import datetime
import win32api
import win32gui
import win32con
import numpy as np
from PIL import ImageGrab
from skimage.metrics import structural_similarity

#=============================================#
#                                             #
#                 定义所需常量                 #
#                                             #
#=============================================#

#下面所有的BOX都是[left,up,right,down]形式，且都是相对于窗口界面的（0~1）
#这些数据最好自己调试一下，对于不同分辨率的模拟器，位置变化会很大的


#=================截图比对区域=================#
IMAGE_PATH = 'initial_IMG/'#读取截图的路径
MAIN_MENU_IMAGE_BOX = [0.65,0.50,0.75,0.58]#主界面判断区域                       
L_SUPPORT_IMAGE_BOX = [0.05,0.30,0.18,0.39]#后勤完成界面判断区域                
COMBAT_MENU_IMAGE_BOX = [0.05,0.70,0.12,0.80]#战斗菜单界面判断区域         
CHOOSE_0_2_IMAGE_BOX = [0.50,0.43,0.60,0.50]#0-2界面判断区域                          
MAP_0_2_IMAGE_BOX = [0.82,0.80,0.95,0.88]#0-2地图判断区域                             
PLAN_FINISH_IMAGE_BOX = [0.80,0.82,0.97,0.88]#计划完成判断区域    
COMBAT_START_IMAGE_BOX = [0.80,0.82,0.97,0.88]#开启作战判断区域                              
GOTO_POWERUP_IMAGE_BOX = [0.58,0.60,0.68,0.64]#提醒强化判断区域               
NAVIGATE_IMAGE_BOX = [0.15,0.10,0.20,0.15]#导航条判断区域       
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.35]#模拟器桌面判断区域         
COMBAT_PAUSE_IMAGE_BOX = [0.45,0.62,0.55,0.67]#战斗终止提示判断区域            
RETURN_COMBAT_IMAGE_BOX = [0.75,0.63,0.90,0.70]#回到作战界面判断区域    

#=================点击拖动区域=================#

#从主菜单进入作战选择界面
COMBAT_CLICK_BOX = [0.62,0.52,0.76,0.60]#在主菜单点击战斗

#从作战选择界面进入0-2界面
COMBAT_MISSION_CLICK_BOX = [0.05,0.28,0.10,0.32]#点击作战任务
CHAPTER_DRAG_BOX = [0.16,0.35,0.22,0.40]#向上拖章节选择条
CHAPTER_0_CLICK_BOX = [0.16,0.18,0.22,0.25]#选择第0章
NORMAL_CLICK_BOX = [0.74,0.24,0.77,0.28]#选择普通难度
EPISODE_DRAG_BOX = [0.40,0.35,0.80,0.40]#向上拖小节选择条

#开始/终止0-2
EPISODE_2_CLICK_BOX = [0.50,0.43,0.60,0.50]#选择第2节
ENTER_COMBAT_CLICK_BOX = [0.72,0.70,0.80,0.75]#进入作战
END_COMBAT_STEP1_CLICK_BOX = [0.72,0.62,0.80,0.66]#终止作战
END_COMBAT_STEP2_CLICK_BOX = [0.52,0.60,0.60,0.65]#确认终止作战

#地图缩放、拖动区
MAP_SCALE_BOX = [0.20,0.20,0.30,0.25]
MAP_DRAG_BOX =[0.20,0.20,0.30,0.25]

#队伍放置点
AIRPORT_CLICK_BOX = [0.34,0.82,0.36,0.83]#机场
COMMAND_CLICK_BOX = [0.50,0.82,0.52,0.85]#指挥部

#更换打手
CHANGE_FORCE_STEP1_CLICK_BOX = [0.17,0.74,0.26,0.77]#点击梯队编成
CHANGE_FORCE_STEP2_CLICK_BOX = [0.15,0.35,0.25,0.55]#点击1队打手
CHANGE_FORCE_STEP3_CLICK_BOX = [0.20,0.25,0.25,0.40]#更换打手
CHANGE_FORCE_STEP4_CLICK_BOX = [0.08,0.10,0.10,0.14]#点击返回

#放置队伍
TEAM_SET_CLICK_BOX = [0.85,0.75,0.92,0.78]

#撤退1队
WITHDRAW_STEP1_CLICK_BOX = [0.72,0.76,0.78,0.78]#点击撤退
WITHDRAW_STEP2_CLICK_BOX = [0.55,0.61,0.62,0.64]#确认撤退

#重启作战
RESTART_STEP1_CLICK_BOX = [0.22,0.09,0.26,0.14]#点击终止作战
RESTART_STEP2_CLICK_BOX = [0.34,0.61,0.43,0.63]#点击重新作战

#16哥修复
M16_REPAIR_INTERVAL = 6   #16哥隔多少轮修一次
REPAIR_STEP1_CLICK_BOX = [0.70,0.30,0.76,0.50]#点击m16        
REPAIR_STEP2_CLICK_BOX = [0.69,0.65,0.75,0.69]#确定修复          
REPAIR_STEP3_CLICK_BOX = [0.85,0.75,0.91,0.79]#退出2队界面         

#开始作战
START_COMBAT_CLICK_BOX = [0.85,0.82,0.92,0.86]#点击开始作战

#补给打手
SUPPLY_STEP1_CLICK_BOX = [0.85,0.68,0.94,0.70]#点击补给
SUPPLY_STEP2_CLICK_BOX = [0.20,0.20,0.30,0.25]#取消选中

#计划模式
PLAN_MODE_CLICK_BOX = [0.04,0.77,0.10,0.79]#点击计划模式
PLAN_POINT1_CLICK_BOX = [0.45,0.67,0.47,0.69]#点击计划点1 
PLAN_POINT2_CLICK_BOX = [0.45,0.53,0.47,0.54]#点击计划点2
PLAN_POINT3_CLICK_BOX = [0.63,0.54,0.65,0.56]#点击计划点3
PLAN_START_CLICK_BOX = [0.88,0.82,0.98,0.85]#点击执行计划

#在终点点击结束回合
ACTION_END_CLICK_BOX = [0.88,0.82,0.96,0.88] 

#战役结算
COMBAT_END_STEP1_CLICK_BOX = [0.80,0.40,0.90,0.60]#进入人形掉落界面       
COMBAT_END_STEP2_CLICK_BOX = [0.80,0.40,0.90,0.60]#退出人形掉落界面          
COMBAT_END_STEP3_CLICK_BOX = [0.80,0.40,0.90,0.60]#退出战役结算界面          

#强化（拆解）
GOTO_POWERUP_CLICK_BOX = [0.58,0.60,0.68,0.64]#前往强化界面
CHOOSE_RETIRE_CLICK_BOX = [0.06,0.46,0.12,0.50]#选择回收拆解选项
CHOOSE_CHARACTER_CLICK_BOX = [0.25,0.26,0.3,0.33]#选择拆解人形
CHARACTER_1_CLICK_BOX = [0.12,0.3,0.14,0.36]#第一行第一只人形 
CHARACTER_2_CLICK_BOX = [0.24,0.3,0.26,0.36]#第一行第二只人形 
CHARACTER_3_CLICK_BOX = [0.36,0.3,0.38,0.36]#第一行第三只人形 
CHARACTER_4_CLICK_BOX = [0.48,0.3,0.50,0.36]#第一行第四只人形 
CHARACTER_5_CLICK_BOX = [0.60,0.3,0.62,0.36]#第一行第五只人形 
CHARACTER_6_CLICK_BOX = [0.72,0.3,0.74,0.36]#第一行第六只人形 
RETIRE_DRAG_BOX = [0.40,0.60,0.60,0.60]#往上拖一行
CHOOSE_FINISH_CLICK_BOX = [0.88,0.68,0.92,0.74]#完成选择
RETIRE_CLICK_BOX = [0.84,0.77,0.90,0.80]#点击拆解
CONFIRM_RETIRE_CLICK_BOX = [0.54,0.74,0.64,0.78]#确认拆解高星人形

#跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.15,0.10,0.18,0.15]#打开导航条
NAVIGATE_BAR_DRAG_BOX = [0.10,0.28,0.17,0.32]#向右拖导航条
NAVIGATE_COMBAT_CLICK_BOX = [0.10,0.28,0.12,0.32]#跳转至作战菜单
NAVIGATE_FACTORY_CLICK_BOX = [[0.38,0.28,0.40,0.32]]#跳转至工厂菜单
NAVIGATE_MAIN_MENU_CLICK_BOX = [0.20,0.18,0.28,0.20]#跳转至主菜单

#收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.60,0.62,0.65]#再次派出

#启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击一次
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击开始 

#关闭游戏
CLOSE_GAME_CLICK_BOX = [0.56,0.02,0.57,0.04]

#关闭作战断开提醒
CLOSE_TIP_CLICK_BOX = [0.45,0.62,0.55,0.67]



#=============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
#=============================================#

#一个好程序都应该有一个较为优雅的启动提醒界面？
def preface():    
    for x in range(5,-1,-1):
        mystr =">>> "+str(x)+"s 后将开始操作，请切换至模拟器界面"
        print(mystr,end="")
        print("\b" * (len(mystr)*2),end = "",flush=True)
        time.sleep(1)
    print(">>> 开始操作,现在是",datetime.datetime.now(),"\n")


#随机等待一段时间,控制在minTime~maxTime之间
def wait(minTime,maxTime):
    waitTime = minTime + (maxTime - minTime) * random.random()
    time.sleep(waitTime)


#获取模拟器窗口数据
def getWindowData():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        print("未找到窗口界面,程序自动退出！")
        exit(0)
    elif hwnd != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd)#获取窗口的位置数据
    elif hwnd_desktop != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd_desktop)#获取窗口的位置数据
    width  = right - left
    height = bottom - top
    return [left,top,right,bottom,width,height]


#获取指定区域box的截图
def getImage(box):
    #windowData = [left,top,right,bottom,width,height]        
    windowData = getWindowData()
    imgLeft   = windowData[0] + int(windowData[4] * box[0])
    imgTop    = windowData[1] + int(windowData[5] * box[1])
    imgRight  = windowData[0] + int(windowData[4] * box[2])
    imgBottom = windowData[1] + int(windowData[5] * box[3])
    img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom))
    return img
    
    
#点击box内随机一点，如果提供具体xy偏量，则点击精确的点
def mouseClick(box,minTime,maxTime,exact_x = 0,exact_y = 0):
    #box = [left,top,right,bottom]
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    if exact_x == 0 and exact_y == 0:
        clickX = windowData[0] + (int)(windowData[4] * box[0] + windowData[4] * width  * random.random())
        clickY = windowData[1] + (int)(windowData[5] * box[1] + windowData[5] * height * random.random())
    else:
        clickX = windowData[0] + (int)(windowData[4] * box[0]) + exact_x
        clickY = windowData[1] + (int)(windowData[5] * box[1]) + exact_y
    clickPos = (clickX,clickY)
    win32api.SetCursorPos(clickPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    wait(minTime,maxTime)


#模拟鼠标拖动，box为起始区域,times为拖动次数,distance为单次拖动距离
#dx,dy为组成移动方向向量，frame_interval为鼠标拖动帧间隔,越小鼠标拖动越快
#multi_interval为连续拖动时的时间间隔
def mouseDrag(box,dx,dy,times,distance,frame_interval,multi_interval):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    for i in range(times):
        dragX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width  * random.random())
        dragY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
        dragPos = (dragX, dragY)
        win32api.SetCursorPos(dragPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        for i in range(distance):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,dx,dy,0,0)
            time.sleep(frame_interval)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        time.sleep(multi_interval)


#模拟Ctrl和滚轮实现缩放地图
#direct = 0 : 放大      direct = 1 : 缩小   times为连续缩放次数
def scaleMap(box,direct,times):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    scaleX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width  * random.random())
    scaleY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
    scalePos = (scaleX, scaleY)
    win32api.SetCursorPos(scalePos)
    win32api.keybd_event(0x11,0,0,0)#按下Ctrl键
    for i in range(times):
        if direct == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,1)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-1)
        wait(0.5,0.7)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP,0)    
    time.sleep(1)
        

#比较两图片吻合度，结构相似性比较法（真的好用）
def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
    return score > 0.95


#=============================================#
#                                             #
#                 高级功能函数                 #
#                                             #
#=============================================#
    
#判断是否计划结束
def isPlanFinished():
    initImage = cv2.imread(IMAGE_PATH+"plan_finish.png")
    capImage  = getImage(PLAN_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    #双重判断
    if imageCompare(initImage,capImage):
        time.sleep(5)
        capImage  = getImage(PLAN_FINISH_IMAGE_BOX)
        capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
        if imageCompare(initImage,capImage):
            return True
    return False
         
#判断是否进入了0-2地图
def isInMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_0_2_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是提醒强化界面
def isGotoPowerup():
    initImage = cv2.imread(IMAGE_PATH+"goto_powerup.png")
    capImage  = getImage(GOTO_POWERUP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是可以选择0-2的界面
def is0_2():
    initImage = cv2.imread(IMAGE_PATH+"_0_2.png")
    capImage  = getImage(CHOOSE_0_2_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是战斗选择菜单
def isCombatMenu():
    initImage = cv2.imread(IMAGE_PATH+"combat_menu.png")
    capImage  = getImage(COMBAT_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是主界面
def isMainMenu():
    initImage = cv2.imread(IMAGE_PATH+"main_menu.png")
    capImage  = getImage(MAIN_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
#判断是否是委托完成界面
def isLSupport():
    initImage = cv2.imread(IMAGE_PATH+"L_support.png")
    capImage  = getImage(L_SUPPORT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是模拟器桌面
def isDesktop():
    initImage = cv2.imread(IMAGE_PATH+"desktop.png")
    capImage  = getImage(DESKTOP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是战斗中断提示界面
def isCombatPause():
    initImage = cv2.imread(IMAGE_PATH+"combat_pause.png")
    capImage  = getImage(COMBAT_PAUSE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否有回到作战界面
def isReturnCombat():
    initImage = cv2.imread(IMAGE_PATH+"return_combat.png")
    capImage  = getImage(RETURN_COMBAT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#当不知道在哪时，判断是否有导航栏，有就可以通过导航栏回到作战菜单
def isNavigate():
    initImage = cv2.imread(IMAGE_PATH+"navigate.png")
    capImage  = getImage(NAVIGATE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
  
#从主菜单进入作战菜单
def mainMenuToCombatMenu():
    print("ACTION: 前往作战菜单")
    mouseClick(COMBAT_CLICK_BOX,5,6)  
    
#从作战菜单进入0-2界面
def combatMenuTo0_2():
    print("ACTION: 前往0-2选择界面")
    mouseClick(COMBAT_MISSION_CLICK_BOX,1,2)
    mouseDrag(CHAPTER_DRAG_BOX,0,1,1,400,0.001,1)
    mouseClick(CHAPTER_0_CLICK_BOX,1,2)
    mouseClick(NORMAL_CLICK_BOX,1,2)
    mouseDrag(EPISODE_DRAG_BOX,0,1,1,300,0.001,1)

#开始0-2
def start0_2():
    print("ACTION: 启动0-2")
    mouseClick(EPISODE_2_CLICK_BOX,2,3)
    mouseClick(ENTER_COMBAT_CLICK_BOX,4,5)    

#终止0-2
def end0_2():
    print("ACTION: 终止0-2")
    mouseClick(EPISODE_2_CLICK_BOX,2,3)
    mouseClick(END_COMBAT_STEP1_CLICK_BOX,2,3)  
    mouseClick(END_COMBAT_STEP2_CLICK_BOX,2,3)  

#调整地图
def adjustMap(tiny = False):
    print("STATE：调整地图")
    if tiny:
        scaleMap(MAP_SCALE_BOX,1,1)
        mouseDrag(MAP_DRAG_BOX,0,1,1,400,0.001,1)
    else:
        scaleMap(MAP_SCALE_BOX,1,8)
        mouseDrag(MAP_DRAG_BOX,0,1,2,400,0.001,1)

#战前准备，调整地图，补给1队
def combatPrepare():
    print("STATE: 战前整备")
    adjustMap()
    setTeam()
    startCombat()
    supplyAirport()
    withdraw()
    restartCombat()

#重启作战
def restartCombat():
    print("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX,1,1.5)
    mouseClick(RESTART_STEP2_CLICK_BOX,8,8)

#更换打手
def changeForce():
    print("ACTION: 更换打手")
    mouseClick(AIRPORT_CLICK_BOX,2,3)
    mouseClick(CHANGE_FORCE_STEP1_CLICK_BOX,3,4)
    mouseClick(CHANGE_FORCE_STEP2_CLICK_BOX,3,4)
    mouseClick(CHANGE_FORCE_STEP3_CLICK_BOX,2,3)
    mouseClick(CHANGE_FORCE_STEP4_CLICK_BOX,4,5)

#放置队伍
def setTeam():
    print("ACTION: 放置队伍")
    mouseClick(AIRPORT_CLICK_BOX,2,3)
    mouseClick(TEAM_SET_CLICK_BOX,2,3)
    mouseClick(COMMAND_CLICK_BOX,2,3)
    mouseClick(TEAM_SET_CLICK_BOX,2,3)

#16哥修复
def repairM16():
    print("ACTION: 修复16哥")
    mouseClick(COMMAND_CLICK_BOX,2,3)
    mouseClick(REPAIR_STEP1_CLICK_BOX,1,2)
    mouseClick(REPAIR_STEP2_CLICK_BOX,1,2)
    mouseClick(REPAIR_STEP3_CLICK_BOX,2,3)

#开始作战
def startCombat():
    print("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,4,5)

#补给机场打手
def supplyAirport():
    print("ACTION: 补给机场队")
    mouseClick(AIRPORT_CLICK_BOX,1,1.5)
    mouseClick(AIRPORT_CLICK_BOX,2,3)
    mouseClick(SUPPLY_STEP1_CLICK_BOX,2,3)
    mouseClick(SUPPLY_STEP2_CLICK_BOX,1,1.5)

#撤退休息队
def withdraw():
    print("ACTION: 撤退Zas")
    mouseClick(AIRPORT_CLICK_BOX,1.5,2)
    mouseClick(AIRPORT_CLICK_BOX,1.5,2)
    mouseClick(WITHDRAW_STEP1_CLICK_BOX,2,2)
    mouseClick(WITHDRAW_STEP2_CLICK_BOX,2,2)
    
#计划模式
def planMode():
    print("ACTION: 计划模式")
    mouseClick(COMMAND_CLICK_BOX,0.8,1)
    mouseClick(PLAN_MODE_CLICK_BOX,1,2)
    mouseClick(PLAN_POINT1_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_POINT2_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_POINT3_CLICK_BOX,0.25,0.3)
    mouseClick(PLAN_START_CLICK_BOX,0,0)

#在终点点击结束回合
def endAction():
    print("ACTION: 结束回合")
    mouseClick(ACTION_END_CLICK_BOX,12,14)

#战役结算
def endCombat():
    print("ACTION: 战役结算")
    mouseClick(COMBAT_END_STEP1_CLICK_BOX,6,6)
    mouseClick(COMBAT_END_STEP2_CLICK_BOX,2,3)
    mouseClick(COMBAT_END_STEP3_CLICK_BOX,6,6)

#强化（拆解）
def gotoPowerup():  
    print("ACTION: 拆解人形") 
    mouseClick(GOTO_POWERUP_CLICK_BOX,4,5)
    mouseClick(CHOOSE_RETIRE_CLICK_BOX,1,2)
    mouseClick(CHOOSE_CHARACTER_CLICK_BOX,1,2)
    for i in range(7):
        mouseClick(CHARACTER_1_CLICK_BOX,0.2,0.3)#选六个
        mouseClick(CHARACTER_2_CLICK_BOX,0.2,0.3)
        mouseClick(CHARACTER_3_CLICK_BOX,0.2,0.3)
        mouseClick(CHARACTER_4_CLICK_BOX,0.2,0.3)
        mouseClick(CHARACTER_5_CLICK_BOX,0.2,0.3)
        mouseClick(CHARACTER_6_CLICK_BOX,0.2,0.3)
        mouseDrag(RETIRE_DRAG_BOX,0,-1,1,325,0.005,1)#往上拖一行
    mouseClick(CHOOSE_FINISH_CLICK_BOX,1,2)
    mouseClick(RETIRE_CLICK_BOX,1,2)
    mouseClick(CONFIRM_RETIRE_CLICK_BOX,3,4)    

#跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    print("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,5,6)

#跳转至战斗菜单(暂时不用)
def backToCombatMenu():
    print("ACTION: 跳转至战斗菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_COMBAT_CLICK_BOX,5,6)

#收后勤支援
def takeLSupport():
    print("ACTION: 收派后勤")
    mouseClick(L_SUPPORT_STEP1_CLICK_BOX,2,3)
    mouseClick(L_SUPPORT_STEP2_CLICK_BOX,4,5)

#启动游戏
def startGame():
    print("ACTION: 启动游戏")
    mouseClick(START_GAME_STEP1_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP2_CLICK_BOX,30,30)
    mouseClick(START_GAME_STEP3_CLICK_BOX,30,30)

#关闭作战断开提醒
def closeTip():
    print("ACTION: 关闭作战断开提示")
    mouseClick(CLOSE_TIP_CLICK_BOX,5,5)

#关闭游戏
def closeGame():
    print("ACTION: 关闭游戏")
    mouseClick(CLOSE_GAME_CLICK_BOX,5,5)


#=============================================#
#                                             #
#                 本程序主函数                 #
#                                             #
#=============================================#

if __name__ == "__main__": 

    preface()
    startTime = datetime.datetime.now()
    combatCount = 0
    firstCombat = True
    failCount = 0

    while True:
        if isInMap():
            print("STATE：0-2地图")
            failCount = 0
            if firstCombat:
                firstCombat = False
                combatPrepare()
                continue
            else:
                adjustMap(True)
            changeForce()
            setTeam()
            if combatCount % M16_REPAIR_INTERVAL == 0:
                repairM16()
            startCombat()
            supplyAirport()           
            planMode()
            checkCount = 0
            while (not isPlanFinished()) and checkCount < 300:#计划开始后300s还没打完，一般是出问题了（比方说卡了一下导致流程漏了）
                checkCount += 1
                time.sleep(1)
            if checkCount >= 300:
                print("STATE：战斗超时！")
                closeGame()
                continue
            endAction()
            endCombat()
            combatCount += 1
            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            print('> 已运行：',runtime,'  0-2轮次：',combatCount)                
        elif isGotoPowerup():
            print("STATE： 提醒强化界面")
            gotoPowerup()
            backToMainMenu()
            failCount = 0
        elif is0_2():
            print("STATE： 0-2界面")
            start0_2()
            failCount = 0
        elif isCombatMenu():
            print("STATE： 战斗菜单")
            combatMenuTo0_2()
            failCount = 0
        elif isCombatPause():
            print("STATE： 战斗中断提醒界面")
            failCount = 0
            closeTip()
        elif isReturnCombat():
            print("STATE： 返回作战界面")
            failCount = 0
            mainMenuToCombatMenu()
            combatMenuTo0_2()
            end0_2()
            firstCombat = True
        elif isMainMenu():
            print("STATE： 主菜单界面")
            mainMenuToCombatMenu()
            failCount = 0
        elif isLSupport():
            print("STATE： 后勤结束界面")
            takeLSupport()
            failCount = 0
        elif isDesktop():
            print("STATE：模拟器界面")
            failCount = 0
            firstCombat = True
            startGame()
            continue
        else:#既不是后勤结束界面也不是
            print("WARNING： 当前状态未知!")
            failCount += 1
            if failCount >= 5:  
                print(">>> ",datetime.datetime.now()," 无法确定当前状态,关闭重启！")
                closeGame()
            else:
                time.sleep(5)
                
            
            
