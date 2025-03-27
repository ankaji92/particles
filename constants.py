import numpy as np

G = 6.67430e-11  # 万有引力定数

SCREEN_SHAPE = np.array([800, 600])  # 画面の形状 (width, height)
SCREEN_CENTER = SCREEN_SHAPE / 2  # 画面の中心 (x, y)

SCALE = 1e9  # 10^9メートルを1ピクセルとする

BG_COLOR = (0, 0, 0)

DELTA_T = 86400  # 1日

CIRCLE_RADIUS = 5  # 円の半径
