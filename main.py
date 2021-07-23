import cv2 as cv
import numpy as np
import win32gui, win32api, win32con, win32ui
import os
import pygame
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class GameWindow:
    def __init__(self, windowClass):
        self.hwnd = win32gui.FindWindow(windowClass, None)
        self.updateSelfBounds()
    
    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.bounds['w'], self.bounds['h'])
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.bounds['w'], self.bounds['h']) , dcObj, (0,0), win32con.SRCCOPY)
        # dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.bounds['h'], self.bounds['w'], 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img

    def updateSelfBounds(self):
        self.rect = win32gui.GetWindowRect(self.hwnd) # (0, 0, 1920, 1080)
        
        self.bounds = {
            'x': self.rect[0],
            'y': self.rect[1]
        } 
        self.bounds['w'] = self.rect[2] - self.bounds['x']
        self.bounds['h'] = self.rect[3] - self.bounds['y']

class OverlayWindow: 
    def __init__(self, x, y, w, h) -> None:
        self.bounds = {
            'x': x,
            'y': y,
            'w': w,
            'h': h,
        }
        self.screen = pygame.display.set_mode(size=(w, h), depth=1, flags=pygame.NOFRAME )
        # | pygame.FULLSCREEN
        self.pink = (255, 192, 203)  # Transparency color
        # Set window transparency color
        self.hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.hwnd, win32api.RGB(*self.pink), 0, win32con.LWA_COLORKEY)
        # Variables
        self.icons = {
            'bleed': {
                'status': False,
                'img': pygame.image.load("display_icon_bleed.png"),
                'x_offset': 4,
                'y_offset': 0
            },
            'freeze': {
                'status': False,
                'img': pygame.image.load("display_icon_freeze.png"),
                'x_offset': -40,
                'y_offset': 0
            },
            'ignite': {
                'status': False,
                'img': pygame.image.load("display_icon_ignite.png"),
                'x_offset': -64,
                'y_offset': 0
            },
            'poison': {
                'status': False,
                'img': pygame.image.load("display_icon_poison.png"),
                'x_offset': 32,
                'y_offset': 0
            },
            'shock': {
                'status': False,
                'img': pygame.image.load("display_icon_shock.png"),
                'x_offset': -16,
                'y_offset': 0
            },
        }

    def draw(self):
        self.screen.fill(self.pink)  # Transparent background
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, self.bounds['x'], self.bounds['y'], self.bounds['w'], self.bounds['h'], win32con.SWP_NOSIZE)
        
        x = 960
        y = 360

        for icon in self.icons:
            curr = self.icons[icon]
            if( self.icons[icon]['status']):
                self.screen.blit(curr['img'], (x + curr['x_offset'], y + curr['y_offset']))
        
        pygame.display.update()

    def resetIconStatus(self):
        for icon in self.icons:
            self.icons[icon]['status'] = False

    def updateBounds(self, x, y, w, h):
        self.bounds['x'] = x
        self.bounds['y'] = y
        self.bounds['w'] = w
        self.bounds['h'] = h

class BuffMatcher:
    def __init__(self) -> None:
        self.detector = cv.SIFT_create()
        self.matcher = cv.BFMatcher()

class BuffIcon: 
     def __init__(self, name, path_str, buff_matcher) -> None:
         self.name = name
         self.path = path_str
         self.img = cv.imread(path_str, cv.IMREAD_UNCHANGED)
        #  self.img = scale_img(self.img, 50)
         self.key_points, self.description = buff_matcher.detector.detectAndCompute(self.img,None) 
         pass

def scale_img(img, scale_percent = 50):
    # scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    #   resize image
    resized = cv.resize(img, dim, interpolation = cv.INTER_AREA)
    return resized

gameWindow = GameWindow("POEWindowClass")
overlay = OverlayWindow(gameWindow.bounds['x'], gameWindow.bounds['y'], gameWindow.bounds['w'], gameWindow.bounds['h'])
buff_matcher = BuffMatcher()

# Load all debuffs images
debuffs = [
    BuffIcon('bleed', "status_icon_bleed.png", buff_matcher),
    BuffIcon('freeze', "status_icon_freeze.png", buff_matcher),
    BuffIcon('ignite', "status_icon_ignite.png", buff_matcher),
    BuffIcon('poison', "status_icon_poison.png", buff_matcher),
    BuffIcon('shock', "status_icon_shock.png", buff_matcher),
    # BuffIcon('sand', "status_icon_sand_stance.png", buff_matcher),
]

gaming = True
target_fps = 10
frameperiod=1.0/target_fps
last_time=time.time()

while gaming:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gaming = False

    gameWindow.updateSelfBounds()
    
    # capture image and convert to opencv
    screenshot_orig = gameWindow.get_screenshot()
    scale_amt = round(((gameWindow.bounds['w'] / (1920.0)) * 100)/2.0)

    screenshot = scale_img(screenshot_orig, scale_amt)
    # screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)

    # find the keypoints and descriptors with SIFT
    kp2, des2 = buff_matcher.detector.detectAndCompute(screenshot,None)
    
    # reset icon status to false until we find it this frame
    overlay.resetIconStatus()

    # check all debuffs and update their status in the overlay
    for buff in debuffs:
        matches = buff_matcher.matcher.knnMatch(buff.description,des2,k=2)
        # Apply ratio test
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append([m])
        
        good_amt = len(good)

        print(f'matches: {good_amt} of {len(buff.key_points)}')
        
        if(good_amt >= 4):
            if buff.name == 'sand': # the debug aura
                for icon in overlay.icons: 
                    overlay.icons[icon]['status'] = True
            else:
                overlay.icons[buff.name]['status'] = True

    # resize overlay to match window and draw
    overlay.updateBounds(**gameWindow.bounds)
    overlay.draw()

    # Frame stuff
    now = time.time()
    nextframe=last_time+frameperiod
    while(now<nextframe):
        time.sleep(nextframe-now)
        now = time.time()
    frame_time = now-last_time 
    # print(frame_time)
    print(1/frame_time)
    last_time = now