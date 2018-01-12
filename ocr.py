import sys
import numpy as np
import cv2
import glob

prefix='.'

def breakCaptcha(captchaPath, BGPath=prefix + '/BGs', charLib=prefix + '/charLib'):
    output = ''
    min_sf = 255.0;
    for bgfilename in glob.iglob(BGPath + '/BG*.png'):
        img = cv2.imread(captchaPath)
        bg = cv2.imread(bgfilename)

        height = img.shape[0]
        width = img.shape[1]

        s = 0
        for i in range(0, height):
            for j in range(0, width):
                if img[i,j][0] < bg[i,j][0]:
                    R = bg[i,j][0] - img[i,j][0]
                else:
                    R = img[i,j][0] - bg[i,j][0]
                if img[i,j][1] < bg[i,j][1]:
                    G = bg[i,j][1] - img[i,j][1]
                else:
                    G = img[i,j][1] - bg[i,j][1]
                if img[i,j][2] < bg[i,j][2]:
                    B = bg[i,j][2] - img[i,j][2]
                else:
                    B = img[i,j][2] - bg[i,j][2]

                img[i,j] = (R,G,B)

                s = s + sum(img[i,j])

        sf = s / (height * width * 3)
        if sf < min_sf:
            min_sf = sf
            min_bg = bgfilename

    img = cv2.imread(captchaPath)
    bg = cv2.imread(min_bg)

    for i in range(0, height):
        for j in range(0, width):
            if img[i,j][0] < 255 or img[i,j][1] < 255 or img[i,j][2] < 255:
                if img[i,j][0] < bg[i,j][0]:
                    R = bg[i,j][0] - img[i,j][0]
                else:
                    R = img[i,j][0] - bg[i,j][0]
                if img[i,j][1] < bg[i,j][1]:
                    G = bg[i,j][1] - img[i,j][1]
                else:
                    G = img[i,j][1] - bg[i,j][1]
                if img[i,j][2] < bg[i,j][2]:
                    B = bg[i,j][2] - img[i,j][2]
                else:
                    B = img[i,j][2] - bg[i,j][2]

                img[i,j] = (R,G,B)

                if sum(img[i,j]) > 200:
                    img[i,j] = (255,255,255)
                else:
                    img[i,j] = (0,0,0)

    cuts = [30,0,0,0,0]
    possible_start = 33;
    last = 30
    for chIdx in range(1, 4):

        min_s = 1999999999
        for i in range(10, 32):
            s = 0;
            for j in range(0, height):

                s = s + img[j, possible_start + i][0]
                s = s + img[j, possible_start + i][1]
                s = s + img[j, possible_start + i][2]

            if s <= min_s:
                min_s = s
                cut = i
            else:
                if min_s == 0:
                    break

        cuts[chIdx] = cut + possible_start;

        last = cut + possible_start;
        possible_start = possible_start + cut + 3;

    chIdx = 4
    cut = 40
    cuts[chIdx] = cut + possible_start;

    for chIdx in range(0, 4):

        min_sf = 255.0
        possible_start = cuts[chIdx];
        for charfilename in glob.iglob(charLib + '/*.png'):
            ch = cv2.imread(charfilename)
            chheight = ch.shape[0]
            chwidth = ch.shape[1]

            for i in range(-10, 10):
                min_s = min_sf * (chheight * chwidth * 3)
                #diff = np.zeros((chheight, chwidth, 3), np.uint8)
                s = 0;
                for j in range(0, chheight):
                    for k in range(0, chwidth):
                        if img[j,k+i+possible_start][0] < ch[j,k][0]:
                            #diff[j,k][0] = ch[j,k][0] - img[j,k+i+possible_start][0]
                            s = s + ch[j,k][0] - img[j,k+i+possible_start][0]
                        else:
                            #diff[j,k][0] = img[j,k+i+possible_start][0] - ch[j,k][0]
                            s = s + img[j,k+i+possible_start][0] - ch[j,k][0]
                        if img[j,k+i+possible_start][1] < ch[j,k][1]:
                            #diff[j,k][1] = ch[j,k][1] - img[j,k+i+possible_start][1]
                            s = s + ch[j,k][1] - img[j,k+i+possible_start][1]
                        else:
                            #diff[j,k][1] = img[j,k+i+possible_start][1] - ch[j,k][1]
                            s = s + img[j,k+i+possible_start][1] - ch[j,k][1]
                        if img[j,k+i+possible_start][2] < ch[j,k][2]:
                            #diff[j,k][2] = ch[j,k][2] - img[j,k+i+possible_start][2]
                            s = s + ch[j,k][2] - img[j,k+i+possible_start][2]
                        else:
                            #diff[j,k][2] = img[j,k+i+possible_start][2] - ch[j,k][2]
                            s = s + img[j,k+i+possible_start][2] - ch[j,k][2]

                        #s = s + sum(diff[j,k])
                        if s >= min_s:
                            break

                    if s >= min_s:
                        break

                sf = s / (chheight * chwidth * 3)
                if sf < min_sf:
                    min_sf = sf
                    min_offset = i
                    min_ch = charfilename

        output = output + min_ch.split("/")[-1].split(".")[0]
    output = output[0:4]

    return output
