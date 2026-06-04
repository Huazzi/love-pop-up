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

# 分幕式祝福语：弹窗会按顺序经历这些章节，让情绪推进更像一场小剧场
# 如果这里留空，程序会自动退回到上面的 MESSAGES 随机抽取模式
BLESSING_CHAPTERS = [
    {
        "title": "第一幕 · 先把你照顾好",
        "subtitle": "认真叮嘱，也认真喜欢你",
        "messages": [
            "别熬夜", "多喝水哦~", "好好吃饭", "记得吃早餐",
            "累了就休息", "注意保暖哦", "少吃辣多吃菜", "出门记得带伞",
        ],
    },
    {
        "title": "第二幕 · 我有一点想你",
        "subtitle": "不是一点点，是每一天",
        "messages": [
            "我想你了", "想抱抱你", "想你每一天", "晚安好梦",
            "睡觉香香", "做你的开心果", "我一直都在",
        ],
    },
    {
        "title": "第三幕 · 今天也要夸夸你",
        "subtitle": "你值得被很多很多温柔包围",
        "messages": [
            "你笑起来真好看", "你最棒的", "你值得所有美好",
            "今天也要元气满满", "保持好心情", "天天开心",
        ],
    },
    {
        "title": "第四幕 · 把爱意放久一点",
        "subtitle": "之后的日子，也站在你这边",
        "messages": [
            "永远爱你", "永远站在你这边", "平安喜乐", "万事顺遂",
            "烦恼都丢掉", "你是我的小幸运", "好好爱自己",
        ],
    },
]

# 轻互动选择：随机弹窗结束后出现，选择结果会进入后续签收提示
INTERACTION_CHOICES = [
    {
        "label": "开心",
        "reply": "那就把这份开心也一起签收吧",
    },
    {
        "label": "想我",
        "reply": "收到，接下来会多一点想你提醒",
    },
    {
        "label": "有点累",
        "reply": "那这份爱意先替你充充电",
    },
]

# 回忆碎片卡片：互动选择后展示，设置为空列表 [] 时会自动跳过
MEMORY_CARDS = [
    {
        "date": "某个普通日子",
        "title": "被你可爱到的瞬间",
        "text": "原来喜欢一个人，是会把很小的事情也记很久。",
        "icon": "💗",
    },
    {
        "date": "每个想你的晚上",
        "title": "想把温柔存起来",
        "text": "等你累的时候，就拿出来一点点给你。",
        "icon": "🌙",
    },
    {
        "date": "从今天到以后",
        "title": "这份偏爱会一直在",
        "text": "不是只在节日里，而是在往后的很多很多天里。",
        "icon": "💌",
    },
]

# -------------------- 最终祝福语（打字机效果） --------------------
# 黑洞动画结束后逐字显示的文字，按顺序一行一行打出
FINAL_LINE_1 = "我会陪你很久很久 ❤ 不是我想 ❤ 而是我会"
FINAL_LINE_2 = "祝亲爱的{nickname}天天开心！"  # {nickname} 会被替换为 NICKNAME

# -------------------- 密码框提示文字 --------------------
EXIT_DIALOG_HINT = '今日祝福已派送完毕~\n快输入\u201c{nickname}亲签\u201d解锁屏幕吧！'

# -------------------- 视觉主题 --------------------
# 后续界面美化统一从这里取色、字体和尺寸，方便整体换风格
THEME_NAME = "520_candy"
FONT_FAMILY = "LXGW Bright"
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

OPENING_LINES = [
    "给亲爱的{nickname}",
    "有一封专属来信正在抵达",
    "准备接收今天份的爱意",
]

OPENING_SCENE_STYLE = {
    "enabled": True,
    "width": 520,
    "height": 260,
    "duration": 4200,
    "frame_interval": 40,
    "countdown_from": 3,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["cream"],
    "content_bg_alt": THEME_COLORS["rose_mist"],
    "title_fg": THEME_COLORS["berry"],
    "body_fg": TEXT_COLORS["primary"],
    "muted_fg": TEXT_COLORS["muted"],
    "heart_fg": THEME_COLORS["hot_pink"],
    "decor_fg": THEME_COLORS["gold"],
    "max_alpha": 0.97,
    "heart": "💗",
    "eyebrow": "LOVE LETTER · PRELUDE",
}

CHAPTER_TOAST_STYLE = {
    "enabled": True,
    "width": 420,
    "height": 96,
    "top_offset": 54,
    "duration": 1700,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["cream"],
    "title_fg": THEME_COLORS["berry"],
    "subtitle_fg": TEXT_COLORS["primary"],
    "muted_fg": TEXT_COLORS["muted"],
    "decor_fg": THEME_COLORS["gold"],
    "alpha": 0.96,
    "icon": "💌",
}

INTERACTION_CHOICE_STYLE = {
    "enabled": True,
    "width": 460,
    "height": 310,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["cream"],
    "title_fg": THEME_COLORS["berry"],
    "body_fg": TEXT_COLORS["primary"],
    "muted_fg": TEXT_COLORS["muted"],
    "button_bg": THEME_COLORS["hot_pink"],
    "button_active_bg": THEME_COLORS["berry"],
    "button_fg": THEME_COLORS["white"],
    "button_alt_bg": THEME_COLORS["candy"],
    "icon": "💗",
    "title": "现在的心情是哪一种？",
    "subtitle": "选一个小状态，再继续签收这份爱意",
    "footer": "选哪一个都算我很想你",
}

MEMORY_CARD_STYLE = {
    "enabled": True,
    "width": 540,
    "height": 300,
    "card_duration": 1900,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["cream"],
    "content_bg_alt": THEME_COLORS["rose_mist"],
    "title_fg": THEME_COLORS["berry"],
    "body_fg": TEXT_COLORS["primary"],
    "muted_fg": TEXT_COLORS["muted"],
    "decor_fg": THEME_COLORS["gold"],
    "icon_fg": THEME_COLORS["hot_pink"],
    "eyebrow": "MEMORY FRAGMENT",
    "footer": "这些小碎片，也一起送给你",
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
    "height": 280,
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

STAMP_SIGNOFF_STYLE = {
    "enabled": True,
    "width": 230,
    "height": 150,
    "duration_frames": 18,
    "frame_interval": 45,
    "transparent_bg": "#010101",
    "stamp_fg": THEME_COLORS["berry"],
    "stamp_bg": THEME_COLORS["cream"],
    "ring": THEME_COLORS["hot_pink"],
    "ring_alt": THEME_COLORS["gold"],
    "text": "已签收",
    "caption": "爱意回执生效中",
    "alpha": 0.96,
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

TRANSITION_BURST_STYLE = {
    "enabled": True,
    "size": 520,
    "duration_frames": 22,
    "frame_interval": 35,
    "transparent_bg": "#010101",
    "ring": THEME_COLORS["hot_pink"],
    "ring_alt": THEME_COLORS["gold"],
    "spark_colors": [
        THEME_COLORS["hot_pink"],
        THEME_COLORS["blush"],
        THEME_COLORS["lavender"],
        THEME_COLORS["gold"],
    ],
    "heart": "💖",
    "caption": "最后一句话，马上送达",
    "caption_fg": THEME_COLORS["cream"],
    "alpha": 0.95,
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

KEEPSAKE_RECEIPT = {
    "enabled": True,
    "title": "最终留存回执",
    "subtitle": "这份爱意已经完成签收",
    "sender": "认真喜欢你的人",
    "recipient": "{nickname}",
    "validity": "永久有效",
    "serial": "LOVE-{nickname}-FOREVER",
    "items": [
        ("签收人", "{nickname}"),
        ("签收状态", "已确认查收"),
        ("心情备注", "{choice}"),
        ("有效期限", "从现在到很久很久以后"),
    ],
    "closing_lines": [
        "本次爱意已永久签收",
        "请把这张回执，留在今天的心里",
    ],
    "footer": "FOREVER RECEIPT · ONLY FOR YOU",
}

KEEPSAKE_RECEIPT_STYLE = {
    "enabled": True,
    "width": 620,
    "height": 420,
    "delay_after_typewriter": 2200,
    "display_duration": 7600,
    "outer_bg": THEME_COLORS["hot_pink"],
    "middle_bg": THEME_COLORS["blush"],
    "content_bg": THEME_COLORS["cream"],
    "content_bg_alt": THEME_COLORS["rose_mist"],
    "title_fg": THEME_COLORS["berry"],
    "body_fg": TEXT_COLORS["primary"],
    "muted_fg": TEXT_COLORS["muted"],
    "decor_fg": THEME_COLORS["gold"],
    "stamp_fg": THEME_COLORS["hot_pink"],
    "alpha": 0.98,
    "icon": "💌",
    "stamp_text": "永久签收",
}

FONT_SIZES = {
    "opening_eyebrow": 9,
    "opening_title": 20,
    "opening_body": 12,
    "opening_countdown": 30,
    "chapter_title": 12,
    "chapter_subtitle": 9,
    "choice_title": 15,
    "choice_body": 10,
    "choice_button": 11,
    "memory_eyebrow": 9,
    "memory_title": 19,
    "memory_date": 10,
    "memory_body": 12,
    "memory_footer": 9,
    "stamp_text": 22,
    "stamp_caption": 10,
    "burst_heart": 24,
    "burst_caption": 9,
    "popup_title": 9,
    "popup_message": 14,
    "dialog_title": 14,
    "dialog_hint": 11,
    "dialog_input": 14,
    "dialog_button": 11,
    "final_decor": 15,
    "final_line1": 22,
    "final_line2": 27,
    "receipt_title": 21,
    "receipt_subtitle": 10,
    "receipt_meta": 10,
    "receipt_item": 11,
    "receipt_closing": 13,
    "receipt_stamp": 14,
    "receipt_footer": 8,
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
