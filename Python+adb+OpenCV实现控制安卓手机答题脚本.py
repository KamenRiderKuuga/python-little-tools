import os
import cv2
import time

all_x = 550

method = cv2.TM_SQDIFF_NORMED
max_num = 18

def init_questions():
    dic_questions = {}
    for num in range(1, max_num):
        img_gray_small = get_gray_pic(f'Q{num}.jpg')
        dic_questions[num] = img_gray_small
    return dic_questions


def init_answers():
    dic_answers = {}
    for num in range(1, max_num):
        img_gray_small = get_gray_pic(f'A{num}.jpg')
        dic_answers[num] = img_gray_small
    return dic_answers


def get_gray_pic(name):
    image = cv2.imread(name)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return img_gray

dic_questions = init_questions()
dic_answers = init_answers()

while True:
    os.system("adb shell /system/bin/screencap -p /sdcard/screen.png") #截取屏幕，图片命名为screen.png
    os.system("adb pull /sdcard/screen.png E:/爬虫/Questions")
    img_gray_large = get_gray_pic('screen.png')
    match = False
    minValue = 0.2
    tap_location = 0
    for num in range(1, max_num):
        img_gray_question = dic_questions[num]
        result = cv2.matchTemplate(img_gray_question, img_gray_large, method)
        if cv2.minMaxLoc(result)[0] < minValue:
            minValue = cv2.minMaxLoc(result)[0]
            img_gray_answer = dic_answers[num]
            result = cv2.matchTemplate(img_gray_answer, img_gray_large, method)
            tap_location = cv2.minMaxLoc(result)[2][1]+50
            match = True
        
    if match == False:
        print("题库中不存在此题目！")
    else:
        print(f"正在点击{all_x},{tap_location}")
        os.system(f"adb shell input tap {all_x} {tap_location}")
        time.sleep(1)