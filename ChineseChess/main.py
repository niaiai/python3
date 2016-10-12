import copy
import tkinter as tk
import tkinter.dialog as dialog
from PIL import Image, ImageTk

root = tk.Tk()
root.wm_title('中国象棋')
root.iconbitmap('QQ.ico')


class make_board:
    def __init__(self, root, L=50):
        self.L = L
        self.root = root
        self.W = L * 10
        self.H = L * 11
        self.off = L
        self.dic = self.dic()
        self.turn = 1
        self.can = tk.Canvas(self.root, width=self.W, height=self.H, bg='#26FDFD')
        self.can.pack()
        self.can.bind_all("<Button-1>", self.deal)

    def __xy_site(self, *xy):
        if xy[0]:
            tem = []
            for i, item in enumerate(xy[1:]):
                if i % 2:
                    tem.append((9-item)*self.L+self.off)
                else:
                    tem.append((8-item)*self.L+self.off)
            return tem
        else:
            return [self.off+item*self.L for item in xy[1:]]

    def dic(self):
        key = ['K', 'A', 'B', 'N', 'R', 'C', 'P']
        dic = {}
        for i in range(1, 8):
            dic[i] = ImageTk.PhotoImage(Image.open('RES\B%s.png' % key[i-1]))
            dic[-i] = ImageTk.PhotoImage(Image.open('RES\R%s.png' % key[i-1]))
        dic[0] = ImageTk.PhotoImage(Image.open('RES\SELECTED_l.png'))
        dic[10] = ImageTk.PhotoImage(Image.open('RES\SELECTED.png'))
        return dic

    def current(self):
        current = [[0]*9 for j in range(10)]
        for i in range(9):
            current[0][i] = 1+abs(i-4)
            current[9][i] = -current[0][i]
        current[2][1] = 6
        current[2][7] = 6

        current[7][1] = -6
        current[7][7] = -6

        for i in range(0, 9, 2):
            current[3][i] = 7
            current[6][i] = -7
        return current

    def make_board(self):
        self.can.create_rectangle(self.__xy_site(0, 0, 0, 8, 9), width=2)
        self.can.create_text(self.__xy_site(0, 1, 4.5), text='楚河')
        self.can.create_text(self.__xy_site(0, 7, 4.5), text='汉界')

        def create_line(r=0):
            for i in range(1, 5):
                self.can.create_line(self.__xy_site(r, 0, i, 8, i))
            for i in range(1, 8):
                self.can.create_line(self.__xy_site(r, i, 0, i, 4))
            self.can.create_line(self.__xy_site(r, 3, 0, 5, 2))
            self.can.create_line(self.__xy_site(r, 3, 2, 5, 0))
        create_line()
        create_line(1)

    def make_piece(self, x, y, key):
        x = x*self.L + self.off
        y = y*self.L + self.off
        return self.can.create_image(x, y, image=self.dic[key])

    def init(self):
        self.make_board()
        self.cur = self.current()
        self.selected = []
        self.next = []
        self.me = ' '
        self.me_key = ' '
        self.turn = -self.turn
        self.key = [[0]*9 for j in range(10)]
        for y in range(10):
            for x in range(9):
                if self.cur[y][x]:
                    self.key[y][x] = self.make_piece(x, y, self.cur[y][x])

    def game_over(self, mess):
        d = dialog.Dialog(None, title='游戏结束', text=mess,
            bitmap=dialog.DIALOG_ICON,default=0,strings=('再来一局', '不玩了 拜拜'))
        if d.num:
            self.root.quit()
        else:
            self.can.delete('all')
            self.init()

    def deal(self, event):
        def turn(x, y):
            return (x + y) > max(x, y) or (x + y) < min(x, y)
        x = int((event.x - self.off*2/3)//self.L)
        y = int((event.y - self.off*2/3)//self.L)
        if (y, x) in self.next and self.me_key:
            x1, y1 = self.me_key
            key = self.key[y1][x1]
            piece = self.cur[y1][x1]
            self.key[y1][x1] = 0
            self.cur[y1][x1] = 0
            self.can.move(key, (x-x1)*self.L, (y-y1)*self.L)
            self.root.update()
            if self.cur[y][x]:
                self.can.delete(self.key[y][x])
                if abs(self.cur[y][x]) == 1:
                    if self.cur[y][x] == 1:
                        mess = '游戏结束 红方胜!'
                    else:
                        mess = '游戏结束 黑方胜!'
                    self.game_over(mess)
                    return None
                self.key[y][x] = 0
                self.cur[y][x] = 0
            self.key[y][x] = key
            self.cur[y][x] = piece
            self.me_key = ''
            self.turn = -self.turn
            if self.selected:
                for i in self.selected:
                    self.can.delete(i)
                self.selected = []
            if self.me:
                self.can.delete(self.me)
        else:
            self.me_key = ''
            if self.selected:
                for i in self.selected:
                    self.can.delete(i)
                self.selected = []
            if self.me:
                self.can.delete(self.me)
            if 0 <= x < 9 and 0 <= y < 10:
                if self.cur[y][x] and turn(self.turn, self.cur[y][x]):
                    self.turn = self.cur[y][x]
                    self.me = self.make_piece(x, y, 10)
                    self.me_key = (x, y)
                    self.next = self.moverule(y, x)
                    for x, y in self.next:
                        self.selected.append(self.make_piece(y, x, 0))

    def moverule(self, i, j):
        index = abs(self.cur[i][j])
        next = []
        if index == 0:
            next = []
        elif index == 1:
            next = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for k, l in copy.deepcopy(next):
                if k not in(0, 1, 2, 7, 8, 9) or l not in (3, 4, 5):
                    next.remove((k, l))
            start = {1: [0, 1, 2], -1: [7, 8, 9]}
            mystart = start[self.cur[i][j]]
            enemystart = start[-self.cur[i][j]]

            enemy_i = -10
            for k in enemystart:
                if self.cur[k][j] == -self.cur[i][j]:
                    enemy_i = k
            nums = 0
            for k in range(min(i, enemy_i)+1, max(i, enemy_i)):
                if (enemy_i != -10 and self.cur[k][j] != 0):
                    nums += 1
            if nums == 0 and enemy_i != -10:
                next.append((enemy_i, j))
        elif index == 2:
            next = [(i-1, j-1), (i+1, j-1), (i-1, j+1), (i+1, j+1)]
            for k, l in copy.deepcopy(next):
                if k not in (0, 1, 2, 7, 8, 9) or l not in(3, 4, 5):
                    next.remove((k, l))
        elif index == 3:
            next = [(i-2, j-2), (i+2, j-2), (i-2, j+2), (i+2, j+2)]
            for k, l in copy.deepcopy(next):
                if (k-4.5)*(i-4.5)<0 or k<0 or k>9 or l<0 or l>8 :
                    next.remove((k, l))
            for k, l in copy.deepcopy(next):
                if self.cur[(i+k)//2][(j+l)//2] != 0:
                    next.remove((k, l))
        elif index == 4:
            next = [(i-2, j+1), (i-2, j-1), (i-1, j+2), (i-1, j-2), (i+2, j-1), (i+2, j+1), (i+1, j+2), (i+1, j-2)]
            for k, l in copy.deepcopy(next):
                if k < 0 or k > 9 or l < 0 or l > 8:
                    next.remove((k, l))
            for k, l in copy.deepcopy(next):
                biejiao_i = int(i if abs(k-i) == 1 else (i+k)/2)
                biejiao_j = int(j if abs(l-j) == 1 else (j+l)/2)
                if self.cur[biejiao_i][biejiao_j] != 0:
                    next.remove((k, l))

        elif index == 5 or index == 6:
            for k, l in [(k, j) for k in range(10)]+[(i, k) for k in range(9)]:
                if (k, l) == (i, j):
                    continue
                nums = 0
                for (k_try, l_try) in [(i, l_try) for l_try in range(min(j, l)+1, max(j, l))]+[(k_try, j) for k_try in range(min(i, k)+1, max(i, k))]: 
                    if self.cur[k_try][l_try] != 0:
                        nums+=1

                if index == 5 and nums == 0:
                    next.append((k, l))
                if index == 6:
                    if (self.cur[k][l] == 0  and nums == 0) or ( self.cur[k][l] != 0 and nums == 1 ):
                        next.append((k, l))
        elif index == 7:
            value=int(self.cur[i][j]/index)
            if value*(i-4.5) < 0:
                next = [(i+value, j)]
            else:
                next = [(i+value, j), (i, j-1), (i, j+1)]
                for k, l in copy.deepcopy(next):
                    if k<0 or k>9 or l<0 or l>8 :
                        next.remove((k, l))
        for k, l in copy.deepcopy(next):
            if(self.cur[i][j]*self.cur[int(k)][int(l)] > 0):
                next.remove((k, l))
        return next


if __name__ == '__main__':
    board = make_board(root)
    board.init()
    root.mainloop()
