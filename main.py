import tkinter as tk
import random
import math
from config import (
    NICKNAME, PASSWORDS, MESSAGES, BG_COLORS,
    FINAL_LINE_1, FINAL_LINE_2, EXIT_DIALOG_HINT,
    WINDOW_WIDTH, WINDOW_HEIGHT, HEART_STEP, HEART_SPEED, HEART_STAY,
    RANDOM_COUNT, RANDOM_SPEED,
    PARTICLE_COUNT, PARTICLE_HEARTS, PARTICLE_COLORS,
    FONT_FAMILY, EMOJI_FONT_FAMILY, POPUP_CARD_STYLE, FONT_SIZES,
    EXIT_DIALOG_STYLE, BLACKHOLE_STYLE, FINAL_SCENE_STYLE, SPACING,
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

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # 爱心缩放系数
        short_side = min(self.screen_width, self.screen_height)
        target_width = short_side * 0.8
        self.heart_scale = max(target_width / 32, 1.0)

        # 绑定紧急退出快捷键 Ctrl+Shift+Q
        self.root.bind_all("<Control-Shift-Q>", lambda e: self.emergency_exit())

        # 延迟启动动画
        self.root.after(100, self.start_animation)

    def start_animation(self):
        self.cleanup()
        self.heart_points = self.generate_heart_points()
        self.current_step = 0
        self.spawn_heart_step()

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
            # 满屏弹窗结束后，延迟 1 秒出现退出确认框
            self.after_id = self.root.after(1000, self.show_exit_dialog)

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
        # 1. 将之前炸屏的无用窗口取消置顶，避免挡住最核心的密码框
        for popup_win in self.all_windows:
            popup_win.attributes("-topmost", False)

        # 2. 创建最顶层的无边框退出验证窗口
        style = EXIT_DIALOG_STYLE
        exit_win = tk.Toplevel(self.root)
        exit_win.overrideredirect(True)
        width, height = style["width"], style["height"]
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        exit_win.geometry(f"{width}x{height}+{x}+{y}")
        exit_win.attributes("-topmost", True)
        exit_win.config(bg=style["outer_bg"])

        # 3. UI 样式：签收礼盒/回执卡
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
        lbl = tk.Label(
            inner_frame,
            text=hint_text,
            bg=style["content_bg"],
            fg=style["hint_fg"],
            font=(FONT_FAMILY, FONT_SIZES["dialog_hint"], "bold"),
            justify="center",
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
            pwd = entry.get().strip()
            if pwd in ALL_PASSWORDS:
                btn.config(text="签收成功", bg=style["button_active_bg"])
                self.trigger_blackhole_animation(exit_win)
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
            self.show_final_message()

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
            self.root.after(5000, self._final_exit)
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

    def _final_exit(self):
        """停止粒子动画，销毁所有窗口，退出程序"""
        self.particle_running = False
        self.typewriter_cursor_running = False
        for pw in self.particle_windows:
            try:
                pw.destroy()
            except tk.TclError:
                pass
        try:
            self.final_win.destroy()
        except tk.TclError:
            pass
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

        msg = random.choice(MESSAGES)
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
        self._destroy_blackhole_center()
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
