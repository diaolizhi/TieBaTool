import sys
sys.path.append("../")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon

from Control.Controlor import Controlor

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.controlor = Controlor(self)
        self.setWindowTitle("关注贴吧工具")
        self.setWindowIcon(QIcon("xx.jpg"))
        self.setMaximumSize(600, 610)
        self.setMinimumSize(600, 610)
        self.setGeometry(100, 100, 600, 610)
        # stylesheet = open('View/style.qss').read()
        # print(stylesheet)
        # self.setStyleSheet(stylesheet)

        self.lw_my_likes = QListWidget(self)
        self.lw_my_likes.setGeometry(40, 280, 130, 310)

        self.lw_local_list = QListWidget(self)
        self.lw_local_list.setGeometry(230, 280, 130, 310)

        self.Avatar = QLabel(self)
        self.Avatar.setGeometry(QRect(260, 0, 80, 80))
        self.Avatar.setMinimumSize(QSize(80, 80))
        self.Avatar.setMaximumSize(QSize(80, 80))
        self.Avatar.setAutoFillBackground(False)
        self.Avatar.setText("")
        self.Avatar.setPixmap(QPixmap("xx.jpg"))
        self.Avatar.setScaledContents(True)
        self.Avatar.setWordWrap(False)

        self.username = QLabel("未登录", self)
        self.username.setGeometry(260, 100, 80, 12)
        self.username.setAlignment(Qt.AlignCenter)

        self.btn_up_mylike = QPushButton("更新我关注的吧",self)
        self.btn_up_mylike.setDisabled(True)
        self.btn_up_mylike.setGeometry(QRect(40, 230, 130, 40))

        self.btn_get_local_list = QPushButton("更新本地列表", self)
        self.btn_get_local_list.setGeometry(QRect(230, 230, 130, 40))
        self.controlor.get_local_list()

        self.le_bduss = QLineEdit("", self)
        self.le_bduss.setGeometry(QRect(40, 130, 400, 40))
        self.le_bduss.setPlaceholderText("请输入BDUSS")

        self.btn_login = QPushButton("登录",self)
        self.btn_login.setGeometry(QRect(480, 130, 111, 40))

        self.btn_to_like = QPushButton("批量关注贴吧", self)
        self.btn_to_like.setDisabled(True)
        self.btn_to_like.setGeometry(QRect(420, 230, 130, 40))

        self.btn_to_del = QPushButton("批量取关贴吧", self)
        self.btn_to_del.setDisabled(True)
        self.btn_to_del.setGeometry(QRect(420, 280, 130, 40))

        self.te_message = QTextEdit(self)
        self.te_message.setGeometry(QRect(420, 330, 130, 260))
        self.te_message.setText("")

        self.show()
        self.my_events()

    def my_events(self):

        # 绑定登陆按钮
        self.btn_login.clicked.connect(self.controlor.login)

        # 更新我喜欢的吧
        self.btn_up_mylike.clicked.connect(self.controlor.up_mylikes)

        # 获取本地列表
        self.btn_get_local_list.clicked.connect(self.controlor.get_local_list)

        # 开始关注贴吧
        self.btn_to_like.clicked.connect(self.controlor.to_like)

        # 批量取关按钮
        self.btn_to_del.clicked.connect(self.controlor.to_del)
