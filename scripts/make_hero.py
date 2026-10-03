#!/usr/bin/env python3
"""生成 <repo>/assets/hero.gif —— GitHub README 顶部的 hero 动图。

用法：把本文件复制到目标仓库的 scripts/ 下，改「文案：只改这一段」区的常量，然后：
    python3 scripts/make_hero.py

设计约定（改之前先读）：
  - 1200x620 / 12 FPS 采样 / 约 8 秒动画 / 128 色量化 → GIF 约 1.3 MB
  - 播放速度由 FRAME_MS 控制（每帧显示多少毫秒），与采样率 FPS 解耦
  - GitHub 暗色底 #0d1117；四段动画：标记+标题 → 流程 → 特性 → 底栏
  - 图形全部现画，不使用任何人物肖像或第三方素材
  - 顶部标记用几何图形，不要依赖 emoji（Pillow 常渲染不出）

依赖：Pillow
"""
import os

from PIL import Image, ImageDraw, ImageFont

# Pyright 会误报 Image.LANCZOS 不存在（Pillow 类型存根问题，运行没问题）。
# 这样写两个 Pillow 版本都兼容。
RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS

W, H = 1200, 620
FPS = 12
# 每帧显示时长（毫秒）。放慢播放只改这里，不要动 FPS ——
# 12 FPS 采样（83ms/帧）会被反馈「动得有点快」，实测 125ms 才够慢；
# 保持 12 FPS 采样、只加长 FRAME_MS，动画更流畅且节奏更慢。
FRAME_MS = 125
BG = (13, 17, 23)
FG = (234, 240, 246)
DIM = (139, 148, 158)
LINE = (48, 54, 61)
ACC = (88, 166, 255)      # 蓝
ACC2 = (63, 185, 80)      # 绿
ACC3 = (210, 153, 34)     # 黄
ACC4 = (188, 140, 255)    # 紫

FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]


def pick(cands, size):
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def layer():
    return Image.new("RGBA", (W, H), BG + (255,))


def blend(col, a):
    return tuple(int(col[i] * a + BG[i] * (1 - a)) for i in range(3))


def draw_centered(d, y, text, font, fill, alpha=1.0):
    if alpha <= 0.01:
        return
    bbox = d.textbbox((0, 0), text, font=font)
    d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], y), text, font=font,
           fill=blend(fill, alpha) + (255,))


def draw_glyph(img, cx, cy, R, alpha=1.0):
    """顶部标记：圆环 + 内部三条递增横线。换成项目自己的几何符号即可。"""
    if alpha <= 0.01:
        return
    S = 4
    size = R * 2 * S
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cd = ImageDraw.Draw(canvas)
    cd.ellipse([3 * S, 3 * S, size - 3 * S, size - 3 * S],
               outline=blend(ACC, alpha) + (255,), width=2 * S + S // 2)
    gap = size * 0.145
    y0 = size * 0.325
    for i, (frac, col) in enumerate([(0.54, ACC2), (0.74, ACC3), (0.94, ACC4)]):
        w = size * 0.52 * frac
        x0 = (size - w) / 2
        y1 = y0 + i * gap
        cd.rounded_rectangle([x0, y1, x0 + w, y1 + gap * 0.44],
                             radius=gap * 0.22, fill=blend(col, alpha) + (255,))
    canvas = canvas.resize((R * 2, R * 2), RESAMPLE)
    img.paste(canvas, (int(cx - R), int(cy - R)), canvas)


# ========================== 文案：只改这一段 ==========================
TITLE = "AI 命运工具公开测评"
SUBTITLE = "12 款开源工具 · 24 个普通人 · 46 件大事，工具组第一名没超过「四句好话」"

# 流程段：(关键词, 说明, 颜色) —— 说明控制在 8-12 字，两列才平衡
FLOW = [
    ("藏起经历", "只给出生资料和三年窗口", ACC),
    ("自己判断", "事业 · 感情 · 学业 · 钱财", ACC),
    ("交出答案", "先说完，再对公开记录", ACC),
    ("逐条对照", "命中 / 说反 / 漏判分开算", ACC3),
    ("错输入对照", "换个生日再问一遍", ACC3),
    ("冻结评分", "规则先定，成绩后出", ACC2),
]

# 特性段：(编号, 文字, 颜色) —— 全角编号 ①②③ 比 1. 2. 3. 好看
FEATS = [
    ("①", "432 份原始回答全部公开，含对照与探针", ACC),
    ("②", "评分可离线复现，不需要 API 密钥", ACC2),
    ("③", "16 种配置：八字 · 紫微 · 印占 · 奇门 · 六爻 · 塔罗", ACC3),
    ("④", "对照组一样跑：全说好事 / 普通 AI / 错生日", ACC4),
    ("⑤", "边界逐条写清，不把回测说成未来准确率", ACC),
    ("⑥", "大文件与第三方依赖留在本地，只放可复核的", ACC2),
]

FLOW_HEADER = "这条测评是怎么做出来的"   # 特性段上方的小标题
FOOT_L = "评分可离线复现 · Python 3.10+ · 无需联网"
FOOT_R = "24 例 · 46 件事 · 16 种配置 · 432 份回答"
# =====================================================================

# 时间轴（秒）——改文案行数后要相应调整，尤其别让 FLOW 撞到底栏
T_FLOW_START = 1.40
T_FLOW_STEP = 0.33
T_SWITCH = 5.05          # 流程 → 特性 的切换点
T_FEAT_START = 5.22
T_FEAT_STEP = 0.25
T_FOOT = 6.45
TOTAL = 7.9

X_DOT = 366              # 项目符号
X_KEY = 392              # 关键词左对齐列
X_VAL = 604              # 说明左对齐列（与 X_KEY 间距保持在 200 左右，别拉更开）
Y_FLOW = 262
ROW_FLOW = 44            # Y_FLOW + 5*ROW_FLOW 必须明显小于 H-86


def frame(t):
    img = layer()
    d = ImageDraw.Draw(img)
    f_title = pick(FONT_CANDIDATES, 62)
    f_sub = pick(FONT_CANDIDATES, 24)
    f_key = pick(FONT_CANDIDATES, 26)
    f_val = pick(FONT_CANDIDATES, 22)
    f_featmk = pick(FONT_CANDIDATES, 24)
    f_feat = pick(FONT_CANDIDATES, 22)
    f_foot = pick(FONT_CANDIDATES, 18)
    f_small = pick(FONT_CANDIDATES, 16)

    # 阶段 1：标记 + 标题
    a1 = ease(t / 0.85)
    draw_glyph(img, W / 2, 80 + int(12 * (1 - a1)), 46, a1)
    draw_centered(d, 138, TITLE, f_title, FG, a1)
    if t > 0.48:
        draw_centered(d, 216, SUBTITLE, f_sub, DIM, ease((t - 0.48) / 0.65))

    # 阶段 2：流程
    if t < T_SWITCH:
        for i, (key, val, color) in enumerate(FLOW):
            st = T_FLOW_START + i * T_FLOW_STEP
            if t < st:
                break
            a = ease((t - st) / 0.42)
            if t > T_SWITCH - 0.18:
                a *= max(0.0, 1 - (t - (T_SWITCH - 0.18)) / 0.18)
            y = Y_FLOW + i * ROW_FLOW + int(13 * (1 - a))
            d.ellipse([X_DOT - 4, y + 14, X_DOT + 4, y + 22],
                      fill=blend(color, a) + (255,))
            d.text((X_KEY, y), key, font=f_key, fill=blend(FG, a) + (255,))
            d.text((X_VAL, y + 6), val, font=f_val, fill=blend(DIM, a) + (255,))
    # 阶段 3：特性
    else:
        a_h = ease((t - T_SWITCH) / 0.38)
        draw_centered(d, 244, FLOW_HEADER, pick(FONT_CANDIDATES, 23), DIM, a_h)
        for i, (mk, text, color) in enumerate(FEATS):
            st = T_FEAT_START + i * T_FEAT_STEP
            if t < st:
                break
            a = ease((t - st) / 0.42)
            y = 286 + i * 40 + int(11 * (1 - a))
            bbox = d.textbbox((0, 0), text, font=f_feat)
            mk_bbox = d.textbbox((0, 0), mk, font=f_featmk)
            mw = mk_bbox[2] - mk_bbox[0]
            x0 = (W - (mw + 14 + bbox[2] - bbox[0])) / 2
            d.text((x0 - mk_bbox[0], y), mk, font=f_featmk,
                   fill=blend(color, a) + (255,))
            d.text((x0 + mw + 14 - bbox[0], y + 2), text, font=f_feat,
                   fill=blend(color, a) + (255,))

    # 阶段 4：底栏
    if t > T_FOOT:
        a = ease((t - T_FOOT) / 0.5)
        d.line([(110, H - 86), (W - 110, H - 86)],
               fill=blend(LINE, a) + (255,), width=1)
        draw_centered(d, H - 68, FOOT_L, f_foot, ACC2, a)
        draw_centered(d, H - 40, FOOT_R, f_small, DIM, a * 0.95)

    return img.convert("RGB")


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "assets", "hero.gif")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    n = int(TOTAL * FPS)
    frames = [frame(i / FPS) for i in range(n)]
    qs = [f.quantize(colors=128) for f in frames]
    qs[0].save(out, save_all=True, append_images=qs[1:],
               duration=FRAME_MS, loop=0, optimize=True)
    print(f"OK {out}")
    print(f"   {n} frames · {TOTAL}s · {W}x{H} · "
          f"{os.path.getsize(out)/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
