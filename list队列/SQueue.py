
class QueueUnderflow(ValueError):
    """SQueue 为空时进行dequeue时的异常类"""
    pass


class SQueue:
    """基于python list实现的队列"""
    def __init__(self, init_len=8):
        self._len = init_len
        self._elems = [0] * self._len
        self._num = 0
        self._head = 0

    def is_empty(self):
        return self._num == 0

    def peek(self):
        if self._num == 0:
            raise QueueUnderflow
        return self._elems[self._head]

    def dequeue(self):
        if self._num == 0:
            raise QueueUnderflow
        e = self._elems[self._head]
        self._head = (self._head + 1) % self._len
        self._num -= 1
        return e

    def enqueue(self, e):
        if self._num == self._len:
            self.__extend_pro()
        self._elems[(self._num + self._head) % self._len] = e
        self._num += 1

    def __extend(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0] * self._len
        for i in range(old_len):
            new_elems[i] = self._elems[(self._head + i) % old_len]
        self._elems, self._head = new_elems, 0

    def __extend_pro(self):
        self._elems.extend([0] * self._len)
        for i in range(self._head):
            self._elems[self._len + i] = self._elems[i]
        self._len *= 2

    def __str__(self):
        s = [self._elems[(self._head + i) % self._len] for i in range(self._num)]
        return str(s)

