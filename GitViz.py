#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import dateutil.parser
import LogParse
import sys

LOG          = [] # The log as a list of dictionaries
AUTHORS      = [] # The list if author names
DATES        = [] # The first dayes the authors commit
FONT         = ImageFont.truetype('Library/Fonts/Arial.ttf', 12)
LONGEST_NAME = 0
LONGEST_DATE = 0
NUM_WEEKS    = 0

def find_week(date):
    return int((date - LOG[0]['date']).days / 7)

def create_log(file):
    global LOG, LONGEST_DATE, LONGEST_NAME, NUM_WEEKS

    parser = LogParse.LogParse(sys.argv[1])
    LOG = parser.get_log()
        
    # Sort into date order
    LOG.sort(key=lambda item:item['date'])

    for commit in LOG:
        # Convert the date to a datetime obj
        # Check if this is the longest date
        commit['date'] = dateutil.parser.parse(commit['date']).date()

        # Check if we know the name
        # Check if this is the longest name
        if not commit['author_name'] in AUTHORS:
            AUTHORS.append(commit['author_name'])
            DATES.append(commit['date'])
            name_length = FONT.getsize(commit['author_name'])[0]
            if name_length > LONGEST_NAME:
                LONGEST_NAME = name_length
            date_length = FONT.getsize(str(commit['date']))[0]
            if date_length > LONGEST_DATE:
                LONGEST_DATE = date_length

    NUM_WEEKS = find_week(LOG[-1]['date'])

def draw_viz():
    padding         = FONT.getsize("X")[1]
    img_height      = (2 * padding) + (padding * len(AUTHORS))
    img_width       = (6 * padding) + (padding * NUM_WEEKS) + (2 * LONGEST_NAME) + LONGEST_DATE
    im              = Image.new("RGB", (img_width, img_height))
    draw            = ImageDraw.Draw(im, "RGBA")

    draw.rectangle([(0, 0), (img_width, img_height)], fill = "#FFFFFF", outline = "#FFFFFF")

    # Draw all the names
    for author in AUTHORS:
        draw.text((padding, padding + (padding * AUTHORS.index(author))), author, fill = "black", font = FONT)

    # Draw all the first dates
    for date in range(len(DATES)):
        txt_width = FONT.getsize(str(DATES[date]))[0]
        week_num = find_week(DATES[date])
        block_x = (padding * 3) + LONGEST_NAME + LONGEST_DATE + (padding * week_num)
        x_pos = block_x - (txt_width + padding)
        y_pos = padding + (padding * date)
        draw.text((x_pos, y_pos), str(DATES[date]), fill = "black", font = FONT)

    # Draw all the blobs
    for commit in LOG:
        week_num = find_week(commit['date'])
        block_x = (padding * 3) + LONGEST_NAME + LONGEST_DATE + (padding * week_num)
        block_y = padding + (padding * AUTHORS.index(commit['author_name']))
        draw.rectangle([(block_x, block_y),(block_x + padding, block_y + padding)], fill = (92, 212, 247, 64))

    # Draw the names again
    for author in AUTHORS:
        x_pos = img_width - (padding + LONGEST_NAME)
        y_pos = padding + (padding * AUTHORS.index(author))
        draw.text((x_pos, y_pos), author, fill = "black", font = FONT)

    del draw
    im.save("result.png", "PNG")

if __name__ == "__main__":
    create_log(sys.argv[1])
    draw_viz()
