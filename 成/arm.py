from ugot import ugot
from time import sleep

#机械臂动作
down = [90, 147, -32]#放下
up   = [90,  13, -78]#升起


u = ugot.UGOT()
u.initialize("192.168.43.143")

def armPlay(zd):
    for i in range(2,-1,-1):
        u.turn_servo_angle(i+51, zd[i], 1000, wait=True)


#机械臂升起，释放夹爪，夹起后举起
if __name__ == "__main__":
    armPlay(up)
    sleep(1)
    u.mechanical_clamp_release()
    armPlay(down)
    u.mechanical_clamp_close()
    armPlay(up)