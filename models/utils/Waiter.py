from PyQt5 import QtCore as qtc
from models.utils.Pointer import Pointer

class Waiter():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Waiter, cls).__new__(cls)
        return cls.instance

    mutex = qtc.QMutex()
    condition = qtc.QWaitCondition()

    def block(self, Condition):
        self.mutex.lock()
        while Condition():
            self.condition.wait(self.mutex)
        self.mutex.unlock()

    def unblock(self, Function):
        self.mutex.lock()
        Function()
        self.mutex.unlock()
        self.condition.wakeAll()

    def unblock_test(self, tests_done, ptr:Pointer):
        self.mutex.lock()
        tests_done[ptr.id] = True
        ptr.id += 1
        self.condition.wakeAll()
        self.mutex.unlock()