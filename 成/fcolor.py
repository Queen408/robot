from ugot import ugot
from time import sleep
camera_center_x = 320
camera_center_y = 240
max_rotate_speed = 60
max_forward_speed = 60
u = ugot.UGOT()
u.initialize("192.168.43.143")
u.load_models(["line_recognition","apriltag_qrcode","color_recognition"])
#逐渐旋转直到朝向想要的颜色
class FcolorTurn():

    def __init__(self) -> None:
        #创建PID控制器
        self.pid_rotate_speed = u.create_pid_controller()
        #设置PID控制器参数
        self.pid_rotate_speed.set_pid(0.3, 0, 0.08)


        self.gap = 0

    #
    def grap_object(self, target_color):
        start_y_speed = 0
        # 调整小车朝向
        self.adjust_direction(target_color)

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
            target_center_x = 460
            return -20
        u.mecanum_stop()
        gap = target_center_x - camera_center_x
        #调用PID
        rotate_speed = round(self.pid_rotate_speed.update(gap))
        if rotate_speed > max_rotate_speed:
            rotate_speed = max_rotate_speed
        if rotate_speed < -max_rotate_speed:
            rotate_speed = -max_rotate_speed
        print("转向速度",rotate_speed)
        return rotate_speed

    # 调整小车朝向
    def adjust_direction(self, target_color):
        #获取小车旋速度
        rotate_speed = self.get_rotate_speed(target_color)
        while abs(rotate_speed) > 13:
            u.mecanum_move_xyz(0, 0, int(rotate_speed))
            # 计算小车原地转动的速度
            rotate_speed = self.get_rotate_speed(target_color)
        u.mecanum_stop()

#朝向绿色色块
if __name__ == "__main__":
    grab_object = FcolorTurn()
    target_color="蓝色"
    grab_object.grap_object(target_color)
    u.mecanum_stop()