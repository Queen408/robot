from ugot import ugot
import tag
import fixangle
import distence
import arm
import fline
import fgocolor
import fcolor
import time
#完整流程，分为part1和part2两个部分

def turnRight():
    u.mecanum_move_speed_times(0, 30, 16, 1)
    u.mecanum_turn_speed_times(3, 30, 88, 2)

def turnLeft():
    u.mecanum_move_speed_times(0, 30, 30, 1)
    u.mecanum_turn_speed_times(2, 30, 88, 2)

def goStraight():
    u.mecanum_move_speed_times(0, 30, 15, 1)

def ask1():
    u.play_audio_tts("请问需要搬运的物品颜色是什么",0,True)
    while True:
        ans = u.start_audio_asr()
        print(ans)
        if ans.find('红') > -1:
            return "红色"
        elif ans.find('蓝') > -1:
            return "蓝色"
        elif ans.find('绿') > -1:
            return "绿色"
        u.play_audio_tts("抱歉，没有听清，请再说一次",0,True)


def ask2():
    u.play_audio_tts("请问需要搬运到哪个高台",0,True)
    while True:
        ans = u.start_audio_asr()
        print(ans)
        if ans.find('1') > -1 or ans.find('一') or ans.find('A') or ans.find('a'):
            return "A"
        elif ans.find('2') > -1 or ans.find('二') or ans.find('B') or ans.find('b'):
            return "B"
        u.play_audio_tts("抱歉，没有听清，请再说一次",0,True)

def speak(st = ""):
    u.play_audio_tts(st, 0 , True)

#蓝色就是要夹起什么色块
def part1(target_color="蓝色"):
    #巡线寻找物块并夹起
    arm.armPlay(arm.up)
    fline.fline()
    turnRight()
    fline.fline()
    turnRight()
    fline.fline()
    fc = fcolor.FcolorTurn()
    fc.grap_object(target_color)
    u.mecanum_stop()
    fgc = fgocolor.GrabObject()
    fgc.go_and_grap_object(target_color)
    u.mecanum_stop()
    u.mechanical_clamp_release()
    arm.armPlay(arm.down)
    time.sleep(1)
    u.mechanical_clamp_close()
    time.sleep(1)
    arm.armPlay(arm.up)

#A或者B就是送到A或者B高台
def part2(target_park = "B"):
    fixangle.angleFix(target-110)
    u.mecanum_move_speed_times(0, 30, 10, 1)
    apriltag_tool = tag.FaceAprilTag(u)
    apriltag_tool.find_apriltag_and_face_it(5)
    apriltag_tool.find_apriltag_and_face_it(5)
    distence.dis(5)
    u.mecanum_turn_speed_times(2, 30, 90, 2)
    u.mecanum_translate_speed_times(45, 30, 5, 1)
    fline.fline()
    turnRight()
    fline.fline()
    if target_park == "B":
        goStraight()
        fline.fline()
    turnRight()
    fline.fline()
    distence.dis(5)
    u.mechanical_clamp_release()

u = ugot.UGOT()
u.initialize("192.168.43.143")
u.load_models(["line_recognition","color_recognition","apriltag_qrcode"])
target = fixangle.getCurrentAngle()

if __name__ == "__main__":
    target_color = "蓝色"
    target_park  = "A"
    speak(f"我要搬运{target_color}色物块并运输至{target_park}号存储区")
    part1(target_color)
    part2(target_park)

