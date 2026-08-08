import json
from PIL import Image, ImageDraw, ImageFont
import os

# 颜色配置 —— 赛博朋克霓虹风
COLORS = {
    "bg": "#0a0a0a",
    "border": "#00d4ff",
    "title": "#00d4ff",
    "text": "#e0e0e0",
    "subtext": "#888888",
    "accent": "#ff00ff",
    "progress_bg": "#1a1a2e",
    "progress_fill": "#00d4ff",
    "gold": "#FFD700",
    "silver": "#C0C0C0",
    "bronze": "#CD7F32",
}

WIDTH, HEIGHT = 900, 750  # 画布尺寸
FONT_SIZE_TITLE = 32
FONT_SIZE_HEADING = 24
FONT_SIZE_BODY = 18
FONT_SIZE_SMALL = 14

def load_data():
    with open("data/profile.json", "r", encoding="utf-8") as f:
        return json.load(f)

def draw_progress_bar(draw, x, y, w, h, progress, color):
    """画一个霓虹进度条"""
    draw.rectangle([x, y, x + w, y + h], fill="#1a1a2e", outline=color, width=1)
    draw.rectangle([x + 2, y + 2, x + 2 + (w - 4) * progress, y + h - 2], fill=color)

def create_card():
    data = load_data()
    
    # 创建画布
    img = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体（没有则用默认）
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE_TITLE)
        font_heading = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", FONT_SIZE_HEADING)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_BODY)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONT_SIZE_SMALL)
    except:
        font_title = font_heading = font_body = font_small = ImageFont.load_default()

    # ---- 标题 ----
    draw.text((40, 30), f"⚡ {data['name']} · {data['title']}", font=font_title, fill=COLORS["title"])
    
    # ---- 分割线 ----
    draw.line([(40, 75), (WIDTH - 40, 75)], fill=COLORS["border"], width=2)

    y = 100

    # ---- 教育经历 ----
    draw.text((40, y), "🎓 EDUCATION", font=font_heading, fill=COLORS["accent"])
    y += 40
    
    for edu in data["education"]:
        # 学校 + 学位
        draw.text((60, y), f"{edu['school']} · {edu['degree']}", font=font_body, fill=COLORS["text"])
        # 时间
        draw.text((500, y), edu["period"], font=font_body, fill=COLORS["subtext"])
        y += 30
        # 进度条（进行中 / 已完成）
        progress = 0.6 if edu["status"] == "进行中" else 1.0
        draw_progress_bar(draw, 60, y, 600, 8, progress, COLORS["progress_fill"])
        # 状态标签
        status_color = COLORS["progress_fill"] if edu["status"] == "进行中" else "#00ff88"
        draw.text((680, y - 6), edu["status"], font=font_small, fill=status_color)
        if "gpa" in edu:
            draw.text((60, y + 20), f"📊 GPA {edu['gpa']}", font=font_small, fill=COLORS["gold"])
        y += 55

    y += 10

    # ---- 获奖经历 ----
    draw.text((40, y), "🏆 ACHIEVEMENTS", font=font_heading, fill=COLORS["accent"])
    y += 40

    # 奖项颜色映射
    award_colors = {
        "全国一等奖": COLORS["gold"],
        "全国二等奖": COLORS["silver"],
        "省一等奖": COLORS["bronze"],
        "二等奖": COLORS["bronze"],
    }

    for ach in data["achievements"]:
        # 奖项名称
        draw.text((60, y), f"▸ {ach['name']}", font=font_body, fill=COLORS["text"])
        # 奖项等级
        award_text = ach["award"]
        if award_text:
            color = award_colors.get(award_text, COLORS["text"])
            draw.text((500, y), award_text, font=font_body, fill=color)
        # 年份
        if ach["year"]:
            draw.text((680, y), ach["year"], font=font_small, fill=COLORS["subtext"])
        y += 35

    # ---- 底部水印 ----
    draw.line([(40, y + 20), (WIDTH - 40, y + 20)], fill=COLORS["border"], width=1)
    draw.text((40, y + 30), "🔥 AI Infrastructure · FPGA · LLM Inference", font=font_small, fill=COLORS["subtext"])
    draw.text((WIDTH - 300, y + 30), f"⚡ Last updated: auto", font=font_small, fill=COLORS["subtext"])

    # ---- 保存 ----
    os.makedirs("images", exist_ok=True)
    img.save("images/achievements-card.png")
    print("✅ 卡片生成成功: images/achievements-card.png")

if __name__ == "__main__":
    create_card()