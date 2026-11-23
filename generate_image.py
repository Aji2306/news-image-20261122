import os
from PIL import Image, ImageDraw, ImageFont

# Create 1024x1024 image with newspaper cream background
width, height = 1024, 1024
image = Image.new("RGB", (width, height), color="#FBF9F1")
draw = ImageDraw.Draw(image)

# Load fonts
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 52)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 16)
    section_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 18)
    h_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 14)
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 14)
    fact_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf", 11)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 11)
except Exception:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    section_font = ImageFont.load_default()
    h_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    fact_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Draw Header Box / Masthead
draw.rectangle([30, 20, 994, 110], fill="#111111")
draw.text((width // 2, 42), "THE DAILY CHRONICLE", fill="#FBF9F1", font=title_font, anchor="mm")

# Date / Sub-header bar
draw.rectangle([30, 110, 994, 138], fill="#EAE5D8")
date_text = "SUNDAY, 22 NOVEMBER 2026  |  WORLD NEWS EDITION  |  FINAL CHRONICLE"
draw.text((width // 2, 124), date_text, fill="#222222", font=subtitle_font, anchor="mm")
draw.line([30, 142, 994, 142], fill="#111111", width=2)

# Helper function to wrap text
def wrap_text(text, font, max_width):
    lines = []
    words = text.split(" ")
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        try:
            w = font.getlength(test_line)
        except AttributeError:
            bbox = font.getbbox(test_line)
            w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# 5 Verified Stories with Fact Strips
stories = [
    {
        "num": "01",
        "title": "COP31 CLIMATE TALKS COLLAPSE",
        "fact": "LOCATION: ANTALYA, TURKEY | STATUS: DEADLOCKED OVER FOSSIL FUELS",
        "summary": "UN climate summit in Antalya, Turkey ends Sunday without agreement after a dispute over fossil fuels; the EU, Britain and allies rejected the final draft deal. First such collapse since 2009.",
        "icon": "climate"
    },
    {
        "num": "02",
        "title": "ICJ: MYANMAR COMMITTED GENOCIDE",
        "fact": "TRIBUNAL: INTERNATIONAL COURT OF JUSTICE | TARGET: ROHINGYA MINORITY",
        "summary": "The International Court of Justice rules that Myanmar committed genocide against its Rohingya minority.",
        "icon": "icj"
    },
    {
        "num": "03",
        "title": "INDONESIA CANDY FACTORY FIRE",
        "fact": "LOCATION: CIKANDE, BANTEN | FACILITY: FONUSA AGUNG MULIA",
        "summary": "Fire at the Fonusa Agung Mulia confectionery factory in Cikande, Banten, kills at least three people; 36 workers missing.",
        "icon": "fire"
    },
    {
        "num": "04",
        "title": "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
        "fact": "LOCATION: SINALOA, MEXICO | OPERATION: ELITE TROOPS RAID",
        "summary": "Mexican elite troops capture alleged cartel boss Fausto Isidro Meza Flores in a Sinaloa raid; a firefight kills four soldiers.",
        "icon": "mexico"
    },
    {
        "num": "05",
        "title": "NVIDIA CHIP SCANDAL",
        "fact": "ACTOR: CHINESE SPY AGENCY | ISSUE: AI EXPORT RESTRICTIONS",
        "summary": "The US confirms China accessed AI chips; the New York Times reports a Chinese spy-agency campaign to obtain AI chips around Western export restrictions.",
        "icon": "chip"
    }
]

def draw_icon(draw, type_str, x, y, size=60):
    draw.rectangle([x, y, x+size, y+size], outline="#333333", width=1, fill="#F2EEE2")
    cx, cy = x + size//2, y + size//2
    
    if type_str == "climate":
        draw.ellipse([cx-18, cy-18, cx+18, cy+18], outline="#222222", width=2)
        draw.line([cx-14, cy, cx+14, cy], fill="#222222", width=1)
        draw.line([cx, cy-14, cx, cy+14], fill="#222222", width=1)
        draw.line([cx-16, cy+16, cx+16, cy-16], fill="#CC3333", width=3)
    elif type_str == "icj":
        draw.line([cx, cy-22, cx, cy+18], fill="#222222", width=2)
        draw.line([cx-16, cy-12, cx+16, cy-12], fill="#222222", width=2)
        draw.arc([cx-22, cy-2, cx-10, cy+20], 0, 180, fill="#222222", width=2)
        draw.line([cx-16, cy-12, cx-16, cy+2], fill="#222222", width=1)
        draw.line([cx-22, cy+2, cx-10, cy+2], fill="#222222", width=1)
        draw.arc([cx+10, cy-2, cx+22, cy+20], 0, 180, fill="#222222", width=2)
        draw.line([cx+16, cy-12, cx+16, cy+2], fill="#222222", width=1)
        draw.line([cx+10, cy+2, cx+22, cy+2], fill="#222222", width=1)
    elif type_str == "fire":
        draw.rectangle([cx-18, cy-2, cx+18, cy+22], outline="#222222", width=2)
        draw.polygon([(cx-12, cy-2), (cx-6, cy-14), (cx-2, cy-2)], fill="#CC3333")
        draw.polygon([(cx+2, cy-2), (cx+8, cy-16), (cx+12, cy-2)], fill="#CC3333")
    elif type_str == "mexico":
        draw.polygon([(cx, cy-20), (cx+16, cy-10), (cx+16, cy+10), (cx, cy+22), (cx-16, cy+10), (cx-16, cy-10)], outline="#222222", width=2)
        draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill="#222222")
    elif type_str == "chip":
        draw.rectangle([cx-16, cy-16, cx+16, cy+16], outline="#222222", width=2, fill="#E4E0D4")
        for p in [-10, -3, 4, 11]:
            draw.line([cx+p, cy-22, cx+p, cy-16], fill="#222222", width=2)
            draw.line([cx+p, cy+16, cx+p, cy+22], fill="#222222", width=2)
            draw.line([cx-22, cy+p, cx-16, cy+p], fill="#222222", width=2)
            draw.line([cx+16, cy+p, cx+22, cy+p], fill="#222222", width=2)

col_w = 468
left_x = 30
right_x = 526

def render_story(draw, story, x, y, w, h):
    draw.rectangle([x, y, x+w, y+h], outline="#D0CBC0", width=1, fill="#FFFFFF")
    
    # Story number & category bar
    draw.rectangle([x, y, x+w, y+24], fill="#333333")
    header_str = f"SPECIAL REPORT — ITEM {story['num']}"
    draw.text((x+10, y+4), header_str, fill="#FBF9F1", font=small_font)
    
    # Icon
    draw_icon(draw, story["icon"], x + w - 75, y + 36, size=60)
    
    # Headline
    hx = x + 12
    hy = y + 32
    hw_max = w - 95
    h_lines = wrap_text(story["title"], h_font, hw_max)
    for i, line in enumerate(h_lines[:2]):
        draw.text((hx, hy + i*17), line, fill="#111111", font=h_font)
    
    # Fact strip background bar
    draw.rectangle([x+12, y+72, x+w-12, y+92], fill="#F2EEE2")
    draw.text((x+18, y+76), story["fact"], fill="#555555", font=fact_font)
    
    # Divider line
    draw.line([x+12, y+98, x+w-12, y+98], fill="#CCCCCC", width=1)
    
    # Summary paragraph with slightly larger font & tighter line spacing
    sx = x + 12
    sy = y + 106
    sw_max = w - 24
    body_lines = wrap_text(story["summary"], body_font, sw_max)
    for i, line in enumerate(body_lines[:10]):
        draw.text((sx, sy + i*18), line, fill="#222222", font=body_font)

# Render Left Column (3 stories: height ~ 266 each)
render_story(draw, stories[0], left_x, 160, col_w, 266)
render_story(draw, stories[1], left_x, 436, col_w, 266)
render_story(draw, stories[2], left_x, 712, col_w, 278)

# Render Right Column (2 taller stories: height ~ 409 each)
def render_story_tall(draw, story, x, y, w, h):
    draw.rectangle([x, y, x+w, y+h], outline="#D0CBC0", width=1, fill="#FFFFFF")
    
    draw.rectangle([x, y, x+w, y+24], fill="#333333")
    header_str = f"SPECIAL REPORT — ITEM {story['num']}"
    draw.text((x+10, y+4), header_str, fill="#FBF9F1", font=small_font)
    
    draw_icon(draw, story["icon"], x + w - 75, y + 36, size=60)
    
    hx = x + 12
    hy = y + 32
    hw_max = w - 95
    h_lines = wrap_text(story["title"], h_font, hw_max)
    for i, line in enumerate(h_lines[:2]):
        draw.text((hx, hy + i*17), line, fill="#111111", font=h_font)
    
    draw.rectangle([x+12, y+72, x+w-12, y+92], fill="#F2EEE2")
    draw.text((x+18, y+76), story["fact"], fill="#555555", font=fact_font)
    
    draw.line([x+12, y+98, x+w-12, y+98], fill="#CCCCCC", width=1)
    
    sx = x + 12
    sy = y + 106
    sw_max = w - 24
    body_lines = wrap_text(story["summary"], body_font, sw_max)
    for i, line in enumerate(body_lines[:15]):
        draw.text((sx, sy + i*18), line, fill="#222222", font=body_font)

render_story_tall(draw, stories[3], right_x, 160, col_w, 409)
render_story_tall(draw, stories[4], right_x, 581, col_w, 409)

# Save image as entry.png
output_path = "entry.png"
image.save(output_path, "PNG")
print(f"Successfully generated denser layout {output_path}")
