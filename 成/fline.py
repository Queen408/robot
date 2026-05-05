from ugot import ugot
import main
#巡线
u = ugot.UGOT()
u.initialize("192.168.43.143")
u.load_models(["line_recognition","apriltag_qrcode","color_recognition"])
u.set_track_recognition_line(0)
#创建一个PID控制器
pid_turn = u.create_pid_controller()
#设置PID控制器参数
pid_turn.set_pid(0.1, 0, 0.007)


max_rotate_speed = 30
max_forward_speed = 30

#获取小车旋转速度
def get_rotate_speed():
    line_info = u.get_single_track_total_info()
    print(line_info)
    offset, line_type, x, y = line_info
    if line_type == 0:
        return 0, line_type, 0, 0
    #设置PID控制器误差
    rotate_speed = round(pid_turn.update(offset))
    if rotate_speed > max_rotate_speed:
        rotate_speed = max_rotate_speed
    if rotate_speed < -max_rotate_speed:
        rotate_speed = -max_rotate_speed
    return rotate_speed, line_type, x, y

def fline():
    num = 0
    while True:
        speed_info = get_rotate_speed()
        rotate_speed, line_type, x, y = speed_info
        if line_type==1:
            #巡线前进
            u.mecanum_move_xyz(0, 20, -int(rotate_speed))
            print("巡线前进中。。。")
        elif line_type==3:
            u.mecanum_stop()
            print("路口")
            break
        else:
            u.mecanum_stop()
            print("没有识别到线")





#从起点出发到货物区
if __name__ == "__main__":
    fline()
    main.turnRight()
    fline()
    main.turnRight()
    fline()
