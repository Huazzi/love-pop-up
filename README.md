# 💕 LoveProgram — 节日祝福/表白弹窗小程序

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

```bash
python main.py
```

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
| `HEART_SPEED` | 爱心弹窗出现间隔（ms） | 30 |
| `HEART_STAY` | 爱心形状停留时间（ms） | 2000 |
| `RANDOM_COUNT` | 随机弹窗数量 | 150 |
| `RANDOM_SPEED` | 随机弹窗出现间隔（ms） | 25 |
| `PARTICLE_COUNT` | 飘落爱心粒子数量 | 55 |

### 视觉配置

| 配置项 | 说明 |
|--------|------|
| `BG_COLORS` | 弹窗背景色列表 |
| `PARTICLE_HEARTS` | 粒子使用的爱心符号 |
| `PARTICLE_COLORS` | 粒子颜色列表 |

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
loveProgram/
├── main.py        # 主程序逻辑（一般不需要修改）
├── config.py      # 配置文件（修改这里即可自定义）
├── main.spec      # PyInstaller 打包配置
└── README.md
```

## 依赖

- Python 3.6+
- tkinter（Python 自带，无需额外安装）

## License

MIT
