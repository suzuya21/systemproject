from PySide2.QtWidgets import QGraphicsDropShadowEffect
from PySide2.QtGui import QColor


# 影つけるやつ
class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self,parent=None):
        super(ShadowEffect,self).__init__(parent)
        self.blur_radius = 30 # 影のぼかし半径
        self.xoffset = 5 # x軸オフセット
        self.yoffset = 5 # y軸オフセット
        self.color = QColor(63, 63, 63, 180)
        # self.color = QColor(184, 136, 59, 180)

        self.create_shadow()

    def set_shadow_color(self,r,g,b,a):
        self.color = QColor(r,g,b,a)
        self.create_shadow()
        return self

    def create_shadow(self):
        self.setOffset(self.xoffset,self.yoffset)
        self.setBlurRadius(self.blur_radius)
        self.setColor(self.color)


if __name__ == '__main__':
    shadow = ShadowEffect()
    print(shadow)
