
# 色の定義
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BG_COLOR = BLACK
P_COLOR = BLUE
O_COLOR = GREEN

COLORS = [
    BLUE,
    GREEN,
    RED
]


# 画面の設定
WIDTH, HEIGHT = 800, 800


# シミュレーションパラメータ
G = 6.67430e-11  # 万有引力定数 (m^3 kg^-1 s^-2)
ALPHA = 1 / 3  # 慣性の重み
DELTA_T = 7e7  # 時間ステップ (s)
STEPS = 300  # ステップ数
NOISE_STD = 1e-5  # 観測ノイズの標準偏差
