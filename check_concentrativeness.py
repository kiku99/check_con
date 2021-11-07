import sys
from PyQt5.QtWidgets import QApplication, QLCDNumber, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import cv2
import threading
from PyQt5.QtCore import Qt

#global dictionary of dynamically changing widgets
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "cam": [],
    "timer": [],
    "answer1": [],
}

running = False
# Face Detector 위한 것
model = 'D:/const2/res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'D:/const2/deploy.prototxt'
net = cv2.dnn.readNet(model, config)
if net.empty():
    print('Net open failed!')
    sys.exit()



def run():
    global running

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Camera open failed!')
        sys.exit()
    width = int(cap.get(3))  # 가로 길이 가져오기
    height = int(cap.get(4))  # 세로 길이 가져오기
    width_2 = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_2 = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcc = cv2.VideoWriter_fourcc(*'DIVX')  # *'DIVX' == 'D', 'I', 'V', 'X'
    out_2 = cv2.VideoWriter('D:/const2/data/video', fcc, fps, (width_2, height_2))

    cnt = 1
    cam.resize(int(width), int(height))

    while running:
        ret, img = cap.read()
        if not ret:
            break

        ## Face Detect
        blob = cv2.dnn.blobFromImage(img, 1, (300, 300), (104, 177, 123))
        net.setInput(blob)
        out = net.forward()
        out_2.write(img)
        detect = out[0, 0, :, :]
        (h, w) = img.shape[:2]

        for i in range(detect.shape[0]):
            confidence = detect[i, 2]
            if confidence < 0.5:
                break

            x1 = int(detect[i, 3] * w)
            y1 = int(detect[i, 4] * h)
            x2 = int(detect[i, 5] * w)
            y2 = int(detect[i, 6] * h)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0))

            label = f'Face: {confidence:4.2f}'
            cv2.putText(img, label, (x1, y1 - 1),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        
        ##
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c,
                                QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qImg)
        cam.setPixmap(pixmap)
        t, _ = net.getPerfProfile()
        if (t * 1000.0 / cv2.getTickFrequency()) % 10000 > 10:
            cv2.imwrite('D:/const2/data/screenshot{}.png'.format(cnt), img,
                        params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
            cnt += 1

    cap.release()
    out_2.release()
    print("Thread end.")
    onExit()
    


def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")


def stop():
    global running
    running = False
    print("stoped..")


def onExit():
    print("exit")
    stop()


#initiallize GUI application
app = QApplication(sys.argv)

#window and settings
window = QWidget()
window.setWindowTitle("checking const")
window.setFixedWidth(1000)
window.setFixedHeight(800)
window.move(300, 100)
window.setStyleSheet("background: #9999FF;")

#initialliza grid layout
grid = QGridLayout()


def clear_widgets():
    ''' hide all existing widgets and erase
        them from the global dictionary'''
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def show_frame1():
    '''display frame 1'''
    clear_widgets()
    frame1()


def start_game():
    '''display frame 2'''
    clear_widgets()
    frame2()


def create_buttons(answer, l_margin, r_margin):
    '''create identical buttons with custom left & right margins'''

    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        #setting variable margins
        "*{margin-left: " + str(l_margin) + "px;" +
        "margin-right: " + str(r_margin) + "px;" +
        '''
        border: 4px solid '#BC006C';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px}
        *:hover{
            background: '#BC006C'
        }
        '''
    )
    button.clicked.connect(show_frame1)
    button.clicked.connect(stop)
    return button


def frame1():
    #logo widget
    image = QPixmap("D:\const2\image\logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px; ")
    widgets["logo"].append(logo)

    #button widget
    button = QPushButton("측정시작")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#330066';
            border-radius: 45px;
            font-size: 35px;
            color: 'white';
            padding: 25px 0;
            margin: 100px 200px;
        }
        *:hover{
            background: '#330066';
        }
        '''
    )
    #button callback
    button.clicked.connect(start_game)
    button.clicked.connect(start)

    widgets["button"].append(button)

    #place global widgets on the grid
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


def frame2():
    #score widget
    score = QLabel("80")
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        '''
        font-size: 40px;
        color: 'white';
        padding: 15px 10px;
        margin: 55px 200px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 35px;
        '''
    )
    widgets["score"].append(score)

    #cam widget
    cam.setAlignment(QtCore.Qt.AlignCenter)
    widgets["cam"].append(cam)

    #button widgets
    button1 = create_buttons("progress", 85, 5)

    widgets["answer1"].append(button1)

    #Timer widget
    timer = QtCore.QTimer()
    timer.setInterval(1000)
    timer.start()

    currentTime = QtCore.QTime.currentTime().toString("hh:mm:ss")

    lcd = QLCDNumber()
    lcd.display(currentTime)
    lcd.setDigitCount(8)

    widgets["timer"].append(lcd)

    #place widget on the grid
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["cam"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["timer"][-1], 2, 1)


#display frame 1
frame1()

cam = QLabel()
window.setLayout(grid)
window.show()

sys.exit(app.exec())