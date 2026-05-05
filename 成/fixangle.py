from ugot import ugot
from time import sleep
u = ugot.UGOT()
u.initialize("192.168.43.143")

#陀螺仪修正角度

def getCurrentAngle():
    """
    读取机器人当前姿态角(使用前建议先校准）
    :return: 返回当前角度值，浮点数
    """
    ret = u.read_gyro_data()
    angle = ret[2]
    return angle


def get_target():
    sleep(2)  # 静置几秒等角度稳定
    angle = 0
    for count in range(3):
        angle = angle + getCurrentAngle()
        sleep(0.5)
    angle = angle / 3
    print("target: %.2f" % angle)
    return angle


def angleFix(target, bias: int = 1):
    """
    :param target: 目标角度
    :param bias: 允许的偏差角度，整数
    :return: Null
    """
    flag_reset = 0  # 复位标志
    # 读取机器人当前姿态角(使用前建议先校准）
    angle = getCurrentAngle()
    # 转换角度表达为0~360
    angle = angle if angle > 0 else angle + 360
    target = target if target > 0 else target + 360
    if abs(angle - target) > 5:
        flag_reset = 1
    while 1:
        # 读取机器人当前姿态角(使用前建议先校准）
        angle = getCurrentAngle()
        # 转换角度表达为0~360
        angle = angle if angle > 0 else angle + 360
        if abs(angle - target) > bias:
            print("angle current: %.2f" % angle)
            print("angle target: %.2f" % target)
            if flag_reset == 1:
                u.mecanum_stop()
                flag_reset = 0
            if target < angle and abs(target - angle) < 180:
                u.mecanum_turn_speed_times(3, 30, int(abs(target - angle)), 2)
                u.mecanum_stop()
            elif target < angle and abs(target - angle) >= 180:
                u.mecanum_turn_speed_times(2, 30, int(360-abs(angle-target)), 2)
                u.mecanum_stop()
            elif target > angle and abs(target - angle) > 180:
                u.mecanum_turn_speed_times(3, 30, int(abs(target - angle)), 2)
                u.mecanum_stop()
            elif target > angle and abs(target - angle) <= 180:
                u.mecanum_turn_speed_times(2, 30, int(abs(  angle-target)), 2)
                u.mecanum_stop()
        else:
            print("角度调整完成")
            u.mecanum_stop()
            break

#小车会自动修正回原来的角度
if __name__ == "__main__":
    target = getCurrentAngle()
    print(111)
    sleep(2)
    print(111)
    while True:
        angleFix(target-90)
        




