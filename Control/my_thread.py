from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QApplication
import time
import json
from multiprocessing.dummy import Pool as ThreadPool

class my_thread_login(QThread):

    login_success = pyqtSignal()
    login_failure = pyqtSignal()

    def __init__(self, tb=None, parent=None):
        super(my_thread_login, self).__init__(parent)
        self.tb = tb

    def run(self):
        try:
            self.tb.profile()
            self.login_success.emit()
        except:
            self.login_failure.emit()

class my_thread_update(QThread):

    update_success = pyqtSignal()
    update_failure = pyqtSignal()

    def __init__(self, tb=None, parent=None):
        super(my_thread_update, self).__init__(parent)
        self.tb = tb

    def run(self):
        try:
            self.tb.my_likes()
            self.update_success.emit()
        except:
            self.update_failure.emit()

class my_thread_to_like(QThread):

    to_like_ok = pyqtSignal()
    to_like_success_one = pyqtSignal(str)
    to_like_failure_one = pyqtSignal(str)

    def __init__(self, tb=None, parent=None):
        super(my_thread_to_like, self).__init__(parent)
        self.tb = tb

    def run(self):
        pool = ThreadPool(10)
        # 上面这句估计是开启线程池，我也不懂
        result = pool.map(self.like_one, self.tb.ready_like_list)
        pool.close()
        pool.join()
        self.to_like_ok.emit()

    def like_one(self, one):
            if self.tb.attention_one(one):
                self.to_like_success_one.emit(one)
            else:
                self.to_like_failure_one.emit(one)

class my_thread_to_del(QThread):

    to_del_ok = pyqtSignal()
    to_del_success_one = pyqtSignal(str)
    to_del_failure_one = pyqtSignal(str)

    def __init__(self, tb=None, parent=None):
        super(my_thread_to_del, self).__init__(parent)
        self.tb = tb

    def run(self):
        pool = ThreadPool(10)
        # 上面这句估计是开启线程池，我也不懂
        result = pool.map(self.del_one, self.tb.ready_del_list)
        pool.close()
        pool.join()
        self.to_del_ok.emit()

    def del_one(self, one):
        if self.tb.deleteone(one):
            self.to_del_success_one.emit(one)
        else:
            self.to_del_failure_one.emit(one)


