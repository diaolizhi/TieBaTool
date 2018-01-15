from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from Model.Tieba import TieBa
from Control.my_thread import *


class Controlor():

    def __init__(self, MainWindow):
        self.tieba = TieBa("")
        self.mainwindow = MainWindow

    def login(self):
        bduss = self.mainwindow.le_bduss.text()
        self.tieba.BDUSS = bduss
        self.tieba.headers = {'Cookie':'BDUSS='+self.tieba.BDUSS}
        self.mainwindow.statusBar().showMessage("正在登录, 请稍等...")
        self.mainwindow.btn_login.setText("正在登录...")
        self.mainwindow.btn_login.setDisabled(True)
        self.my_thread_login = my_thread_login(self.tieba)
        self.my_thread_login.start()
        self.my_thread_login.login_success.connect(self.login_yes)
        self.my_thread_login.login_failure.connect(self.login_no)

    def login_yes(self):
        self.mainwindow.statusBar().showMessage("登录成功")
        self.mainwindow.Avatar.setPixmap(QPixmap("./head_img.jpg"))
        self.mainwindow.username.setText(self.tieba.username)
        self.mainwindow.le_bduss.setDisabled(True)
        self.mainwindow.btn_login.setText("登录成功")
        self.mainwindow.btn_login.setDisabled(True)
        self.mainwindow.btn_up_mylike.setDisabled(False)
        self.mainwindow.btn_to_like.setDisabled(False)
        self.mainwindow.btn_to_del.setDisabled(False)
        self.up_mylikes()

    def login_no(self):
        self.mainwindow.statusBar().showMessage("登录失败, 请检查 BDUSS 是否正确")
        self.mainwindow.btn_login.setText("登录")
        self.mainwindow.btn_login.setDisabled(False)

    def up_mylikes(self):
        self.mainwindow.btn_up_mylike.setText("正在更新")
        self.mainwindow.btn_up_mylike.setDisabled(True)
        self.mainwindow.statusBar().showMessage("正在更新, 可能需要一些时间")
        self.my_thread_update = my_thread_update(self.tieba)
        self.my_thread_update.start()

        self.my_thread_update.update_success.connect(self.update_yes)
        self.my_thread_update.update_failure.connect(self.update_no)

    def update_yes(self):
        self.mainwindow.btn_up_mylike.setText("更新我关注的吧")
        self.mainwindow.btn_up_mylike.setDisabled(False)
        self.mainwindow.lw_my_likes.clear()  # 清空列表
        for one in self.tieba.likelist:
            self.mainwindow.item = QListWidgetItem(one, self.mainwindow.lw_my_likes)
            self.mainwindow.item.setCheckState(False)
        self.mainwindow.statusBar().showMessage("我关注的吧更新成功!")

    def update_no(self):
        self.mainwindow.btn_up_mylike.setText("更新我关注的吧")
        self.mainwindow.btn_up_mylike.setDisabled(False)
        self.mainwindow.statusBar().showMessage("更新失败")

    def get_local_list(self):
        i = 0
        with open('./lists.json', 'r') as f:
            self.all_like_list = json.load(f)
        self.mainwindow.lw_local_list.clear()  # 清空列表
        for one in self.all_like_list:
            i += 1
            self.mainwindow.item = QListWidgetItem(one, self.mainwindow.lw_local_list)
            self.mainwindow.item.setCheckState(False)
        self.mainwindow.statusBar().showMessage("获取本地列表成功, 可勾选不想关注的贴吧")

    def to_like(self):
        reply = QMessageBox.question(self.mainwindow, '提示', '是否开始批量关注操作?(可勾选不想关注的贴吧)', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            mess = "---开始关注贴吧---\n"
            self.mainwindow.te_message.setText(mess)
            self.mainwindow.statusBar().showMessage("正在批量关注贴吧, 请稍等...")
            self.tieba.ready_like_list = []
            num = self.mainwindow.lw_local_list.count()
            for one in range(num):
                item = self.mainwindow.lw_local_list.item(one)
                ischeck = item.checkState()
                if ischeck == False:
                    self.tieba.ready_like_list.append(item.text())
            self.my_thread_to_like = my_thread_to_like(self.tieba)
            self.my_thread_to_like.start()
            self.my_thread_to_like.to_like_success_one.connect(self.to_like_one_success)
            self.my_thread_to_like.to_like_failure_one.connect(self.to_like_one_failure)
            self.my_thread_to_like.to_like_ok.connect(self.to_like_ok)
        else:
            pass

    def to_like_one_success(self, name):
        mess = self.mainwindow.te_message.toPlainText()
        mess += (name + "  " + "√\n")
        self.mainwindow.te_message.setText(mess)

    def to_like_one_failure(self, name):
        mess = self.mainwindow.te_message.toPlainText()
        mess += (name + "  " +"×\n")
        self.mainwindow.te_message.setText(mess)

    def to_like_ok(self):
        self.mainwindow.statusBar().showMessage("批量关注结束")
        mess = self.mainwindow.te_message.toPlainText()
        mess += "---结束---\n"
        self.mainwindow.te_message.setText(mess)

    def to_del(self):
        reply = QMessageBox.question(self.mainwindow, '提示', "是否进行批量取关操作?(请勾选想保留的贴吧)", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            mess = "---开始批量取关---\n"
            self.mainwindow.te_message.setText(mess)
            self.mainwindow.statusBar().showMessage("正在批量取关, 请稍等...")
            self.tieba.ready_del_list = []
            num = self.mainwindow.lw_my_likes.count()
            for one in range(num):
                item = self.mainwindow.lw_my_likes.item(one)
                ischeck = item.checkState()
                if  ischeck==False:
                    self.tieba.ready_del_list.append(item.text())
            self.my_thread_to_del = my_thread_to_del(self.tieba)
            self.my_thread_to_del.start()
            self.my_thread_to_del.to_del_success_one.connect(self.to_del_one_success)
            self.my_thread_to_del.to_del_failure_one.connect(self.to_del_one_failure)
            self.my_thread_to_del.to_del_ok.connect(self.to_del_ok)
        else:
            pass

    def to_del_one_success(self, name):
        mess = self.mainwindow.te_message.toPlainText()
        mess += (name + "  " + "√\n")
        self.mainwindow.te_message.setText(mess)

    def to_del_one_failure(self, name):
        mess = self.mainwindow.te_message.toPlainText()
        mess += (name + "  " + "×\n")
        self.mainwindow.te_message.setText(mess)

    def to_del_ok(self):
        self.mainwindow.statusBar().showMessage("取关结束")
        self.mainwindow.statusBar().showMessage("批量关注结束")
        mess = self.mainwindow.te_message.toPlainText()
        mess += "---结束---\n"
        self.mainwindow.te_message.setText(mess)


