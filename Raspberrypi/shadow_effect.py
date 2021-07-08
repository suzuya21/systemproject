from PySide2.QtWidgets import QGraphicsDropShadowEffect

# 影つけるやつ
class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self):
        super(ShadowEffect,self).__init__()
        self.blur_radius = 20 # 影のぼかし半径
        self.color = 'red' # 色
        self.xoffset = 5 # x軸オフセット
        self.yoffset = 5 # y軸オフセット

        self.create_shadow()

    def create_shadow(self):
        self.setOffset(self.xoffset,self.yoffset)
        self.setBlurRadius(self.blur_radius)

if __name__ == '__main__':
    shadow = ShadowEffect()
    print(shadow)
