"""
节日祝福/表白程序配置文件
修改这里即可自定义你的专属表白
"""

# -------------------- 对象名称 --------------------
# 你对象的昵称，会出现在密码提示、祝福语等位置
NICKNAME = "笨笨"

# -------------------- 密码/口令 --------------------
# 解锁屏幕时可以输入的合法口令（支持多个，任意一个即可通过）
# 程序会自动生成一些基于昵称的口令，你也可以在这里额外添加
PASSWORDS = [
    "亲签", "收到", "收到啦", "知道啦",
    "爱你", "我爱你",
]
# 以下口令会自动根据 NICKNAME 生成，无需手动添加：
#   "{NICKNAME}亲签", "本{NICKNAME}收到", "本{NICKNAME}收到啦",
#   "本{NICKNAME}知道啦", "本{NICKNAME}爱你"

# -------------------- 弹窗祝福语 --------------------
# 爱心和随机弹窗中显示的文字，随机抽取
MESSAGES = [
    "好好爱自己", "顺顺利利", "别熬夜", "多喝水哦~",
    "好好吃饭", "我想你了", "天天开心", "保持好心情",
    "永远爱你", "你笑起来真好看", "今天也要元气满满",
    "记得吃早餐", "累了就休息", "你是我的小幸运",
    "想抱抱你", "晚安好梦", "注意保暖哦", "睡觉香香",
    "你值得所有美好", "每天都要开心鸭", "我一直都在",
    "少吃辣多吃菜", "出门记得带伞", "你最棒的",
    "想你每一天", "做你的开心果", "永远站在你这边",
    "平安喜乐", "万事顺遂", "烦恼都丢掉",
]

# -------------------- 最终祝福语（打字机效果） --------------------
# 黑洞动画结束后逐字显示的文字，按顺序一行一行打出
FINAL_LINE_1 = "我会陪你很久很久 ❤ 不是我想 ❤ 而是我会"
FINAL_LINE_2 = "祝亲爱的{nickname}520快乐！"  # {nickname} 会被替换为 NICKNAME

# -------------------- 密码框提示文字 --------------------
EXIT_DIALOG_HINT = '520祝福已派送完毕~\n快输入\u201c{nickname}亲签\u201d解锁屏幕吧！'

# -------------------- 视觉主题 --------------------
# 后续界面美化统一从这里取色、字体和尺寸，方便整体换风格
THEME_NAME = "520_candy"
FONT_FAMILY = "微软雅黑"
EMOJI_FONT_FAMILY = "Segoe UI Emoji"

THEME_COLORS = {
    "cream": "#fff7fb",
    "rose_mist": "#ffe4ef",
    "blush": "#ffc6d9",
    "peach": "#ffd7c8",
    "candy": "#ff7eb6",
    "hot_pink": "#ff4f9a",
    "berry": "#d92573",
    "plum": "#3a1838",
    "plum_soft": "#5b3158",
    "lavender": "#eadcff",
    "sky": "#d8f0ff",
    "mint": "#dff8ed",
    "gold": "#ffd76a",
    "white": "#ffffff",
    "shadow": "#9f5a78",
}

# 兼容旧代码：随机弹窗仍然读取 BG_COLORS
BG_COLORS = [
    THEME_COLORS["rose_mist"],
    THEME_COLORS["blush"],
    THEME_COLORS["peach"],
    THEME_COLORS["lavender"],
    THEME_COLORS["sky"],
    THEME_COLORS["mint"],
]

TEXT_COLORS = {
    "primary": "#4a263a",
    "muted": "#8d5c75",
    "inverse": THEME_COLORS["white"],
    "accent": THEME_COLORS["berry"],
    "danger": "#d6285f",
}

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 18,
    "xl": 26,
}

POPUP_CARD_STYLE = {
    "border": THEME_COLORS["white"],
    "border_active": THEME_COLORS["hot_pink"],
    "header": THEME_COLORS["candy"],
    "header_alt": THEME_COLORS["berry"],
    "title_fg": THEME_COLORS["white"],
    "message_fg": TEXT_COLORS["primary"],
    "subtle_fg": TEXT_COLORS["muted"],
    "shadow": THEME_COLORS["shadow"],
    "padding_x": 12,
    "padding_y": 8,
    "header_height": 20,
    "border_width": 2,
    "corner_radius": 12,
    "titles": ["LOVE", "520", "MISS U"],
    "decorations": ["❤", "💕", "✨", "💗"],
}

EXIT_DIALOG_STYLE = {
    "width": 380,
    "height": 230,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["cream"],
    "title_fg": THEME_COLORS["berry"],
    "hint_fg": TEXT_COLORS["primary"],
    "muted_fg": TEXT_COLORS["muted"],
    "entry_bg": THEME_COLORS["white"],
    "entry_fg": TEXT_COLORS["primary"],
    "button_bg": THEME_COLORS["hot_pink"],
    "button_active_bg": THEME_COLORS["berry"],
    "button_fg": THEME_COLORS["white"],
    "error_fg": TEXT_COLORS["danger"],
    "shake_distance": 10,
    "shake_steps": 8,
    "shake_interval": 28,
}

BLACKHOLE_STYLE = {
    "size": 150,
    "bg": "#020013",
    "ring": THEME_COLORS["hot_pink"],
    "ring_alt": THEME_COLORS["lavender"],
    "heart": "💖",
    "heart_fg": THEME_COLORS["hot_pink"],
    "caption": "正在把爱意收进心里",
    "caption_fg": THEME_COLORS["cream"],
    "pulse_interval": 80,
    "batch_size": 24,
    "release_interval": 42,
    "frame_interval": 16,
    "min_frames": 14,
    "max_frames": 22,
    "spin_min": 0.08,
    "spin_max": 0.16,
    "cover_start": 0.84,
}

FINAL_SCENE_STYLE = {
    "width": 760,
    "height": 280,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["plum"],
    "content_bg_alt": THEME_COLORS["plum_soft"],
    "line1_fg": THEME_COLORS["blush"],
    "line2_fg": THEME_COLORS["hot_pink"],
    "decor_fg": THEME_COLORS["gold"],
    "muted_fg": "#f5b8d6",
    "cursor": "▌",
    "cursor_blink_interval": 420,
}

FONT_SIZES = {
    "popup_title": 9,
    "popup_message": 14,
    "dialog_title": 14,
    "dialog_hint": 11,
    "dialog_input": 14,
    "dialog_button": 11,
    "final_decor": 15,
    "final_line1": 22,
    "final_line2": 27,
}

# -------------------- 动画参数 --------------------
WINDOW_WIDTH = 180            # 弹窗宽度
WINDOW_HEIGHT = 80            # 弹窗高度
HEART_STEP = 3                # 爱心轮廓步长(度)，越小越密
HEART_SPEED = 120              # 绘制爱心时，相邻祝福弹窗出现间隔 (毫秒)，想慢一点就调大
HEART_STAY = 2000             # 整个爱心形状画完后的停留时间 (毫秒)
RANDOM_COUNT = 150            # 随机弹窗数量
RANDOM_SPEED = 25             # 随机弹窗出现间隔 (毫秒)

# -------------------- 粒子动画参数 --------------------
PARTICLE_COUNT = 55           # 飘落爱心粒子数量
PARTICLE_HEARTS = ["❤", "♥", "💕", "💗", "💖", "✨", "💫", "🌸"]
PARTICLE_COLORS = [
    THEME_COLORS["hot_pink"],
    THEME_COLORS["berry"],
    THEME_COLORS["candy"],
    THEME_COLORS["blush"],
    THEME_COLORS["lavender"],
    THEME_COLORS["gold"],
]
