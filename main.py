import tkinter as tk
import random
import math
from config import (
    NICKNAME, PASSWORDS, MESSAGES, BG_COLORS,
    FINAL_LINE_1, FINAL_LINE_2, EXIT_DIALOG_HINT,
    WINDOW_WIDTH, WINDOW_HEIGHT, HEART_STEP, HEART_SPEED, HEART_STAY,
    RANDOM_COUNT, RANDOM_SPEED,
    PARTICLE_COUNT, PARTICLE_HEARTS, PARTICLE_COLORS,
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

    def show_exit_dialog(self):
        # 1. 将之前炸屏的无用窗口取消置顶，避免挡住最核心的密码框
        for popup_win in self.all_windows:
            popup_win.attributes("-topmost", False)

        # 2. 创建最顶层的无边框退出验证窗口
        exit_win = tk.Toplevel(self.root)
        exit_win.overrideredirect(True)
        width, height = 340, 180
        x = (self.screen_width - width) // 2
        y = (self.screen_height - height) // 2
        exit_win.geometry(f"{width}x{height}+{x}+{y}")
        exit_win.attributes("-topmost", True)

        # 3. UI 样式：使用粉色边框和浅背景
        frame = tk.Frame(exit_win, bg="#dda0dd", bd=4)
        frame.pack(fill=tk.BOTH, expand=True)
        inner_frame = tk.Frame(frame, bg="#fff0f5")
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # 提示文本
        hint_text = EXIT_DIALOG_HINT.replace("{nickname}", NICKNAME)
        lbl = tk.Label(
            inner_frame, text=hint_text,
            bg="#fff0f5", fg="#d02090", font=("微软雅黑", 12, "bold")
        )
        lbl.pack(pady=20)

        # 居中的输入框
        entry = tk.Entry(inner_frame, font=("微软雅黑", 14), justify="center", width=14, bd=2)
        entry.pack(pady=5)
        entry.focus_set()

        # 4. 校验密码逻辑
        def check_password(event=None):
            pwd = entry.get().strip()
            if pwd in ALL_PASSWORDS:
                self.trigger_blackhole_animation(exit_win)
            else:
                lbl.config(text="口令不对哦，再试一次嘛~", fg="red")
                entry.delete(0, tk.END)

        # 确认按钮
        btn = tk.Button(
            inner_frame, text="确认查收", font=("微软雅黑", 10, "bold"),
            bg="#ffb6c1", fg="white", activebackground="#ff69b4",
            relief=tk.FLAT, command=check_password
        )
        btn.pack(pady=10)

        # 绑定回车键可以快捷确认
        exit_win.bind("<Return>", check_password)

        # 禁用常规的强杀
        exit_win.protocol("WM_DELETE_WINDOW", lambda: None)

    def trigger_blackhole_animation(self, exit_win):
        exit_win.destroy()

        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        items = []
        for win in self.all_windows:
            if not win.winfo_exists():
                continue
            x = win.winfo_x() + WINDOW_WIDTH // 2
            y = win.winfo_y() + WINDOW_HEIGHT // 2
            dist = math.hypot(x - center_x, y - center_y)
            items.append((win, x, y, dist))

        items.sort(key=lambda d: -d[3])

        self.waves = []
        BATCH_SIZE = 30

        for i, (win, sx, sy, dist) in enumerate(items):
            wave_idx = i // BATCH_SIZE
            total_frames = random.randint(6, 10)
            spin = random.choice([-1, 1]) * random.uniform(0.08, 0.15)

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
            self.root.after(20, self.release_next_wave)

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

            ease = t * t
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
                active.append(data)
            except tk.TclError:
                pass

        self.waves = active

        if self.waves:
            self.root.after(33, self.blackhole_step)
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
        self.final_win = tk.Toplevel(self.root)
        self.final_win.overrideredirect(True)
        self.final_win.attributes("-topmost", True)

        final_width, final_height = 720, 240
        fx = (self.screen_width - final_width) // 2
        fy = (self.screen_height - final_height) // 2
        self.final_win.geometry(f"{final_width}x{final_height}+{fx}+{fy}")

        # 外层渐变边框效果：用多层 Frame 模拟
        border_frame = tk.Frame(self.final_win, bg="#ff69b4", bd=0)
        border_frame.pack(fill=tk.BOTH, expand=True)
        inner_border = tk.Frame(border_frame, bg="#ffb6c1", bd=0)
        inner_border.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        content_frame = tk.Frame(inner_border, bg="#2d1b2e", bd=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # 顶部装饰爱心
        deco_label = tk.Label(
            content_frame, text="💗 · 💕 · 💗", font=("Segoe UI Emoji", 14),
            fg="#ff69b4", bg="#2d1b2e"
        )
        deco_label.pack(pady=(15, 5))

        self.typewriter_label1 = tk.Label(
            content_frame, text="", font=("微软雅黑", 22, "bold"),
            fg="#ffb6c1", bg="#2d1b2e"
        )
        self.typewriter_label1.pack(padx=30, pady=(10, 8))

        self.typewriter_label2 = tk.Label(
            content_frame, text="", font=("微软雅黑", 26, "bold"),
            fg="#ff69b4", bg="#2d1b2e"
        )
        self.typewriter_label2.pack(padx=30, pady=(0, 8))

        # 底部装饰线
        bottom_deco = tk.Label(
            content_frame, text="━━━━━━━━━━━━━━━━━━━━",
            font=("微软雅黑", 8), fg="#ff69b4", bg="#2d1b2e"
        )
        bottom_deco.pack(pady=(0, 12))

        # 打字机文本队列（使用配置中的文本，替换昵称占位符）
        line1 = FINAL_LINE_1
        line2 = FINAL_LINE_2.replace("{nickname}", NICKNAME)
        self.typewriter_lines = [
            (self.typewriter_label1, line1),
            (self.typewriter_label2, line2),
        ]
        self.typewriter_line_idx = 0
        self.typewriter_char_idx = 0
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

    def _typewriter_step(self):
        """逐字显示文本，一行完成后进入下一行"""
        if self.typewriter_line_idx >= len(self.typewriter_lines):
            self.root.after(5000, self._final_exit)
            return

        label, full_text = self.typewriter_lines[self.typewriter_line_idx]
        self.typewriter_char_idx += 1
        displayed = full_text[:self.typewriter_char_idx]
        label.config(text=displayed)

        if self.typewriter_char_idx >= len(full_text):
            self.typewriter_line_idx += 1
            self.typewriter_char_idx = 0
            self.root.after(500, self._typewriter_step)
        else:
            self.root.after(100, self._typewriter_step)

    def _final_exit(self):
        """停止粒子动画，销毁所有窗口，退出程序"""
        self.particle_running = False
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

    def create_popup(self, x, y):
        win = tk.Toplevel(self.root)
        win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        win.attributes("-topmost", True)
        win.attributes("-alpha", 0.0)  # 初始完全透明

        msg = random.choice(MESSAGES)
        color = random.choice(BG_COLORS)
        label = tk.Label(
            win, text=msg, bg=color,
            font=("微软雅黑", 16, "bold"), fg="#333333"
        )
        label.pack(fill=tk.BOTH, expand=True)

        label.bind("<Button-1>", self.start_move)
        label.bind("<B1-Motion>", self.on_move)
        win.bind("<Button-1>", self.start_move)
        win.bind("<B1-Motion>", self.on_move)
        win.bind("<Button-3>", lambda e: self.destroy_popup(win))

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
