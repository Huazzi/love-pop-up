# 💕 Love Pop-Up — 节日祝福/表白弹窗小程序

一个用 Python + Tkinter 编写的浪漫表白小工具，通过满屏弹窗 + 爱心动画 + 口令解锁的方式，给 TA 一个甜蜜的惊喜。

**只需修改 `config.py` 中的昵称和文案，即可定制你的专属表白。**

## ✨ 效果流程

1. **开场预热** — 居中显示专属来信、心跳爱心和短倒计时
2. **分幕祝福** — 按照照顾、想念、夸奖、承诺等章节推进弹窗文案
3. **爱心弹窗** — 屏幕上按心形轮廓依次弹出彩色祝福弹窗，带淡入效果
4. **随机炸屏** — 150 个弹窗随机铺满全屏，满屏都是爱
5. **轻互动选择** — 选择当前心情，后续签收提示和回执会带上这个选择
6. **回忆碎片** — 自动展示几张文字回忆卡片，作为签收前的小桥段
7. **口令签收** — 弹出甜蜜签收单，输入正确口令后出现“已签收”盖章动画
8. **黑洞转场** — 所有弹窗以螺旋路径飞向屏幕中心，随后出现扩散爆发转场
9. **最终告白** — 飘落爱心粒子 + 打字机效果逐字显示告白文字
10. **留存回执** — 最后显示一张可配置的永久签收回执页，并按配置自动退出

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
pyinstaller main.spec
```

打包后的可执行文件在 `dist/` 目录下，可以直接发给对方双击运行。

如果不使用 `main.spec`，需要手动把字体资源加入打包命令：

```powershell
pyinstaller --onefile --noconsole --add-data "assets/fonts/LXGWBright-Regular.ttf;assets/fonts" main.py
```

### 打包为 macOS App

在 macOS 上可以使用项目内置脚本生成可双击打开的 `.app`：

```bash
./scripts/build_macos_app.sh
```

脚本会自动完成以下步骤：

- 从 `assets/icon01.png` 生成 `assets/love.icns`
- 使用 `main_macos.spec` 调用 PyInstaller
- 生成 `dist/Love Pop-Up.app`
- 生成便于发送的 `Love Pop-Up.zip`

如果脚本没有执行权限，先运行：

```bash
chmod +x scripts/build_macos_app.sh
```

首次构建会通过 `uvx` 临时下载并运行 PyInstaller，不会在项目内创建虚拟环境或锁文件。

未经过 Apple Developer ID 签名和公证的 `.app` 发给别人后，macOS 可能会拦截首次打开。短期测试可以右键选择“打开”；正式分发建议增加签名、公证和 DMG 打包流程。

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

### 剧情内容配置

这些配置决定“表白小剧场”每个环节展示什么内容：

| 配置项 | 说明 |
|--------|------|
| `OPENING_LINES` | 开场预热逐段显示的短句，支持 `{nickname}` 占位符 |
| `BLESSING_CHAPTERS` | 分幕式祝福配置，每一幕包含 `title`、`subtitle` 和 `messages` |
| `INTERACTION_CHOICES` | 轻互动按钮配置，每个选项包含 `label` 和选择后的 `reply` |
| `MEMORY_CARDS` | 回忆碎片卡片列表，每张卡可配置 `date`、`title`、`text`、`icon` |
| `STAMP_SIGNOFF_STYLE["text"]` | 正确口令后的盖章文字 |
| `TRANSITION_BURST_STYLE["caption"]` | 黑洞吸收完成后的爆发转场提示 |
| `KEEPSAKE_RECEIPT` | 最终留存回执内容，包括寄件人、收件人、有效期、编号、条目和结尾文案 |

`BLESSING_CHAPTERS` 为空时会自动退回到旧的 `MESSAGES` 随机祝福模式。`MEMORY_CARDS` 为空或关闭时，会跳过回忆碎片环节并继续进入签收单。

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
| `OPENING_SCENE_STYLE` | 开场预热窗口样式和时长 |
| `CHAPTER_TOAST_STYLE` | 分幕标题提示条样式 |
| `INTERACTION_CHOICE_STYLE` | 心情选择窗口样式 |
| `MEMORY_CARD_STYLE` | 回忆碎片卡片窗口样式 |
| `POPUP_CARD_STYLE` | 弹窗卡片样式，例如边框、标题条、装饰符号 |
| `EXIT_DIALOG_STYLE` | 口令签收框样式，例如尺寸、按钮色、错误晃动参数 |
| `STAMP_SIGNOFF_STYLE` | “已签收”盖章动画样式 |
| `BLACKHOLE_STYLE` | 黑洞吸附中心视觉样式 |
| `TRANSITION_BURST_STYLE` | 黑洞后扩散爆发转场样式 |
| `FINAL_SCENE_STYLE` | 最终告白场景样式，例如尺寸、背景色、打字机光标 |
| `KEEPSAKE_RECEIPT_STYLE` | 最终留存回执页样式、延迟和停留时长 |
| `FONT_SIZES` | 各阶段窗口、按钮、卡片和告白文字的字体大小 |

### 最终留存回执

最终告白文字打完后，程序会等待 `KEEPSAKE_RECEIPT_STYLE["delay_after_typewriter"]` 毫秒，再切换到留存回执页。回执页展示完成后，会在 `KEEPSAKE_RECEIPT_STYLE["display_duration"]` 毫秒后自动退出。

常用字段：

| 配置项 | 说明 |
|--------|------|
| `KEEPSAKE_RECEIPT["sender"]` | 寄件人 |
| `KEEPSAKE_RECEIPT["recipient"]` | 收件人，支持 `{nickname}` |
| `KEEPSAKE_RECEIPT["validity"]` | 回执有效期 |
| `KEEPSAKE_RECEIPT["serial"]` | 回执编号，支持 `{nickname}` |
| `KEEPSAKE_RECEIPT["items"]` | 回执详情条目，支持 `{nickname}` 和 `{choice}` |
| `KEEPSAKE_RECEIPT["closing_lines"]` | 回执页底部的留存文案 |
| `KEEPSAKE_RECEIPT_STYLE["display_duration"]` | 回执页显示时长 |

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
