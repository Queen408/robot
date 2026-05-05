from ugot import ugot
import fline
import tag
import fgocolor
import fcolor
import fixangle
import distence
import arm
import time

#测试文件

u = ugot.UGOT()
u.initialize("192.168.43.143")
u.load_models(["line_recognition","apriltag_qrcode","color_recognition"])

fline.fline()