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
    body_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 13)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 11)
except Exception:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    section_font = ImageFont.load_default()
    h_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
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
        # Use getlength if available, else textbbox
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

# Layout: 2 Columns for the 5 stories
# Col 1: Left X: 30 to 500. Col 2: Right X: 524 to 994.
# Y starts at 160.

# We have 5 stories:
stories = [
    {
        "num": "01",
        "title": "COP31 CLIMATE TALKS COLLAPSE",
        "summary": "UN climate summit in Antalya, Turkey ends Sunday without agreement after a dispute over fossil fuels; the EU, Britain and allies rejected the final draft deal. First such collapse since 2009.",
        "icon": "climate"
    },
    {
        "num": "02",
        "title": "ICJ: MYANMAR COMMITTED GENOCIDE",
        "summary": "The International Court of Justice rules that Myanmar committed genocide against its Rohingya minority.",
        "icon": "icj"
    },
    {
        "num": "03",
        "title": "INDONESIA CANDY FACTORY FIRE",
        "summary": "Fire at the Fonusa Agung Mulia confectionery factory in Cikande, Banten, kills at least three people; 36 workers missing.",
        "icon": "fire"
    },
    {
        "num": "04",
        "title": "MEXICO CAPTURES 'EL CHAPO ISIDRO'",
        "summary": "Mexican elite troops capture alleged cartel boss Fausto Isidro Meza Flores in a Sinaloa raid; a firefight kills four soldiers.",
        "icon": "mexico"
    },
    {
        "num": "05",
        "title": "NVIDIA CHIP SCANDAL",
        "summary": "The US confirms China accessed AI chips; the New York Times reports a Chinese spy-agency campaign to obtain AI chips around Western export restrictions.",
        "icon": "chip"
    }
]

def draw_icon(draw, type_str, x, y, size=60):
    # Draw background box for illustration
    draw.rectangle([x, y, x+size, y+size], outline="#333333", width=1, fill="#F2EEE2")
    cx, cy = x + size//2, y + size//2
    
    if type_str == "climate":
        # Globe & broken line
        draw.ellipse([cx-18, cy-18, cx+18, cy+18], outline="#222222", width=2)
        draw.line([cx-14, cy, cx+14, cy], fill="#222222", width=1)
        draw.line([cx, cy-14, cx, cy+14], fill="#222222", width=1)
        draw.line([cx-16, cy+16, cx+16, cy-16], fill="#CC3333", width=3)
    elif type_str == "icj":
        # Scales of justice
        draw.line([cx, cy-22, cx, cy+18], fill="#222222", width=2)
        draw.line([cx-16, cy-12, cx+16, cy-12], fill="#222222", width=2)
        draw.arc([cx-22, cy-2, cx-10, cy+20], 0, 180, fill="#222222", width=2)
        draw.line([cx-16, cy-12, cx-16, cy+2], fill="#222222", width=1)
        draw.line([cx-22, cy+2, cx-10, cy+2], fill="#222222", width=1)
        draw.arc([cx+10, cy-2, cx+22, cy+20], 0, 180, fill="#222222", width=2)
        draw.line([cx+16, cy-12, cx+16, cy+2], fill="#222222", width=1)
        draw.line([cx+10, cy+2, cx+22, cy+2], fill="#222222", width=1)
    elif type_str == "fire":
        # Factory & smoke/flame
        draw.rectangle([cx-18, cy-2, cx+18, cy+22], outline="#222222", width=2)
        draw.polygon([(cx-12, cy-2), (cx-6, cy-14), (cx-2, cy-2)], fill="#CC3333")
        draw.polygon([(cx+2, cy-2), (cx+8, cy-16), (cx+12, cy-2)], fill="#CC3333")
    elif type_str == "mexico":
        # Shield / star
        draw.polygon([(cx, cy-20), (cx+16, cy-10), (cx+16, cy+10), (cx, cy+22), (cx-16, cy+10), (cx-16, cy-10)], outline="#222222", width=2)
        draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill="#222222")
    elif type_str == "chip":
        # Microprocessor chip
        draw.rectangle([cx-16, cy-16, cx+16, cy+16], outline="#222222", width=2, fill="#E4E0D4")
        # Pins
        for p in [-10, -3, 4, 11]:
            draw.line([cx+p, cy-22, cx+p, cy-16], fill="#222222", width=2)
            draw.line([cx+p, cy+16, cx+p, cy+22], fill="#222222", width=2)
            draw.line([cx-22, cy+p, cx-16, cy+p], fill="#222222", width=2)
            draw.line([cx+16, cy+p, cx+22, cy+p], fill="#222222", width=2)

# Coordinates for 5 stories
# Let's do 2 columns:
# Left column: stories 0, 1, 2
# Right column: stories 3, 4

col_w = 468
left_x = 30
right_x = 526

# We can position each story block cleanly
# Box heights ~ 270px each
y_positions_left = [160, 445, 730]
y_positions_right = [160, 500] # Right side has 2 major stories with deep coverage

# Story 0, 1, 2 on left
# Story 3, 4 on right

def render_story(draw, story, x, y, w):
    # Outer box for story
    draw.rectangle([x, y, x+w, y+270], outline="#D0CBC0", width=1, fill="#FFFFFF")
    
    # Story number & category bar
    draw.rectangle([x, y, x+w, y+24], fill="#333333")
    header_str = f"SPECIAL REPORT — ITEM {story['num']}"
    draw.text((x+10, y+4), header_str, fill="#FBF9F1", font=small_font)
    
    # Icon on top right of box
    draw_icon(draw, story["icon"], x + w - 75, y + 36, size=60)
    
    # Headline
    hx = x + 12
    hy = y + 34
    hw_max = w - 95
    h_lines = wrap_text(story["title"], h_font, hw_max)
    for i, line in enumerate(h_lines[:2]):
        draw.text((hx, hy + i*18), line, fill="#111111", font=h_font)
    
    # Divider line
    draw.line([x+12, y+85, x+w-12, y+85], fill="#CCCCCC", width=1)
    
    # Summary paragraph
    sx = x + 12
    sy = y + 95
    sw_max = w - 24
    body_lines = wrap_text(story["summary"], body_font, sw_max)
    for i, line in enumerate(body_lines[:8]):
        draw.text((sx, sy + i*16), line, fill="#333333", font=body_font)

# Render Left Column (Stories 0, 1, 2)
render_story(draw, stories[0], left_x, 160, col_w)
render_story(draw, stories[1], left_x, 445, col_w)
render_story(draw, stories[2], left_x, 730, col_w)

# Render Right Column (Stories 3, 4) - make them taller/deeper since there are 2
def render_story_tall(draw, story, x, y, w, h):
    draw.rectangle([x, y, x+w, y+h], outline="#D0CBC0", width=1, fill="#FFFFFF")
    
    draw.rectangle([x, y, x+w, y+24], fill="#333333")
    header_str = f"SPECIAL REPORT — ITEM {story['num']}"
    draw.text((x+10, y+4), header_str, fill="#FBF9F1", font=small_font)
    
    draw_icon(draw, story["icon"], x + w - 75, y + 36, size=60)
    
    hx = x + 12
    hy = y + 34
    hw_max = w - 95
    h_lines = wrap_text(story["title"], h_font, hw_max)
    for i, line in enumerate(h_lines[:2]):
        draw.text((hx, hy + i*18), line, fill="#111111", font=h_font)
    
    draw.line([x+12, y+85, x+w-12, y+85], fill="#CCCCCC", width=1)
    
    sx = x + 12
    sy = y + 95
    sw_max = w - 24
    body_lines = wrap_text(story["summary"], body_font, sw_max)
    for i, line in enumerate(body_lines[:12]):
        draw.text((sx, sy + i*16), line, fill="#333333", font=body_font)

render_story_tall(draw, stories[3], right_x, 160, col_w, 410)
render_story_tall(draw, stories[4], right_x, 590, col_w, 410)

# Save image as entry.png
output_path = "entry.png"
image.save(output_path, "PNG")
print(f"Successfully generated {output_path}")
