import ctypes
import time

# SendInput = ctypes.windll.user32.SendInput

class Point(ctypes.Structure):
    _fields_=[("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

def currentCursorPosition():
    point = Point()
    ctypes.windll.user32.GetCursorPos(ctypes.pointer(point))
    return (point.x, point.y)

def nextCursorPosition(meanGradient, screenWidth):
    currentX, currentY = currentCursorPosition()
    (x - currentX) / screenWidth
    return (x, currentY)


W = 0x11
S = 0x1F

def click(meanGradient, screenWidth):
    x, y = nextCursorPosition(meanGradient)
    ctypes.windll.user32.SetCursorPos(x, y)
    # left mouse down, https://msdn.microsoft.com/en-us/library/windows/desktop/ms646260(v=vs.85).aspx
    ctypes.windll.user32.mouse_event(2, x, y, 0, 0)
    # left mouse up
    ctypes.windll.user32.mouse_event(4, x, y, 0, 0)

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def main():
    startTime = time.time()
    while (time.time() - startTime < 20):
        PressKey(W)
        time.sleep(2)
        ReleaseKey(W)
        ctypes.windll.user32.SetCursorPos(320, 240)
        ctypes.windll.user32.mouse_event(1, -300,0, 0, 0)
        time.sleep(2)
        print(currentCursorPosition())
        ctypes.windll.user32.mouse_event(1, 600,0, 0, 0)
        time.sleep(2)
        print(currentCursorPosition())
        # # left mouse down, https://msdn.microsoft.com/en-us/library/windows/desktop/ms646260(v=vs.85).aspx
        # ctypes.windll.user32.mouse_event(2, 200, 200, 0, 0)
        # # left mouse up
        # ctypes.windll.user32.mouse_event(4, 200, 200, 0, 0)

time.sleep(8)
main()
