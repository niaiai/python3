from PIL import Image, ImageTk


['BR', 'BN', 'BB', 'BA', 'BK', 'BC', 'BP']


def is_CP(t, x, y):
    pass
BR = ImageTk.PhotoImage(Image.open('RES\BR.png'))
def is_side(*key):
    x, y = key[0]
    return -1<x<9 and -1<y<10

class CP_private:
    def __init__(self, x, y, c='B'):
        self.image = ImageTk.PhotoImage(Image.open('RES\%P.png' % c))
        self.x = x
        self.y = x
        self.c = c

    def move(self, x, y):
        self.x = x
        self.y = y

    def rule(self):
        if self.y < 5:
            if is_CP(0, self.x, self+1):
                return None
            else:
                return (self.x, self.y+1)
        else:
            temp = []
            for x, y in filter(is_side, [(self.x,self.y+1),(self.x-1,self.y),(self.x+1,self.y)]):
                if not is_CP(0,x,y):
                    temp.append((x,y))
            return temp

# t = filter(is_side,[(1,5),(1,45)])
# print(list(t))
