from ugot import ugot


#控制小车逐渐靠近
#gldistance是距离远近

camera_center_x = 320
camera_center_y = 240
max_rotate_speed = 30
max_forward_speed = 20
u = ugot.UGOT()
u.initialize("192.168.43.143")
gldistance = 6

class Distence():

    def __init__(self) -> None:
        self.pid_forward_speed = u.create_pid_controller()
        self.pid_forward_speed.set_pid(0.9, 0, 0.001)

        self.gap = 0

    #
    def go_and_grap_object(self):
        start_y_speed = 0
        self.adjust_direction(start_y_speed)



    # 计算前进速度（负数就表示后退速度）
    def get_forward_speed(self):
        # 获取传感器数据
        global gldistance
        distance = u.read_distance_data(21)
        print("距离:", distance)
        dis = gldistance - distance
        print(gldistance)
        # 调用PID
        forward_speed = round(self.pid_forward_speed.update(dis))
        if forward_speed > max_forward_speed:
            forward_speed = max_forward_speed
        if forward_speed < -max_forward_speed:
            forward_speed = -max_forward_speed
        print("前进速度:", forward_speed)
        return forward_speed


    # 调整小车朝向
    def adjust_direction(self, forward_speed):
        #获取小车旋速度
        forward_speed = self.get_forward_speed()
        while abs(forward_speed) > 1:
            u.mecanum_move_xyz(0, int(forward_speed), 0)
            # 计算小车原地转动的速度
            forward_speed = self.get_forward_speed()
        u.mecanum_stop()


def dis(x = 6):
    global gldistance
    gldistance = x
    grab_object = Distence()
    grab_object.go_and_grap_object()
    u.mecanum_stop()

#逐渐靠近到距离为4厘米
if __name__ == "__main__":
    dis(4)
    distance = u.read_distance_data(21)
    print(distance)

