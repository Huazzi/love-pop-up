import ctypes
import os
import random
import math
import sys

APP_FONT_FILE = os.path.join("assets", "fonts", "LXGWBright-Regular.ttf")
FR_PRIVATE = 0x10


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def load_private_font(relative_path):
    if sys.platform != "win32":
        return False

    font_path = resource_path(relative_path)
    if not os.path.exists(font_path):
        return False

    return ctypes.windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0) > 0


load_private_font(APP_FONT_FILE)

import tkinter as tk
from config import (
    NICKNAME, PASSWORDS, MESSAGES, BG_COLORS, BLESSING_CHAPTERS,
    INTERACTION_CHOICES, MEMORY_CARDS,
    FINAL_LINE_1, FINAL_LINE_2, EXIT_DIALOG_HINT,
    WINDOW_WIDTH, WINDOW_HEIGHT, HEART_STEP, HEART_SPEED, HEART_STAY,
    RANDOM_COUNT, RANDOM_SPEED,
    PARTICLE_COUNT, PARTICLE_HEARTS, PARTICLE_COLORS,
    FONT_FAMILY, EMOJI_FONT_FAMILY, POPUP_CARD_STYLE, FONT_SIZES,
    EXIT_DIALOG_STYLE, BLACKHOLE_STYLE, FINAL_SCENE_STYLE, SPACING,
    OPENING_LINES, OPENING_SCENE_STYLE, CHAPTER_TOAST_STYLE,
    INTERACTION_CHOICE_STYLE, MEMORY_CARD_STYLE,
    STAMP_SIGNOFF_STYLE, TRANSITION_BURST_STYLE,
    KEEPSAKE_RECEIPT, KEEPSAKE_RECEIPT_STYLE,
)

# 根据昵称自动生成额外口令
_AUTO_PASSWORDS = [
    f"{NICKNAME}亲签",
    f"本{NICKNAME}收到", f"本{NICKNAME}收到啦",
    f"本{NICKNAME}知道啦", f"本{NICKNAME}爱你",
]
ALL_PASSWORDS = list(set(PASSWORDS + _AUTO_PASSWORDS))

class PopupApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 完全隐藏主窗口

        self.all_windows = []
        self.heart_points = []
        self.current_step = 0
        self.after_id = None
        self.blackhole_win = None
        self.blackhole_canvas = None
        self.blackhole_running = False
        self.blackhole_pulse = 0
        self.opening_win = None
        self.opening_canvas = None
        self.opening_running = False
        self.opening_tick = 0
        self.blessing_chapters = []
        self.popup_flow_index = 0
        self.popup_flow_total = 1
        self.active_chapter_idx = None
        self.chapter_toast_win = None
        self.chapter_toast_after_id = None
        self.interaction_choice = None
        self.interaction_reply = ""
        self.interaction_win = None
        self.memory_cards = []
        self.memory_idx = 0
        self.memory_win = None
        self.memory_canvas = None
        self.memory_after_id = None
        self.stamp_win = None
        self.stamp_canvas = None
        self.stamp_after_id = None
        self.stamp_running = False
        self.transition_burst_win = None
        self.transition_burst_canvas = None
        self.transition_burst_after_id = None
        self.final_win = None
        self.particle_windows = []
        self.particle_data = []
        self.particle_running = False
        self.typewriter_cursor_running = False
        self.keepsake_win = None
        self.keepsake_after_id = None

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # 爱心缩放系数
        short_side = min(self.screen_width, self.screen_height)
        target_width = short_side * 0.8
        self.heart_scale = max(target_width / 32, 1.0)

        # 绑定紧急退出快捷键 Ctrl+Shift+Q
        self.root.bind_all("<Control-Shift-Q>", lambda e: self.emergency_exit())

        # 延迟启动动画
        self.root.after(100, self.show_opening_scene)

    def show_opening_scene(self):
        style = OPENING_SCENE_STYLE
        if not style.get("enabled", True):
            self.start_animation()
            return

        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"{width}x{height}+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.0)
        win.config(bg=style["outer_bg"])
        win.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())

        canvas = tk.Canvas(
            win,
            width=width,
            height=height,
            bg=style["outer_bg"],
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self.opening_win = win
        self.opening_canvas = canvas
        self.opening_running = True
        self.opening_tick = 0
        self.opening_lines = [
            line.replace("{nickname}", NICKNAME) for line in OPENING_LINES
        ] or [f"给亲爱的{NICKNAME}"]
        self._animate_opening_scene()

    def _animate_opening_scene(self):
        if (
            not self.opening_running
            or self.opening_win is None
            or self.opening_canvas is None
        ):
            return

        style = OPENING_SCENE_STYLE
        frame_interval = style["frame_interval"]
        total_ticks = max(1, style["duration"] // frame_interval)
        progress = min(1.0, self.opening_tick / total_ticks)

        if progress >= 1.0:
            self._finish_opening_scene()
            return

        canvas = self.opening_canvas
        width, height = style["width"], style["height"]
        canvas.delete("all")

        alpha = min(style["max_alpha"], style["max_alpha"] * (self.opening_tick / 8))
        if progress > 0.86:
            alpha *= max(0.0, 1 - (progress - 0.86) / 0.14)
        try:
            self.opening_win.attributes("-alpha", alpha)
        except tk.TclError:
            return

        self._draw_round_rect(
            canvas,
            4,
            4,
            width - 4,
            height - 4,
            22,
            fill=style["outer_bg"],
            outline="",
        )
        self._draw_round_rect(
            canvas,
            10,
            10,
            width - 10,
            height - 10,
            18,
            fill=style["middle_bg"],
            outline="",
        )
        self._draw_round_rect(
            canvas,
            16,
            16,
            width - 16,
            height - 16,
            16,
            fill=style["content_bg"],
            outline="",
        )
        canvas.create_oval(
            -60,
            -70,
            170,
            150,
            fill=style["content_bg_alt"],
            outline="",
        )
        canvas.create_oval(
            width - 145,
            height - 125,
            width + 58,
            height + 58,
            fill=style["content_bg_alt"],
            outline="",
        )

        for i, dot_x in enumerate(range(60, width - 40, 86)):
            dot_y = 52 + (i % 2) * 10
            canvas.create_oval(
                dot_x,
                dot_y,
                dot_x + 4,
                dot_y + 4,
                fill=style["decor_fg"],
                outline="",
            )

        pulse = math.sin(self.opening_tick * 0.35)
        heart_size = int(38 + pulse * 5)
        canvas.create_text(
            width / 2,
            68,
            text=style["heart"],
            font=(EMOJI_FONT_FAMILY, heart_size),
            fill=style["heart_fg"],
        )
        canvas.create_text(
            width / 2,
            106,
            text=style["eyebrow"],
            font=(FONT_FAMILY, FONT_SIZES["opening_eyebrow"], "bold"),
            fill=style["muted_fg"],
        )

        line_count = max(1, len(self.opening_lines))
        line_idx = min(line_count - 1, int(progress * line_count))
        canvas.create_text(
            width / 2,
            145,
            text=self.opening_lines[line_idx],
            font=(FONT_FAMILY, FONT_SIZES["opening_title"], "bold"),
            fill=style["title_fg"],
            width=width - 72,
            justify="center",
        )

        countdown = style["countdown_from"] - int(
            progress * style["countdown_from"]
        )
        countdown_text = str(max(1, countdown)) if progress < 0.82 else "♡"
        canvas.create_text(
            width / 2,
            196,
            text=countdown_text,
            font=(FONT_FAMILY, FONT_SIZES["opening_countdown"], "bold"),
            fill=style["heart_fg"],
        )
        canvas.create_text(
            width / 2,
            228,
            text="这一刻，先留给你",
            font=(FONT_FAMILY, FONT_SIZES["opening_body"]),
            fill=style["body_fg"],
        )

        self.opening_tick += 1
        self.after_id = self.root.after(frame_interval, self._animate_opening_scene)

    def _finish_opening_scene(self):
        self.opening_running = False
        self.after_id = None
        self._destroy_opening_scene()
        self.start_animation()

    def _destroy_opening_scene(self):
        self.opening_running = False
        if self.opening_win is not None:
            try:
                self.opening_win.destroy()
            except tk.TclError:
                pass
        self.opening_win = None
        self.opening_canvas = None

    def start_animation(self):
        self.cleanup()
        self.heart_points = self.generate_heart_points()
        self.current_step = 0
        self._prepare_blessing_flow()
        self.spawn_heart_step()

    def _prepare_blessing_flow(self):
        self.blessing_chapters = [
            chapter for chapter in BLESSING_CHAPTERS
            if chapter.get("messages")
        ]
        self.popup_flow_index = 0
        self.popup_flow_total = max(1, len(self.heart_points) + RANDOM_COUNT)
        self.active_chapter_idx = None

    def _select_popup_message(self):
        if not self.blessing_chapters:
            return random.choice(MESSAGES) if MESSAGES else "爱你"

        chapter_idx = min(
            len(self.blessing_chapters) - 1,
            int(self.popup_flow_index * len(self.blessing_chapters) / self.popup_flow_total),
        )
        chapter = self.blessing_chapters[chapter_idx]

        if chapter_idx != self.active_chapter_idx:
            self.active_chapter_idx = chapter_idx
            self._show_chapter_toast(chapter, chapter_idx)

        self.popup_flow_index += 1
        messages = chapter.get("messages") or MESSAGES
        return random.choice(messages) if messages else "爱你"

    def _show_chapter_toast(self, chapter, chapter_idx):
        style = CHAPTER_TOAST_STYLE
        if not style.get("enabled", True):
            return

        self._destroy_chapter_toast()

        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = style["top_offset"]

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"{width}x{height}+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", style["alpha"])
        win.config(bg=style["outer_bg"])

        canvas = tk.Canvas(
            win,
            width=width,
            height=height,
            bg=style["outer_bg"],
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self._draw_round_rect(
            canvas,
            4,
            4,
            width - 4,
            height - 4,
            18,
            fill=style["middle_bg"],
            outline="",
        )
        self._draw_round_rect(
            canvas,
            9,
            9,
            width - 9,
            height - 9,
            14,
            fill=style["content_bg"],
            outline="",
        )
        canvas.create_text(
            34,
            height / 2,
            text=style["icon"],
            font=(EMOJI_FONT_FAMILY, 22),
            fill=style["title_fg"],
        )
        canvas.create_text(
            68,
            30,
            text=chapter.get("title", f"第{chapter_idx + 1}幕"),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["chapter_title"], "bold"),
            fill=style["title_fg"],
        )
        canvas.create_text(
            68,
            58,
            text=chapter.get("subtitle", ""),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["chapter_subtitle"]),
            fill=style["subtitle_fg"],
            width=width - 118,
        )
        canvas.create_text(
            width - 38,
            height / 2,
            text=f"{chapter_idx + 1:02d}",
            font=(FONT_FAMILY, 14, "bold"),
            fill=style["muted_fg"],
        )

        self.chapter_toast_win = win
        self.chapter_toast_after_id = self.root.after(
            style["duration"],
            self._destroy_chapter_toast,
        )

    def _destroy_chapter_toast(self):
        if self.chapter_toast_after_id is not None:
            try:
                self.root.after_cancel(self.chapter_toast_after_id)
            except tk.TclError:
                pass
            self.chapter_toast_after_id = None
        if self.chapter_toast_win is not None:
            try:
                self.chapter_toast_win.destroy()
            except tk.TclError:
                pass
        self.chapter_toast_win = None

    def generate_heart_points(self):
        points = []
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        for angle in range(0, 360, HEART_STEP):
            rad = angle * math.pi / 180
            x = center_x + self.heart_scale * 16 * (math.sin(rad) ** 3)
            y = center_y - self.heart_scale * (
                13 * math.cos(rad) - 5 * math.cos(2*rad)
                - 2 * math.cos(3*rad) - math.cos(4*rad)
            )
            points.append((int(x), int(y)))
        return points

    def spawn_heart_step(self):
        if self.current_step < len(self.heart_points):
            x, y = self.heart_points[self.current_step]
            win_x = max(0, min(x - WINDOW_WIDTH // 2, self.screen_width - WINDOW_WIDTH))
            win_y = max(0, min(y - WINDOW_HEIGHT // 2, self.screen_height - WINDOW_HEIGHT))
            self.create_popup(win_x, win_y)
            self.current_step += 1
            self.after_id = self.root.after(HEART_SPEED, self.spawn_heart_step)
        else:
            self.after_id = self.root.after(HEART_STAY, self.close_all_heart_windows)

    def close_all_heart_windows(self):
        self.cleanup()
        self.random_step_count = 0
        self.spawn_random_step()

    def spawn_random_step(self):
        if self.random_step_count < RANDOM_COUNT:
            x = random.randint(0, self.screen_width - WINDOW_WIDTH)
            y = random.randint(0, self.screen_height - WINDOW_HEIGHT)
            self.create_popup(x, y)
            self.random_step_count += 1
            self.after_id = self.root.after(RANDOM_SPEED, self.spawn_random_step)
        else:
            # 满屏弹窗结束后，先给对方一个轻互动选择
            self.after_id = self.root.after(1000, self.show_interaction_choice)

    def show_interaction_choice(self):
        self.after_id = None
        style = INTERACTION_CHOICE_STYLE
        choices = [choice for choice in INTERACTION_CHOICES if choice.get("label")]
        if not style.get("enabled", True) or not choices:
            self.show_memory_cards()
            return

        self._destroy_interaction_choice()

        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2

        choice_win = tk.Toplevel(self.root)
        choice_win.overrideredirect(True)
        choice_win.geometry(f"{width}x{height}+{x}+{y}")
        choice_win.attributes("-topmost", True)
        choice_win.config(bg=style["outer_bg"])
        choice_win.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())
        choice_win.protocol("WM_DELETE_WINDOW", lambda: None)

        outer_frame = tk.Frame(choice_win, bg=style["outer_bg"], bd=0)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        middle_frame = tk.Frame(outer_frame, bg=style["middle_bg"], bd=0)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        inner_frame = tk.Frame(middle_frame, bg=style["content_bg"], bd=0)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        header_frame = tk.Frame(inner_frame, bg=style["content_bg"], bd=0)
        header_frame.pack(fill=tk.X, padx=SPACING["lg"], pady=(SPACING["lg"], 0))
        icon_label = tk.Label(
            header_frame,
            text=style["icon"],
            bg=style["content_bg"],
            fg=style["title_fg"],
            font=(EMOJI_FONT_FAMILY, 26),
        )
        icon_label.pack(side=tk.LEFT)

        title_box = tk.Frame(header_frame, bg=style["content_bg"], bd=0)
        title_box.pack(side=tk.LEFT, padx=(SPACING["sm"], 0), fill=tk.X, expand=True)
        title_label = tk.Label(
            title_box,
            text=style["title"],
            bg=style["content_bg"],
            fg=style["title_fg"],
            font=(FONT_FAMILY, FONT_SIZES["choice_title"], "bold"),
            anchor="w",
        )
        title_label.pack(fill=tk.X)
        subtitle_label = tk.Label(
            title_box,
            text=style["subtitle"],
            bg=style["content_bg"],
            fg=style["body_fg"],
            font=(FONT_FAMILY, FONT_SIZES["choice_body"]),
            anchor="w",
            wraplength=style["width"] - 110,
        )
        subtitle_label.pack(fill=tk.X, pady=(2, 0))

        separator = tk.Frame(inner_frame, bg=style["middle_bg"], height=1)
        separator.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["md"])

        button_frame = tk.Frame(inner_frame, bg=style["content_bg"], bd=0)
        button_frame.pack(fill=tk.X, padx=SPACING["xl"])

        def choose(choice):
            self.interaction_choice = choice.get("label", "")
            self.interaction_reply = choice.get("reply", "")
            self._destroy_interaction_choice()
            self.after_id = self.root.after(180, self.show_memory_cards)

        for idx, choice in enumerate(choices[:3]):
            button_bg = (
                style["button_bg"] if idx == 0 else style["button_alt_bg"]
            )
            btn = tk.Button(
                button_frame,
                text=choice["label"],
                font=(FONT_FAMILY, FONT_SIZES["choice_button"], "bold"),
                bg=button_bg,
                fg=style["button_fg"],
                activebackground=style["button_active_bg"],
                activeforeground=style["button_fg"],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda data=choice: choose(data),
            )
            btn.pack(fill=tk.X, pady=(0, SPACING["sm"]), ipady=5)

        footer_label = tk.Label(
            inner_frame,
            text=style["footer"],
            bg=style["content_bg"],
            fg=style["muted_fg"],
            font=(FONT_FAMILY, 9),
            wraplength=style["width"] - 72,
        )
        footer_label.pack(pady=(SPACING["xs"], SPACING["sm"]))

        choice_win.bind("<Return>", lambda e: choose(choices[0]))
        self.interaction_win = choice_win
        try:
            choice_win.lift()
        except tk.TclError:
            pass

    def _destroy_interaction_choice(self):
        if self.interaction_win is not None:
            try:
                self.interaction_win.destroy()
            except tk.TclError:
                pass
        self.interaction_win = None

    def show_memory_cards(self):
        self.after_id = None
        style = MEMORY_CARD_STYLE
        cards = [card for card in MEMORY_CARDS if card.get("title") or card.get("text")]
        if not style.get("enabled", True) or not cards:
            self.show_exit_dialog()
            return

        self._destroy_memory_cards()
        self.memory_cards = cards[:5]
        self.memory_idx = 0

        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2

        memory_win = tk.Toplevel(self.root)
        memory_win.overrideredirect(True)
        memory_win.geometry(f"{width}x{height}+{x}+{y}")
        memory_win.attributes("-topmost", True)
        memory_win.config(bg=style["outer_bg"])
        memory_win.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())
        memory_win.protocol("WM_DELETE_WINDOW", lambda: None)

        canvas = tk.Canvas(
            memory_win,
            width=width,
            height=height,
            bg=style["outer_bg"],
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self.memory_win = memory_win
        self.memory_canvas = canvas
        self._render_memory_card()

    def _render_memory_card(self):
        if self.memory_canvas is None or self.memory_win is None:
            return

        if self.memory_idx >= len(self.memory_cards):
            self._destroy_memory_cards()
            self.show_exit_dialog()
            return

        style = MEMORY_CARD_STYLE
        card = self.memory_cards[self.memory_idx]
        canvas = self.memory_canvas
        width, height = style["width"], style["height"]
        canvas.delete("all")

        self._draw_round_rect(
            canvas,
            4,
            4,
            width - 4,
            height - 4,
            24,
            fill=style["outer_bg"],
            outline="",
        )
        self._draw_round_rect(
            canvas,
            11,
            11,
            width - 11,
            height - 11,
            20,
            fill=style["middle_bg"],
            outline="",
        )
        self._draw_round_rect(
            canvas,
            18,
            18,
            width - 18,
            height - 18,
            17,
            fill=style["content_bg"],
            outline="",
        )
        canvas.create_oval(
            -56,
            -64,
            180,
            156,
            fill=style["content_bg_alt"],
            outline="",
        )
        canvas.create_oval(
            width - 170,
            height - 140,
            width + 64,
            height + 70,
            fill=style["content_bg_alt"],
            outline="",
        )

        canvas.create_text(
            42,
            42,
            text=style["eyebrow"],
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["memory_eyebrow"], "bold"),
            fill=style["muted_fg"],
        )
        canvas.create_text(
            width - 44,
            45,
            text=f"{self.memory_idx + 1}/{len(self.memory_cards)}",
            anchor="e",
            font=(FONT_FAMILY, FONT_SIZES["memory_date"], "bold"),
            fill=style["muted_fg"],
        )
        canvas.create_line(
            42,
            68,
            width - 42,
            68,
            fill=style["middle_bg"],
            width=1,
        )

        canvas.create_text(
            68,
            112,
            text=card.get("icon", "💗"),
            font=(EMOJI_FONT_FAMILY, 34),
            fill=style["icon_fg"],
        )
        canvas.create_text(
            112,
            96,
            text=card.get("date", ""),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["memory_date"], "bold"),
            fill=style["muted_fg"],
        )
        canvas.create_text(
            112,
            130,
            text=card.get("title", ""),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["memory_title"], "bold"),
            fill=style["title_fg"],
            width=width - 154,
        )
        canvas.create_text(
            width / 2,
            194,
            text=card.get("text", ""),
            font=(FONT_FAMILY, FONT_SIZES["memory_body"], "bold"),
            fill=style["body_fg"],
            width=width - 92,
            justify="center",
        )
        canvas.create_line(
            132,
            height - 50,
            width - 132,
            height - 50,
            fill=style["decor_fg"],
            width=1,
        )
        canvas.create_text(
            width / 2,
            height - 30,
            text=style["footer"],
            font=(FONT_FAMILY, FONT_SIZES["memory_footer"]),
            fill=style["muted_fg"],
        )

        self.memory_idx += 1
        self.memory_after_id = self.root.after(
            style["card_duration"],
            self._render_memory_card,
        )

    def _destroy_memory_cards(self):
        if self.memory_after_id is not None:
            try:
                self.root.after_cancel(self.memory_after_id)
            except tk.TclError:
                pass
            self.memory_after_id = None
        if self.memory_win is not None:
            try:
                self.memory_win.destroy()
            except tk.TclError:
                pass
        self.memory_win = None
        self.memory_canvas = None

    def _shake_window(self, win, base_x, base_y, step=0):
        style = EXIT_DIALOG_STYLE
        total_steps = style["shake_steps"]
        if step >= total_steps:
            try:
                win.geometry(f"+{base_x}+{base_y}")
            except tk.TclError:
                pass
            return

        direction = -1 if step % 2 == 0 else 1
        distance = int(style["shake_distance"] * (1 - step / total_steps))
        try:
            win.geometry(f"+{base_x + direction * distance}+{base_y}")
            self.root.after(
                style["shake_interval"],
                lambda: self._shake_window(win, base_x, base_y, step + 1),
            )
        except tk.TclError:
            pass

    def show_exit_dialog(self):
        self.after_id = None

        # 1. 创建最顶层的无边框退出验证窗口
        style = EXIT_DIALOG_STYLE
        exit_win = tk.Toplevel(self.root)
        exit_win.overrideredirect(True)
        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        exit_win.geometry(f"{width}x{height}+{x}+{y}")
        exit_win.attributes("-topmost", True)
        exit_win.config(bg=style["outer_bg"])

        # 2. UI 样式：签收礼盒/回执卡
        outer_frame = tk.Frame(exit_win, bg=style["outer_bg"], bd=0)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        middle_frame = tk.Frame(outer_frame, bg=style["middle_bg"], bd=0)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        inner_frame = tk.Frame(middle_frame, bg=style["content_bg"], bd=0)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        header_frame = tk.Frame(inner_frame, bg=style["content_bg"], bd=0)
        header_frame.pack(fill=tk.X, padx=SPACING["lg"], pady=(SPACING["md"], 0))

        gift_label = tk.Label(
            header_frame,
            text="💌",
            bg=style["content_bg"],
            fg=style["title_fg"],
            font=(EMOJI_FONT_FAMILY, 22),
        )
        gift_label.pack(side=tk.LEFT)

        title_box = tk.Frame(header_frame, bg=style["content_bg"], bd=0)
        title_box.pack(side=tk.LEFT, padx=(SPACING["sm"], 0), fill=tk.X, expand=True)
        title_label = tk.Label(
            title_box,
            text="甜蜜签收单",
            bg=style["content_bg"],
            fg=style["title_fg"],
            font=(FONT_FAMILY, FONT_SIZES["dialog_title"], "bold"),
            anchor="w",
        )
        title_label.pack(fill=tk.X)
        receipt_label = tk.Label(
            title_box,
            text="LOVE DELIVERY · 520",
            bg=style["content_bg"],
            fg=style["muted_fg"],
            font=(FONT_FAMILY, 8, "bold"),
            anchor="w",
        )
        receipt_label.pack(fill=tk.X)

        stamp_label = tk.Label(
            header_frame,
            text="已送达",
            bg=style["button_bg"],
            fg=style["button_fg"],
            font=(FONT_FAMILY, 9, "bold"),
            padx=8,
            pady=3,
        )
        stamp_label.pack(side=tk.RIGHT)

        separator = tk.Frame(inner_frame, bg=style["middle_bg"], height=1)
        separator.pack(fill=tk.X, padx=SPACING["lg"], pady=(SPACING["sm"], SPACING["md"]))

        # 提示文本
        hint_text = EXIT_DIALOG_HINT.replace("{nickname}", NICKNAME)
        if self.interaction_reply:
            hint_text = f"{self.interaction_reply}\n{hint_text}"
        lbl = tk.Label(
            inner_frame,
            text=hint_text,
            bg=style["content_bg"],
            fg=style["hint_fg"],
            font=(FONT_FAMILY, FONT_SIZES["dialog_hint"], "bold"),
            justify="center",
            wraplength=width - 72,
        )
        lbl.pack(fill=tk.X, padx=SPACING["lg"], pady=(0, SPACING["sm"]))

        entry_shell = tk.Frame(inner_frame, bg=style["middle_bg"], bd=0)
        entry_shell.pack(padx=SPACING["xl"], pady=(0, SPACING["sm"]), fill=tk.X)
        entry = tk.Entry(
            entry_shell,
            font=(FONT_FAMILY, FONT_SIZES["dialog_input"], "bold"),
            justify="center",
            width=16,
            bd=0,
            relief=tk.FLAT,
            bg=style["entry_bg"],
            fg=style["entry_fg"],
            insertbackground=style["title_fg"],
        )
        entry.pack(fill=tk.X, padx=2, pady=2, ipady=5)
        entry.focus_set()

        # 4. 校验密码逻辑
        def check_password(event=None):
            if self.stamp_running:
                return
            pwd = entry.get().strip()
            if pwd in ALL_PASSWORDS:
                btn.config(text="签收成功", bg=style["button_active_bg"])
                entry.config(state=tk.DISABLED)
                btn.config(state=tk.DISABLED, cursor="arrow")
                self.show_stamp_signoff(exit_win)
            else:
                lbl.config(text="口令不对哦，再试一次嘛~", fg=style["error_fg"])
                entry.delete(0, tk.END)
                self._shake_window(exit_win, x, y)

        action_frame = tk.Frame(inner_frame, bg=style["content_bg"], bd=0)
        action_frame.pack(fill=tk.X, padx=SPACING["xl"])
        btn = tk.Button(
            action_frame,
            text="确认查收",
            font=(FONT_FAMILY, FONT_SIZES["dialog_button"], "bold"),
            bg=style["button_bg"],
            fg=style["button_fg"],
            activebackground=style["button_active_bg"],
            activeforeground=style["button_fg"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=check_password,
        )
        btn.pack(fill=tk.X, ipady=5)

        footer_label = tk.Label(
            inner_frame,
            text="♡ 专属爱意回执 ♡",
            bg=style["content_bg"],
            fg=style["muted_fg"],
            font=(FONT_FAMILY, 9),
        )
        footer_label.pack(pady=(SPACING["sm"], 0))

        # 绑定回车键可以快捷确认
        exit_win.bind("<Return>", check_password)

        # 禁用常规的强杀
        exit_win.protocol("WM_DELETE_WINDOW", lambda: None)
        try:
            exit_win.lift()
        except tk.TclError:
            pass

    def show_stamp_signoff(self, exit_win):
        style = STAMP_SIGNOFF_STYLE
        if not style.get("enabled", True):
            self.trigger_blackhole_animation(exit_win)
            return

        self._destroy_stamp_signoff()
        self.stamp_running = True

        width, height = style["width"], style["height"]
        try:
            base_x = exit_win.winfo_x() + (exit_win.winfo_width() - width) // 2
            base_y = exit_win.winfo_y() + (exit_win.winfo_height() - height) // 2
        except tk.TclError:
            self.trigger_blackhole_animation(exit_win)
            return

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"{width}x{height}+{base_x}+{base_y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", style["alpha"])
        trans_color = style["transparent_bg"]
        win.config(bg=trans_color)
        try:
            win.attributes("-transparentcolor", trans_color)
        except tk.TclError:
            pass
        win.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())

        canvas = tk.Canvas(
            win,
            width=width,
            height=height,
            bg=trans_color,
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self.stamp_win = win
        self.stamp_canvas = canvas
        self._animate_stamp_signoff(exit_win, 0)

    def _animate_stamp_signoff(self, exit_win, frame):
        if self.stamp_canvas is None or self.stamp_win is None:
            return

        style = STAMP_SIGNOFF_STYLE
        total = max(1, style["duration_frames"])
        if frame >= total:
            self._destroy_stamp_signoff()
            self.trigger_blackhole_animation(exit_win)
            return

        canvas = self.stamp_canvas
        width, height = style["width"], style["height"]
        canvas.delete("all")

        progress = frame / total
        drop = max(0.0, 1.0 - progress * 2.2)
        pulse = math.sin(progress * math.pi * 3)
        cx = width / 2
        cy = height / 2 + drop * 34
        scale = 0.72 + min(1.0, progress * 2.0) * 0.28 + pulse * 0.035
        rx = 78 * scale
        ry = 42 * scale

        canvas.create_oval(
            cx - rx,
            cy - ry,
            cx + rx,
            cy + ry,
            fill=style["stamp_bg"],
            outline=style["ring"],
            width=4,
        )
        canvas.create_oval(
            cx - rx + 10,
            cy - ry + 8,
            cx + rx - 10,
            cy + ry - 8,
            outline=style["ring_alt"],
            width=2,
        )
        canvas.create_line(
            cx - rx + 22,
            cy,
            cx + rx - 22,
            cy,
            fill=style["ring"],
            width=2,
        )
        canvas.create_text(
            cx,
            cy - 9,
            text=style["text"],
            font=(FONT_FAMILY, FONT_SIZES["stamp_text"], "bold"),
            fill=style["stamp_fg"],
        )
        canvas.create_text(
            cx,
            cy + 27,
            text=style["caption"],
            font=(FONT_FAMILY, FONT_SIZES["stamp_caption"], "bold"),
            fill=style["stamp_fg"],
        )

        self.stamp_after_id = self.root.after(
            style["frame_interval"],
            lambda: self._animate_stamp_signoff(exit_win, frame + 1),
        )

    def _destroy_stamp_signoff(self):
        self.stamp_running = False
        if self.stamp_after_id is not None:
            try:
                self.root.after_cancel(self.stamp_after_id)
            except tk.TclError:
                pass
            self.stamp_after_id = None
        if self.stamp_win is not None:
            try:
                self.stamp_win.destroy()
            except tk.TclError:
                pass
        self.stamp_win = None
        self.stamp_canvas = None

    def _show_blackhole_center(self, center_x, center_y):
        self._destroy_blackhole_center()

        style = BLACKHOLE_STYLE
        size = style["size"]
        caption_height = 30
        total_height = size + caption_height
        trans_color = "#010101"

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.94)
        win.config(bg=trans_color)
        try:
            win.attributes("-transparentcolor", trans_color)
        except tk.TclError:
            pass

        x = center_x - size // 2
        y = center_y - total_height // 2
        win.geometry(f"{size}x{total_height}+{x}+{y}")

        canvas = tk.Canvas(
            win,
            width=size,
            height=total_height,
            bg=trans_color,
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self.blackhole_win = win
        self.blackhole_canvas = canvas
        self.blackhole_running = True
        self.blackhole_pulse = 0
        self._animate_blackhole_center()

    def _animate_blackhole_center(self):
        if not self.blackhole_running or self.blackhole_canvas is None:
            return

        style = BLACKHOLE_STYLE
        size = style["size"]
        cx = size // 2
        cy = size // 2
        tick = self.blackhole_pulse

        try:
            canvas = self.blackhole_canvas
            canvas.delete("all")

            pulse = math.sin(tick * 0.45)
            outer_r = 64 + pulse * 5
            middle_r = 48 - pulse * 3
            core_r = 31 + pulse * 2

            canvas.create_oval(
                cx - outer_r,
                cy - outer_r,
                cx + outer_r,
                cy + outer_r,
                outline=style["ring_alt"],
                width=2,
            )
            canvas.create_oval(
                cx - middle_r,
                cy - middle_r,
                cx + middle_r,
                cy + middle_r,
                outline=style["ring"],
                width=3,
            )
            canvas.create_oval(
                cx - core_r,
                cy - core_r,
                cx + core_r,
                cy + core_r,
                fill=style["bg"],
                outline=style["ring"],
                width=2,
            )

            for i in range(10):
                angle = tick * 0.22 + i * math.pi * 0.4
                radius = 54 - (i % 3) * 8
                dot_x = cx + math.cos(angle) * radius
                dot_y = cy + math.sin(angle) * radius
                dot_size = 3 + (i % 2)
                color = style["ring"] if i % 2 == 0 else style["ring_alt"]
                canvas.create_oval(
                    dot_x - dot_size,
                    dot_y - dot_size,
                    dot_x + dot_size,
                    dot_y + dot_size,
                    fill=color,
                    outline="",
                )

            canvas.create_text(
                cx,
                cy - 2,
                text=style["heart"],
                font=(EMOJI_FONT_FAMILY, 34),
                fill=style["heart_fg"],
            )
            canvas.create_text(
                cx,
                size + 14,
                text=style["caption"],
                font=(FONT_FAMILY, 8, "bold"),
                fill=style["caption_fg"],
                width=size - 8,
                justify="center",
            )
        except tk.TclError:
            return

        self.blackhole_pulse += 1
        self.root.after(style["pulse_interval"], self._animate_blackhole_center)

    def _destroy_blackhole_center(self):
        self.blackhole_running = False
        if self.blackhole_win is not None:
            try:
                self.blackhole_win.destroy()
            except tk.TclError:
                pass
        self.blackhole_win = None
        self.blackhole_canvas = None

    def trigger_blackhole_animation(self, exit_win):
        exit_win.destroy()

        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        items = []
        for win in self.all_windows:
            if not win.winfo_exists():
                continue
            try:
                win.attributes("-topmost", True)
                win.attributes("-alpha", 1.0)
                win.lift()
            except tk.TclError:
                continue
            x = win.winfo_x() + WINDOW_WIDTH // 2
            y = win.winfo_y() + WINDOW_HEIGHT // 2
            dist = math.hypot(x - center_x, y - center_y)
            items.append((win, x, y, dist))

        self._show_blackhole_center(center_x, center_y)
        items.sort(key=lambda d: -d[3])

        self.waves = []
        style = BLACKHOLE_STYLE
        batch_size = style["batch_size"]

        for i, (win, sx, sy, dist) in enumerate(items):
            wave_idx = i // batch_size
            total_frames = random.randint(style["min_frames"], style["max_frames"])
            spin = random.choice([-1, 1]) * random.uniform(
                style["spin_min"],
                style["spin_max"],
            )

            self.waves.append({
                "win": win,
                "sx": float(sx),
                "sy": float(sy),
                "dist": dist,
                "frame": 0,
                "total_frames": total_frames,
                "spin": spin,
                "wave": wave_idx,
                "started": False,
            })

        self.wave_released = 0
        self.bh_center_x = center_x
        self.bh_center_y = center_y
        self.release_next_wave()

    def release_next_wave(self):
        for data in self.waves:
            if data["wave"] == self.wave_released:
                data["started"] = True
        self.wave_released += 1

        has_more = any(not d["started"] for d in self.waves)
        if has_more:
            self.root.after(BLACKHOLE_STYLE["release_interval"], self.release_next_wave)

        if self.wave_released == 1:
            self.blackhole_step()

    def blackhole_step(self):
        active = []
        cx = self.bh_center_x
        cy = self.bh_center_y

        for data in self.waves:
            if not data["started"]:
                active.append(data)
                continue

            data["frame"] += 1
            t = data["frame"] / data["total_frames"]

            if t >= 1.0:
                try:
                    data["win"].destroy()
                except tk.TclError:
                    pass
                continue

            ease = t * t * (3 - 2 * t)
            nx = data["sx"] + (cx - data["sx"]) * ease
            ny = data["sy"] + (cy - data["sy"]) * ease

            remaining_ratio = 1.0 - ease
            offset = math.sin(t * math.pi * 2.5) * data["dist"] * data["spin"] * remaining_ratio
            dx = cx - data["sx"]
            dy = cy - data["sy"]
            length = data["dist"] if data["dist"] > 0 else 1
            perp_x = -dy / length
            perp_y = dx / length
            nx += offset * perp_x
            ny += offset * perp_y

            win_x = int(nx - WINDOW_WIDTH // 2)
            win_y = int(ny - WINDOW_HEIGHT // 2)

            try:
                data["win"].geometry(f"+{win_x}+{win_y}")
                if t > BLACKHOLE_STYLE["cover_start"] and self.blackhole_win is not None:
                    data["win"].lower(self.blackhole_win)
                active.append(data)
            except tk.TclError:
                pass

        self.waves = active
        if self.blackhole_win is not None:
            try:
                self.blackhole_win.lift()
            except tk.TclError:
                pass

        if self.waves:
            self.root.after(BLACKHOLE_STYLE["frame_interval"], self.blackhole_step)
        else:
            self.cleanup()
            self.show_transition_burst()

    def show_transition_burst(self):
        style = TRANSITION_BURST_STYLE
        if not style.get("enabled", True):
            self.show_final_message()
            return

        self._destroy_transition_burst()

        size = style["size"]
        x = (self.screen_width - size) // 2
        y = (self.screen_height - size) // 2
        trans_color = style["transparent_bg"]

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"{size}x{size}+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", style["alpha"])
        win.config(bg=trans_color)
        try:
            win.attributes("-transparentcolor", trans_color)
        except tk.TclError:
            pass
        win.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())

        canvas = tk.Canvas(
            win,
            width=size,
            height=size,
            bg=trans_color,
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self.transition_burst_win = win
        self.transition_burst_canvas = canvas
        self._animate_transition_burst(0)

    def _animate_transition_burst(self, frame):
        if self.transition_burst_canvas is None or self.transition_burst_win is None:
            return

        style = TRANSITION_BURST_STYLE
        total = max(1, style["duration_frames"])
        if frame >= total:
            self._destroy_transition_burst()
            self.show_final_message()
            return

        size = style["size"]
        canvas = self.transition_burst_canvas
        canvas.delete("all")

        progress = frame / total
        cx = size / 2
        cy = size / 2
        fade = max(0.0, 1.0 - progress)

        for i, base_radius in enumerate((34, 62, 92)):
            radius = base_radius + progress * (76 + i * 26)
            color = style["ring"] if i % 2 == 0 else style["ring_alt"]
            width = max(1, int(5 * fade) + 1)
            canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                outline=color,
                width=width,
            )

        spark_colors = style["spark_colors"] or [style["ring"]]
        for i in range(18):
            angle = i * math.pi * 2 / 18 + progress * 1.4
            distance = 22 + progress * (96 + (i % 3) * 18)
            spark_x = cx + math.cos(angle) * distance
            spark_y = cy + math.sin(angle) * distance
            spark_size = max(2, int((7 - (i % 3)) * fade) + 1)
            canvas.create_oval(
                spark_x - spark_size,
                spark_y - spark_size,
                spark_x + spark_size,
                spark_y + spark_size,
                fill=spark_colors[i % len(spark_colors)],
                outline="",
            )

        heart_size = FONT_SIZES["burst_heart"] + int(math.sin(progress * math.pi) * 8)
        canvas.create_text(
            cx,
            cy - 10,
            text=style["heart"],
            font=(EMOJI_FONT_FAMILY, heart_size),
            fill=style["ring"],
        )
        canvas.create_text(
            cx,
            cy + 44,
            text=style["caption"],
            font=(FONT_FAMILY, FONT_SIZES["burst_caption"], "bold"),
            fill=style["caption_fg"],
        )

        self.transition_burst_after_id = self.root.after(
            style["frame_interval"],
            lambda: self._animate_transition_burst(frame + 1),
        )

    def _destroy_transition_burst(self):
        if self.transition_burst_after_id is not None:
            try:
                self.root.after_cancel(self.transition_burst_after_id)
            except tk.TclError:
                pass
            self.transition_burst_after_id = None
        if self.transition_burst_win is not None:
            try:
                self.transition_burst_win.destroy()
            except tk.TclError:
                pass
        self.transition_burst_win = None
        self.transition_burst_canvas = None

    def show_final_message(self):
        # ---------- 飘落爱心粒子（每个粒子是一个小透明窗口） ----------
        self.particle_windows = []
        self.particle_data = []
        self.particle_running = True

        for _ in range(PARTICLE_COUNT):
            x = random.randint(0, self.screen_width - 40)
            y = random.randint(-self.screen_height, -40)
            heart = random.choice(PARTICLE_HEARTS)
            color = random.choice(PARTICLE_COLORS)
            size = random.randint(14, 32)

            pw = tk.Toplevel(self.root)
            pw.overrideredirect(True)
            pw.attributes("-topmost", True)
            pw.attributes("-alpha", random.uniform(0.6, 0.95))
            trans_color = "#010101"
            pw.config(bg=trans_color)
            pw.attributes("-transparentcolor", trans_color)
            win_size = size + 24
            pw.geometry(f"{win_size}x{win_size}+{x}+{y}")

            lbl = tk.Label(pw, text=heart, font=("Segoe UI Emoji", size),
                           fg=color, bg=trans_color)
            lbl.place(relx=0.5, rely=0.5, anchor="center")

            self.particle_windows.append(pw)
            self.particle_data.append({
                "win": pw,
                "x": float(x),
                "y": float(y),
                "speed_y": random.uniform(1.5, 5.5),
                "speed_x": random.uniform(-1.2, 1.2),
                "swing_amp": random.uniform(0.8, 2.5),
                "swing_freq": random.uniform(0.02, 0.08),
                "tick": 0,
            })

        # 分两组交替更新以减少每帧系统调用
        self._particle_group = 0
        self._animate_particles()

        # ---------- 打字机文字窗口 ----------
        style = FINAL_SCENE_STYLE
        self.final_win = tk.Toplevel(self.root)
        self.final_win.overrideredirect(True)
        self.final_win.attributes("-topmost", True)

        final_width, final_height = style["width"], style["height"]
        fx = (self.screen_width - final_width) // 2
        fy = (self.screen_height - final_height) // 2
        self.final_win.geometry(f"{final_width}x{final_height}+{fx}+{fy}")
        self.final_win.config(bg=style["outer_bg"])

        outer_frame = tk.Frame(self.final_win, bg=style["outer_bg"], bd=0)
        outer_frame.pack(fill=tk.BOTH, expand=True)
        middle_frame = tk.Frame(outer_frame, bg=style["middle_bg"], bd=0)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        scene_canvas = tk.Canvas(
            middle_frame,
            width=final_width - 8,
            height=final_height - 8,
            bg=style["content_bg"],
            bd=0,
            highlightthickness=0,
        )
        scene_canvas.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        canvas_w = final_width - 14
        canvas_h = final_height - 14
        scene_canvas.create_rectangle(
            0,
            0,
            canvas_w,
            canvas_h,
            fill=style["content_bg"],
            outline="",
        )
        scene_canvas.create_oval(
            -50,
            -65,
            220,
            180,
            fill=style["content_bg_alt"],
            outline="",
        )
        scene_canvas.create_oval(
            canvas_w - 180,
            canvas_h - 155,
            canvas_w + 90,
            canvas_h + 90,
            fill=style["content_bg_alt"],
            outline="",
        )
        for i, x_pos in enumerate(range(70, canvas_w, 92)):
            dot_y = 48 + (i % 2) * 12
            scene_canvas.create_oval(
                x_pos,
                dot_y,
                x_pos + 3,
                dot_y + 3,
                fill=style["decor_fg"],
                outline="",
            )
        scene_canvas.create_text(
            32,
            30,
            text="LOVE LETTER · 520",
            anchor="w",
            font=(FONT_FAMILY, 9, "bold"),
            fill=style["muted_fg"],
        )
        scene_canvas.create_text(
            canvas_w - 42,
            32,
            text="💖",
            font=(EMOJI_FONT_FAMILY, FONT_SIZES["final_decor"]),
            fill=style["decor_fg"],
        )
        scene_canvas.create_line(
            34,
            58,
            canvas_w - 34,
            58,
            fill=style["muted_fg"],
            width=1,
        )
        scene_canvas.create_text(
            canvas_w / 2,
            82,
            text="💗 · 💕 · 💗",
            font=(EMOJI_FONT_FAMILY, FONT_SIZES["final_decor"]),
            fill=style["decor_fg"],
        )

        self.typewriter_label1 = tk.Label(
            scene_canvas,
            text="",
            font=(FONT_FAMILY, FONT_SIZES["final_line1"], "bold"),
            fg=style["line1_fg"],
            bg=style["content_bg"],
            justify="center",
            wraplength=final_width - 96,
        )
        scene_canvas.create_window(
            canvas_w / 2,
            138,
            window=self.typewriter_label1,
            width=final_width - 90,
        )

        self.typewriter_label2 = tk.Label(
            scene_canvas,
            text="",
            font=(FONT_FAMILY, FONT_SIZES["final_line2"], "bold"),
            fg=style["line2_fg"],
            bg=style["content_bg"],
            justify="center",
            wraplength=final_width - 96,
        )
        scene_canvas.create_window(
            canvas_w / 2,
            190,
            window=self.typewriter_label2,
            width=final_width - 90,
        )
        scene_canvas.create_line(
            124,
            canvas_h - 34,
            canvas_w - 124,
            canvas_h - 34,
            fill=style["decor_fg"],
            width=1,
        )
        scene_canvas.create_text(
            canvas_w / 2,
            canvas_h - 18,
            text="FOREVER AND ALWAYS",
            font=(FONT_FAMILY, 8, "bold"),
            fill=style["muted_fg"],
        )

        # 打字机文本队列（使用配置中的文本，替换昵称占位符）
        line1 = FINAL_LINE_1
        line2 = FINAL_LINE_2.replace("{nickname}", NICKNAME)
        self.typewriter_lines = [
            (self.typewriter_label1, line1),
            (self.typewriter_label2, line2),
        ]
        self.typewriter_displayed = ["", ""]
        self.typewriter_line_idx = 0
        self.typewriter_char_idx = 0
        self.typewriter_cursor_line_idx = 0
        self.typewriter_cursor_visible = True
        self.typewriter_cursor_running = True
        self._blink_typewriter_cursor()
        self._typewriter_step()

    def _animate_particles(self):
        """每帧移动一半粒子窗口，两组交替更新，降低单帧开销"""
        if not self.particle_running:
            return

        group = self._particle_group
        self._particle_group = 1 - group

        for i, p in enumerate(self.particle_data):
            p["tick"] += 1
            p["y"] += p["speed_y"]
            swing = p["swing_amp"] * math.sin(p["tick"] * p["swing_freq"])
            p["x"] += p["speed_x"] + swing * 0.3

            if p["y"] > self.screen_height + 40:
                p["y"] = random.uniform(-80, -40)
                p["x"] = random.randint(0, self.screen_width - 40)
                p["tick"] = 0

            if i % 2 == group:
                try:
                    p["win"].geometry(f"+{int(p['x'])}+{int(p['y'])}")
                except tk.TclError:
                    pass

        self.root.after(25, self._animate_particles)

    def _render_typewriter_lines(self):
        cursor = FINAL_SCENE_STYLE["cursor"]
        for idx, (label, _) in enumerate(self.typewriter_lines):
            text = self.typewriter_displayed[idx]
            if (
                self.typewriter_cursor_running
                and idx == self.typewriter_cursor_line_idx
                and self.typewriter_cursor_visible
            ):
                text += cursor
            try:
                label.config(text=text)
            except tk.TclError:
                pass

    def _blink_typewriter_cursor(self):
        if not self.typewriter_cursor_running:
            return
        self.typewriter_cursor_visible = not self.typewriter_cursor_visible
        self._render_typewriter_lines()
        self.root.after(
            FINAL_SCENE_STYLE["cursor_blink_interval"],
            self._blink_typewriter_cursor,
        )

    def _typewriter_step(self):
        """逐字显示文本，一行完成后进入下一行"""
        if self.typewriter_line_idx >= len(self.typewriter_lines):
            self.typewriter_cursor_running = False
            self._render_typewriter_lines()
            if (
                KEEPSAKE_RECEIPT.get("enabled", True)
                and KEEPSAKE_RECEIPT_STYLE.get("enabled", True)
            ):
                delay = KEEPSAKE_RECEIPT_STYLE["delay_after_typewriter"]
                self.keepsake_after_id = self.root.after(
                    delay,
                    self.show_keepsake_receipt,
                )
            else:
                self.keepsake_after_id = self.root.after(5000, self._final_exit)
            return

        label, full_text = self.typewriter_lines[self.typewriter_line_idx]
        self.typewriter_char_idx += 1
        displayed = full_text[:self.typewriter_char_idx]
        self.typewriter_displayed[self.typewriter_line_idx] = displayed
        self.typewriter_cursor_line_idx = self.typewriter_line_idx
        self.typewriter_cursor_visible = True
        self._render_typewriter_lines()

        if self.typewriter_char_idx >= len(full_text):
            self.typewriter_line_idx += 1
            self.typewriter_char_idx = 0
            self.root.after(500, self._typewriter_step)
        else:
            self.root.after(100, self._typewriter_step)

    def _receipt_text(self, value):
        choice_text = self.interaction_choice or "每一种都很想你"
        return (
            str(value)
            .replace("{nickname}", NICKNAME)
            .replace("{choice}", choice_text)
        )

    def show_keepsake_receipt(self):
        if not (
            KEEPSAKE_RECEIPT.get("enabled", True)
            and KEEPSAKE_RECEIPT_STYLE.get("enabled", True)
        ):
            self._final_exit()
            return

        self.keepsake_after_id = None
        self._destroy_final_message()
        self._destroy_keepsake_receipt()

        style = KEEPSAKE_RECEIPT_STYLE
        content = KEEPSAKE_RECEIPT
        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2

        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"{width}x{height}+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", style["alpha"])
        win.config(bg=style["outer_bg"])
        win.bind("<Control-Shift-Q>", lambda e: self.emergency_exit())
        win.protocol("WM_DELETE_WINDOW", lambda: None)

        canvas = tk.Canvas(
            win,
            width=width,
            height=height,
            bg=style["outer_bg"],
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        self.keepsake_win = win
        self._draw_keepsake_receipt(canvas, width, height)
        try:
            win.lift()
        except tk.TclError:
            pass

        self.keepsake_after_id = self.root.after(
            style["display_duration"],
            self._final_exit,
        )

    def _draw_keepsake_receipt(self, canvas, width, height):
        style = KEEPSAKE_RECEIPT_STYLE
        content = KEEPSAKE_RECEIPT

        self._draw_round_rect(
            canvas, 4, 4, width - 4, height - 4, 24,
            fill=style["outer_bg"], outline="",
        )
        self._draw_round_rect(
            canvas, 12, 12, width - 12, height - 12, 20,
            fill=style["middle_bg"], outline="",
        )
        self._draw_round_rect(
            canvas, 22, 22, width - 22, height - 22, 17,
            fill=style["content_bg"], outline="",
        )
        canvas.create_oval(
            -70, -72, 190, 164,
            fill=style["content_bg_alt"], outline="",
        )
        canvas.create_oval(
            width - 188, height - 146, width + 70, height + 74,
            fill=style["content_bg_alt"], outline="",
        )

        canvas.create_text(
            54, 58,
            text=style["icon"],
            font=(EMOJI_FONT_FAMILY, 28),
            fill=style["stamp_fg"],
        )
        canvas.create_text(
            92, 48,
            text=self._receipt_text(content["title"]),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["receipt_title"], "bold"),
            fill=style["title_fg"],
        )
        canvas.create_text(
            92, 76,
            text=self._receipt_text(content["subtitle"]),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["receipt_subtitle"], "bold"),
            fill=style["body_fg"],
        )
        canvas.create_text(
            width - 52, 54,
            text=self._receipt_text(content["serial"]),
            anchor="e",
            font=(FONT_FAMILY, FONT_SIZES["receipt_meta"], "bold"),
            fill=style["muted_fg"],
        )
        canvas.create_line(
            50, 102, width - 50, 102,
            fill=style["decor_fg"], width=1,
        )

        meta_lines = [
            ("寄件人", self._receipt_text(content["sender"])),
            ("收件人", self._receipt_text(content["recipient"])),
            ("回执效力", self._receipt_text(content["validity"])),
        ]
        for idx, (label, value) in enumerate(meta_lines):
            y = 132 + idx * 30
            canvas.create_text(
                68, y,
                text=label,
                anchor="w",
                font=(FONT_FAMILY, FONT_SIZES["receipt_meta"], "bold"),
                fill=style["muted_fg"],
            )
            canvas.create_text(
                138, y,
                text=value,
                anchor="w",
                font=(FONT_FAMILY, FONT_SIZES["receipt_item"], "bold"),
                fill=style["body_fg"],
                width=width - 250,
            )

        stamp_x, stamp_y = width - 126, 160
        canvas.create_oval(
            stamp_x - 74, stamp_y - 45,
            stamp_x + 74, stamp_y + 45,
            outline=style["stamp_fg"],
            width=4,
        )
        canvas.create_oval(
            stamp_x - 60, stamp_y - 34,
            stamp_x + 60, stamp_y + 34,
            outline=style["decor_fg"],
            width=2,
        )
        canvas.create_text(
            stamp_x, stamp_y,
            text=style["stamp_text"],
            font=(FONT_FAMILY, FONT_SIZES["receipt_stamp"], "bold"),
            fill=style["stamp_fg"],
        )

        item_top = 232
        item_left = 68
        item_right = width - 68
        self._draw_round_rect(
            canvas, item_left, item_top, item_right, item_top + 92, 12,
            fill="#fff7fb", outline=style["middle_bg"],
        )
        valid_items = [
            item for item in content.get("items", [])
            if len(item) >= 2
        ][:4]
        for idx, (label, value) in enumerate(valid_items):
            col = idx % 2
            row = idx // 2
            base_x = item_left + 26 + col * ((item_right - item_left) / 2)
            base_y = item_top + 28 + row * 38
            canvas.create_text(
                base_x, base_y,
                text=self._receipt_text(label),
                anchor="w",
                font=(FONT_FAMILY, FONT_SIZES["receipt_meta"], "bold"),
                fill=style["muted_fg"],
            )
            canvas.create_text(
                base_x + 74, base_y,
                text=self._receipt_text(value),
                anchor="w",
                font=(FONT_FAMILY, FONT_SIZES["receipt_item"], "bold"),
                fill=style["body_fg"],
                width=(item_right - item_left) / 2 - 110,
            )

        closing_lines = content.get("closing_lines", [])
        for idx, line in enumerate(closing_lines[:2]):
            canvas.create_text(
                width / 2, 348 + idx * 24,
                text=self._receipt_text(line),
                font=(FONT_FAMILY, FONT_SIZES["receipt_closing"], "bold"),
                fill=style["title_fg"] if idx == 0 else style["body_fg"],
                width=width - 100,
                justify="center",
            )
        canvas.create_text(
            width / 2, height - 30,
            text=self._receipt_text(content["footer"]),
            font=(FONT_FAMILY, FONT_SIZES["receipt_footer"], "bold"),
            fill=style["muted_fg"],
        )

    def _destroy_final_message(self):
        self.particle_running = False
        self.typewriter_cursor_running = False
        for pw in self.particle_windows:
            try:
                pw.destroy()
            except tk.TclError:
                pass
        self.particle_windows = []
        self.particle_data = []
        if self.final_win is not None:
            try:
                self.final_win.destroy()
            except tk.TclError:
                pass
        self.final_win = None

    def _destroy_keepsake_receipt(self):
        if self.keepsake_after_id is not None:
            try:
                self.root.after_cancel(self.keepsake_after_id)
            except tk.TclError:
                pass
            self.keepsake_after_id = None
        if self.keepsake_win is not None:
            try:
                self.keepsake_win.destroy()
            except tk.TclError:
                pass
        self.keepsake_win = None

    def _final_exit(self):
        """停止粒子动画，销毁所有窗口，退出程序"""
        self._destroy_final_message()
        self._destroy_keepsake_receipt()
        self.root.quit()

    def _draw_round_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        radius = max(0, min(radius, int((x2 - x1) / 2), int((y2 - y1) / 2)))
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, splinesteps=14, **kwargs)

    def _bind_popup_events(self, win, widget):
        widget.bind("<Button-1>", self.start_move)
        widget.bind("<B1-Motion>", self.on_move)
        widget.bind("<Button-3>", lambda e: self.destroy_popup(win))
        win.bind("<Button-1>", self.start_move)
        win.bind("<B1-Motion>", self.on_move)
        win.bind("<Button-3>", lambda e: self.destroy_popup(win))

    def _popup_message_font_size(self, message):
        base_size = FONT_SIZES["popup_message"]
        if len(message) > 14:
            return max(11, base_size - 3)
        if len(message) > 9:
            return max(12, base_size - 1)
        return base_size

    def create_popup(self, x, y):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.0)  # 初始完全透明
        trans_color = "#010101"
        win.config(bg=trans_color)
        try:
            win.attributes("-transparentcolor", trans_color)
        except tk.TclError:
            pass

        msg = self._select_popup_message()
        color = random.choice(BG_COLORS)
        style = POPUP_CARD_STYLE
        radius = style["corner_radius"]
        border_width = style["border_width"]
        header_height = style["header_height"]

        canvas = tk.Canvas(
            win,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=trans_color,
            bd=0,
            highlightthickness=0,
        )
        canvas.pack(fill=tk.BOTH, expand=True)

        card_x1 = 3
        card_y1 = 2
        card_x2 = WINDOW_WIDTH - 5
        card_y2 = WINDOW_HEIGHT - 6
        self._draw_round_rect(
            canvas,
            card_x1 + 3,
            card_y1 + 4,
            card_x2 + 3,
            card_y2 + 4,
            radius,
            fill=style["shadow"],
            outline="",
        )
        self._draw_round_rect(
            canvas,
            card_x1,
            card_y1,
            card_x2,
            card_y2,
            radius,
            fill=style["border"],
            outline=style["border_active"],
            width=1,
        )

        inner_x1 = card_x1 + border_width
        inner_y1 = card_y1 + border_width
        inner_x2 = card_x2 - border_width
        inner_y2 = card_y2 - border_width
        self._draw_round_rect(
            canvas,
            inner_x1,
            inner_y1,
            inner_x2,
            inner_y2,
            radius - 2,
            fill=color,
            outline="",
        )

        header_color = random.choice([style["header"], style["header_alt"]])
        header_x1 = inner_x1 + style["padding_x"] - 2
        header_y1 = inner_y1 + style["padding_y"] - 4
        header_x2 = header_x1 + 64
        header_y2 = header_y1 + header_height
        self._draw_round_rect(
            canvas,
            header_x1,
            header_y1,
            header_x2,
            header_y2,
            9,
            fill=header_color,
            outline="",
        )
        canvas.create_text(
            header_x1 + 10,
            header_y1 + header_height / 2,
            text=random.choice(style["titles"]),
            anchor="w",
            font=(FONT_FAMILY, FONT_SIZES["popup_title"], "bold"),
            fill=style["title_fg"],
        )

        for dot_x in (header_x2 + 9, header_x2 + 18, header_x2 + 27):
            canvas.create_oval(
                dot_x,
                header_y1 + 6,
                dot_x + 4,
                header_y1 + 10,
                fill=style["border"],
                outline="",
            )

        canvas.create_text(
            inner_x2 - 18,
            header_y1 + header_height / 2 + 1,
            text=random.choice(style["decorations"]),
            font=(EMOJI_FONT_FAMILY, 13),
            fill=style["header_alt"],
        )
        canvas.create_text(
            WINDOW_WIDTH / 2,
            51,
            text=msg,
            font=(FONT_FAMILY, self._popup_message_font_size(msg), "bold"),
            fill=style["message_fg"],
            width=WINDOW_WIDTH - 28,
            justify="center",
        )
        canvas.create_line(
            inner_x1 + 16,
            inner_y2 - 9,
            inner_x2 - 16,
            inner_y2 - 9,
            fill=style["border"],
            width=1,
        )

        self._bind_popup_events(win, canvas)

        self.all_windows.append(win)

        # 淡入动画
        self._fade_in(win, 0.0)

    def _fade_in(self, win, alpha):
        """逐步提升窗口透明度，实现淡入效果"""
        if alpha >= 1.0:
            try:
                win.attributes("-alpha", 1.0)
            except tk.TclError:
                pass
            return
        try:
            win.attributes("-alpha", alpha)
            self.root.after(20, lambda: self._fade_in(win, alpha + 0.3))
        except tk.TclError:
            pass

    def start_move(self, event):
        win = event.widget if isinstance(event.widget, tk.Toplevel) else event.widget.winfo_toplevel()
        win._drag_start_x = event.x_root
        win._drag_start_y = event.y_root
        win._drag_win_x = win.winfo_x()
        win._drag_win_y = win.winfo_y()

    def on_move(self, event):
        win = event.widget if isinstance(event.widget, tk.Toplevel) else event.widget.winfo_toplevel()
        dx = event.x_root - win._drag_start_x
        dy = event.y_root - win._drag_start_y
        win.geometry(f"+{win._drag_win_x + dx}+{win._drag_win_y + dy}")

    def destroy_popup(self, win):
        try:
            if win in self.all_windows:
                self.all_windows.remove(win)
            win.destroy()
        except tk.TclError:
            pass

    def cleanup(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self._destroy_opening_scene()
        self._destroy_blackhole_center()
        self._destroy_chapter_toast()
        self._destroy_interaction_choice()
        self._destroy_memory_cards()
        self._destroy_stamp_signoff()
        self._destroy_transition_burst()
        self._destroy_final_message()
        self._destroy_keepsake_receipt()
        for win in self.all_windows[:]:
            try:
                win.destroy()
            except tk.TclError:
                pass
        self.all_windows.clear()

    def emergency_exit(self):
        """紧急退出：销毁所有窗口并退出程序"""
        self.cleanup()
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PopupApp()
    app.run()
