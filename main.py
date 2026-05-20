import tkinter as tk
import random
import math

# -------------------------- 可自定义参数 --------------------------
WINDOW_WIDTH = 180
WINDOW_HEIGHT = 80
HEART_STEP = 3                # 爱心轮廓步长(度)
HEART_SPEED = 30              # 爱心弹窗间隔 (毫秒)
HEART_STAY = 2000             # 爱心停留时间 (毫秒)
RANDOM_COUNT = 150            # 随机弹窗数量
RANDOM_SPEED = 25             # 随机弹窗间隔 (毫秒)

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
BG_COLORS = ["#ffb6c1", "#98fb98", "#87cefa", "#fffacd", "#dda0dd"]
# ----------------------------------------------------------------

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
        exit_win.overrideredirect(True)  # 无标题栏边框
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
        lbl = tk.Label(
            inner_frame, text="520祝福已派送完毕~\n快输入“笨笨亲签”解锁屏幕吧！", 
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
            # 埋一点小彩蛋，多几个合法口令
            if pwd in ["笨笨亲签", "亲签", "收到", "收到啦", "知道啦", "爱你", "我爱你", "本笨笨收到", "本笨笨收到啦", "本笨笨知道啦", "本笨笨爱你", "我爱你"]:
                # 口令正确，触发黑洞吸附动画
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
        
        # 禁用常规的强杀(比如快捷键试图关闭时拦截)
        exit_win.protocol("WM_DELETE_WINDOW", lambda: None)

    def trigger_blackhole_animation(self, exit_win):
        # 首先销毁密码框
        exit_win.destroy()

        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        # 收集所有存活窗口，按距离中心从近到远排序
        items = []
        for win in self.all_windows:
            if not win.winfo_exists():
                continue
            x = win.winfo_x() + WINDOW_WIDTH // 2
            y = win.winfo_y() + WINDOW_HEIGHT // 2
            dist = math.hypot(x - center_x, y - center_y)
            items.append((win, x, y, dist))

        # 按距离从远到近排序 → 外圈先飞
        items.sort(key=lambda d: -d[3])

        # 分波次：每波 20 个窗口，波间间隔 50ms
        # 每个窗口只需要知道起点和飞行速度
        self.waves = []
        BATCH_SIZE = 30
        max_dist = items[0][3] if items else 1

        for i, (win, sx, sy, dist) in enumerate(items):
            wave_idx = i // BATCH_SIZE
            # 飞行速度：像素/帧，距离越远速度越快，保证差不多同时到达
            # 总帧数控制在 18~25 帧（约 0.3~0.4 秒）
            total_frames = random.randint(6, 10)
            # 螺旋方向随机
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

        self.wave_released = 0  # 当前已释放的波次
        self.bh_center_x = center_x
        self.bh_center_y = center_y

        # 启动波次释放定时器
        self.release_next_wave()

    def release_next_wave(self):
        """释放下一波窗口开始飞行"""
        for data in self.waves:
            if data["wave"] == self.wave_released:
                data["started"] = True
        self.wave_released += 1

        # 检查是否还有未释放的波次
        has_more = any(not d["started"] for d in self.waves)
        if has_more:
            self.root.after(20, self.release_next_wave)

        # 如果是第一波，启动动画循环
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
                # 到达中心，直接销毁（不改大小，避免闪烁）
                try:
                    data["win"].destroy()
                except:
                    pass
                continue

            # ease-in-quad：前慢后快，模拟加速吸入
            ease = t * t

            # 基础直线插值
            nx = data["sx"] + (cx - data["sx"]) * ease
            ny = data["sy"] + (cy - data["sy"]) * ease

            # 叠加轻微螺旋偏移（垂直于飞行方向的正弦摆动，随接近中心衰减）
            remaining_ratio = 1.0 - ease
            offset = math.sin(t * math.pi * 2.5) * data["dist"] * data["spin"] * remaining_ratio
            # 垂直方向
            dx = cx - data["sx"]
            dy = cy - data["sy"]
            length = data["dist"] if data["dist"] > 0 else 1
            # 法线方向
            perp_x = -dy / length
            perp_y = dx / length
            nx += offset * perp_x
            ny += offset * perp_y

            win_x = int(nx - WINDOW_WIDTH // 2)
            win_y = int(ny - WINDOW_HEIGHT // 2)

            try:
                # 只移动位置，不改变窗口大小 → 避免重绘闪烁
                data["win"].geometry(f"+{win_x}+{win_y}")
                active.append(data)
            except:
                pass

        self.waves = active

        if self.waves:
            # 30fps 足够流畅，且大幅降低 CPU 压力（相比 16ms/60fps）
            self.root.after(33, self.blackhole_step)
        else:
            self.cleanup()
            self.show_final_message()
            
    def show_final_message(self):
        # 创建一个居中的小窗口，无边框，粉色背景
        self.final_win = tk.Toplevel(self.root)
        self.final_win.overrideredirect(True)
        self.final_win.attributes("-topmost", True)

        final_width, final_height = 700, 200
        fx = (self.screen_width - final_width) // 2
        fy = (self.screen_height - final_height) // 2
        self.final_win.geometry(f"{final_width}x{final_height}+{fx}+{fy}")
        self.final_win.config(bg="#fff0f5")

        self.typewriter_label1 = tk.Label(
            self.final_win, text="", font=("微软雅黑", 24, "bold"),
            fg="#d02090", bg="#fff0f5"
        )
        self.typewriter_label1.pack(padx=30, pady=(40, 10))

        self.typewriter_label2 = tk.Label(
            self.final_win, text="", font=("微软雅黑", 28, "bold"),
            fg="#ff1493", bg="#fff0f5"
        )
        self.typewriter_label2.pack(padx=30, pady=(0, 30))

        # 打字机文本队列
        self.typewriter_lines = [
            (self.typewriter_label1, "我会陪你很久很久 ❤ 不是我想 ❤ 而是我会"),
            (self.typewriter_label2, "祝亲爱的笨笨520快乐！"),
        ]
        self.typewriter_line_idx = 0
        self.typewriter_char_idx = 0
        self._typewriter_step()

    def _typewriter_step(self):
        """逐字显示文本，一行完成后进入下一行"""
        if self.typewriter_line_idx >= len(self.typewriter_lines):
            # 所有文字打完，等待 3 秒后退出
            self.root.after(3000, self.root.quit)
            return

        label, full_text = self.typewriter_lines[self.typewriter_line_idx]
        self.typewriter_char_idx += 1
        displayed = full_text[:self.typewriter_char_idx]
        label.config(text=displayed)

        if self.typewriter_char_idx >= len(full_text):
            # 当前行打完，切换到下一行
            self.typewriter_line_idx += 1
            self.typewriter_char_idx = 0
            # 行间停顿 500ms
            self.root.after(500, self._typewriter_step)
        else:
            # 每个字 100ms
            self.root.after(100, self._typewriter_step)

    def create_popup(self, x, y):
        win = tk.Toplevel(self.root)
        win.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        win.attributes("-topmost", True)

        msg = random.choice(MESSAGES)
        color = random.choice(BG_COLORS)
        label = tk.Label(
            win, text=msg, bg=color,
            font=("微软雅黑", 16, "bold"), fg="#333333"
        )
        label.pack(fill=tk.BOTH, expand=True)

        # 左键拖动
        label.bind("<Button-1>", self.start_move)
        label.bind("<B1-Motion>", self.on_move)
        win.bind("<Button-1>", self.start_move)
        win.bind("<B1-Motion>", self.on_move)

        # 右键关闭
        win.bind("<Button-3>", lambda e: self.destroy_popup(win))

        self.all_windows.append(win)

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
        except:
            pass

    def cleanup(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        for win in self.all_windows[:]:
            try:
                win.destroy()
            except:
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