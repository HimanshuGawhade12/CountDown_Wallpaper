from PIL import Image, ImageDraw, ImageFont
import os
import ctypes
from datetime import datetime
import time

target_date = datetime(2025, 4, 30, 23, 59, 59)

def create_wallpaper():
    now = datetime.now()
    remaining = target_date - now

    if remaining.total_seconds() <= 0:
        text = ["00", "00", "00", "00"]
        labels = ["DAYS", "HOURS", "MINUTES", "SECONDS"]
    else:
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds // 60) % 60
        seconds = remaining.seconds % 60
        text = [f"{days:03}", f"{hours:02}", f"{minutes:02}", f"{seconds:02}"]
        labels = ["DAYS", "HOURS", "MINUTES", "SECONDS"]

    width, height = 1920, 1080  
    image = Image.new('RGB', (width, height), (0, 0, 0)) 
    draw = ImageDraw.Draw(image)
  
    font_path =  "GLECB.TTF"
    try:
        number_font = ImageFont.truetype(font_path, 200)  
        label_font = ImageFont.truetype(font_path, 60)  
    except OSError:
        print("Error: Font file not found. Use a valid .ttf file.")
        return
   
    spacing = 90
    total_width = 0
    max_column_widths = []

    for num, label in zip(text, labels):
        num_width = draw.textbbox((0, 0), num, font=number_font)[2]
        label_width = draw.textbbox((0, 0), label, font=label_font)[2]
        column_width = max(num_width, label_width)
        max_column_widths.append(column_width)
        total_width += column_width + spacing

    total_width -= spacing 
    start_x = (width - total_width) // 2
    y_offset_number = height // 3
    y_offset_label = y_offset_number + 150  

    current_x = start_x
    for num, label, column_width in zip(text, labels, max_column_widths):
        num_bbox = draw.textbbox((0, 0), num, font=number_font)
        num_width = num_bbox[2] - num_bbox[0]
        num_height = num_bbox[3] - num_bbox[1]
        draw.text(
            (current_x + (column_width - num_width) // 2, y_offset_number - num_height // 2),
            num,
            font=number_font,
            fill=(255, 255, 255),
        )

        label_bbox = draw.textbbox((0, 0), label, font=label_font)
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]
        draw.text(
            (current_x + (column_width - label_width) // 2, y_offset_label - label_height // 2),
            label,
            font=label_font,
            fill=(255, 255, 255),
        )

        current_x += column_width + spacing

    image_path = "countdown_wallpaper.jpg"
    image.save(image_path)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(image_path), 0)

if __name__ == "__main__":
    while True:
        create_wallpaper()
        time.sleep(1)
