# 💕 Love Pop-Up — 节日祝福/表白弹窗小程序

一个用 Python + Tkinter 编写的浪漫表白小工具，通过满屏弹窗 + 爱心动画 + 口令解锁的方式，给 TA 一个甜蜜的惊喜。

**只需修改 `config.py` 中的昵称和文案，即可定制你的专属表白。**

## ✨ 效果流程

1. **爱心弹窗** — 屏幕上按心形轮廓依次弹出彩色祝福弹窗，带淡入效果
2. **随机炸屏** — 150 个弹窗随机铺满全屏，满屏都是爱
3. **口令解锁** — 弹出密码框，输入正确口令才能解锁屏幕
4. **黑洞吸附** — 所有弹窗以螺旋路径飞向屏幕中心并消失
5. **最终告白** — 飘落爱心粒子 + 打字机效果逐字显示告白文字

## 🚀 运行方式

### 直接运行

建议先创建虚拟环境并安装依赖：

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

macOS / Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

本项目运行时不需要第三方 pip 包；`requirements.txt` 主要用于保持通用的安装流程。Tkinter 通常随 Python 自带，部分 Linux 发行版可能需要额外安装系统包 `python3-tk`。

### 打包为 exe

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py config.py
```

打包后的可执行文件在 `dist/` 目录下，可以直接发给对方双击运行。

## 🎨 自定义配置

所有可自定义内容集中在 `config.py` 中，无需修改 `main.py`：

### 核心配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `NICKNAME` | 对象的昵称，全局生效 | `"宝宝"` |
| `PASSWORDS` | 解锁口令列表 | `["亲签", "收到", "爱你"]` |
| `MESSAGES` | 弹窗祝福语列表 | 见 config.py |
| `FINAL_LINE_1` | 最终告白第一行 | `"我会陪你很久很久 ❤"` |
| `FINAL_LINE_2` | 最终告白第二行（支持 `{nickname}` 占位符） | `"祝亲爱的{nickname}520快乐！"` |
| `EXIT_DIALOG_HINT` | 密码框提示文字（支持 `{nickname}` 占位符） | 见 config.py |

### 动画参数

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `HEART_STEP` | 爱心轮廓步长（度），越小越密 | 3 |
| `HEART_SPEED` | 绘制爱心时，相邻祝福弹窗出现间隔（ms），想让每个弹窗隔久一点再出现下一个就调大 | 120 |
| `HEART_STAY` | 整个爱心形状画完后的停留时间（ms） | 2000 |
| `RANDOM_COUNT` | 随机弹窗数量 | 150 |
| `RANDOM_SPEED` | 随机弹窗出现间隔（ms） | 25 |
| `PARTICLE_COUNT` | 飘落爱心粒子数量 | 55 |

`HEART_SPEED` 控制“画爱心过程中，下一个祝福弹窗多久出现”；`HEART_STAY` 控制“整颗爱心画完后，整体停留多久”。如果只是想让组成爱心的每个弹窗出现得慢一点，改 `HEART_SPEED`。

### 视觉配置

| 配置项 | 说明 |
|--------|------|
| `BG_COLORS` | 弹窗背景色列表 |
| `PARTICLE_HEARTS` | 粒子使用的爱心符号 |
| `PARTICLE_COLORS` | 粒子颜色列表 |

### 高级主题配置

如果想整体调整视觉风格，可以继续修改 `config.py` 中的主题配置：

| 配置项 | 说明 |
|--------|------|
| `THEME_NAME` | 当前主题名称 |
| `THEME_COLORS` | 全局主题色板 |
| `TEXT_COLORS` | 文字颜色配置 |
| `POPUP_CARD_STYLE` | 弹窗卡片样式，例如边框、标题条、装饰符号 |
| `EXIT_DIALOG_STYLE` | 口令签收框样式，例如尺寸、按钮色、错误晃动参数 |
| `BLACKHOLE_STYLE` | 黑洞吸附中心视觉样式 |
| `FINAL_SCENE_STYLE` | 最终告白场景样式，例如尺寸、背景色、打字机光标 |
| `FONT_SIZES` | 弹窗、口令框、最终告白的字体大小 |

### 黑洞吸附参数

黑洞吸附速度和遮盖效果集中在 `BLACKHOLE_STYLE` 中：

| 参数 | 当前值 | 说明 |
|------|--------|------|
| `batch_size` | 24 | 每一波开始吸附的弹窗数量，越大同时动的弹窗越多 |
| `release_interval` | 42 | 每一波之间的间隔（ms），越小吸附启动越快 |
| `frame_interval` | 16 | 黑洞动画每帧间隔（ms），越小动画越快也越顺滑 |
| `min_frames` / `max_frames` | 14 / 22 | 单个弹窗飞向中心的帧数，越小吸入速度越快 |
| `spin_min` / `spin_max` | 0.08 / 0.16 | 螺旋偏移强度，越大旋转感越明显 |
| `cover_start` | 0.84 | 弹窗接近中心后被黑洞视觉遮住的时机，越小越早被遮住 |

如果觉得吸入太慢，优先调小 `min_frames` / `max_frames` 或 `release_interval`；如果觉得吸入太急，就把它们调大一点。

## 🔑 口令机制

程序会根据 `NICKNAME` 自动生成一组口令：

- `{NICKNAME}亲签`（如"宝宝亲签"）
- `本{NICKNAME}收到` / `本{NICKNAME}收到啦`
- `本{NICKNAME}知道啦` / `本{NICKNAME}爱你`

加上 `PASSWORDS` 列表中手动配置的口令，任意一个即可通过。

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Shift+Q` | 紧急退出（任何阶段均可使用） |

## 📁 项目结构

```
love-pop-up/
├── main.py        # 主程序逻辑（一般不需要修改）
├── config.py      # 配置文件（修改这里即可自定义）
├── requirements.txt
├── main.spec      # PyInstaller 打包配置
└── README.md
```

## 依赖

- Python 3.6+
- tkinter（通常随 Python 自带；Linux 如缺失可安装 `python3-tk`）
- 无第三方运行时 pip 依赖

## License

MIT
