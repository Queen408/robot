from ugot import ugot

camera_center_x = 320
camera_center_y = 240
max_rotate_speed = 30
max_forward_speed = 20
u = ugot.UGOT()
u.initialize("192.168.43.143")
u.load_models(["line_recognition","apriltag_qrcode","color_recognition"])
#向色块靠近
class GrabObject():

    def __init__(self) -> None:
        #创建PID控制器
        self.pid_rotate_speed = u.create_pid_controller()
        #设置PID控制器参数
        self.pid_rotate_speed.set_pid(0.1, 0, 0.007)

        self.pid_forward_speed = u.create_pid_controller()
        self.pid_forward_speed.set_pid(0.9, 0, 0.001)

        self.gap = 0

    #
    def go_and_grap_object(self, target_color):
        start_y_speed = 0
        # 调整小车朝向
        self.adjust_direction(start_y_speed, target_color)

    # 计算小车原地转动的速度
    def get_rotate_speed(self, target_color):
        color_info = u.get_color_total_info()
        [color, type, target_center_x, target_center_y, height, width, area] = color_info
        if (
                len(color) == 0
                or len(type) == 0
                or target_center_x == -1
                or str(target_color) != color
        ):
            target_center_x = 460  #！
            return 0

        gap = target_center_x - camera_center_x
        #调用PID
        rotate_speed = round(self.pid_rotate_speed.update(gap))
        if rotate_speed > max_rotate_speed:
            rotate_speed = max_rotate_speed
        if rotate_speed < -max_rotate_speed:
            rotate_speed = -max_rotate_speed
        print("转向速度",rotate_speed)
        return rotate_speed


    # 计算前进速度（负数就表示后退速度）
    def get_forward_speed(self, target_color):
        # 获取传感器数据
        distance = u.read_distance_data(21)
        print("距离:", distance)
        dis = 8 - distance
        # 调用PID
        forward_speed = round(self.pid_forward_speed.update(dis))
        if forward_speed > max_forward_speed:
            forward_speed = max_forward_speed
        if forward_speed < -max_forward_speed:
            forward_speed = -max_forward_speed
        print("前进速度:", forward_speed)
        return forward_speed


    # 调整小车朝向
    def adjust_direction(self, forward_speed, target_color):
        #获取小车旋速度
        rotate_speed = self.get_rotate_speed(target_color)
        forward_speed = self.get_forward_speed(target_color)
        while abs(rotate_speed) > 1 or abs(forward_speed) > 1:
            u.mecanum_move_xyz(0, int(forward_speed), int(rotate_speed))
            # 计算小车原地转动的速度
            rotate_speed = self.get_rotate_speed(target_color)
            forward_speed = self.get_forward_speed(target_color)
        u.mecanum_stop()

#逐渐靠近绿色色块
if __name__ == "__main__":
    grab_object = GrabObject()
    target_color="绿色"
    grab_object.go_and_grap_object(target_color)
    u.mecanum_stop()
