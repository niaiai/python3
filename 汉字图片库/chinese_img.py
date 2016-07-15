# -*- coding: UTF-8 -*-

import pygame
import os

# 以二进制读取文件，然后进行utf-8解码
f = open('word.txt', 'rb')
words = f.readlines()[0].decode('utf-8')
f.close()


def pasteWord(words):
    os.chdir('./IMAGE')
    pygame.init()
    # font_path = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
    font_path = "C:\Windows\Fonts\simkai.ttf"
    font = pygame.font.Font(font_path, 22)

    text_list = words.split(' ')
    length = len(text_list)
    for i in range(length):
        if not text_list[i]:
            continue
        text = text_list[i]
        imgName = text+'.png'
        if os.path.isfile(imgName):
            print('重复汉字', text)
            continue
        else:
            rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
            pygame.image.save(rtext, imgName)


if __name__ == '__main__':
    pasteWord(words)
