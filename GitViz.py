#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import dateutil.parser
import json
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

    with open(file) as data_file:    
        LOG = json.load(data_file) 
        
    # Sort into date order
    LOG.sort(key=lambda item:item['date'])

    for commit in LOG:
        # Convert the date to a datetime obj
        # Check if this is the longest date
        commit['date'] = dateutil.parser.parse(commit['date'])

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
    """
    - The height of the image:
      Two spare blocks (top, bottom) + one block per author
    - The width of the image:
      Two spare blocks (left, right) + two spare blocks (after name, date) + one block per week + name + date
    """
    forget, padding = FONT.getsize("X")
    img_height      = (2 * padding) + (padding * len(AUTHORS))
    img_width       = (5 * padding) + (padding * NUM_WEEKS) + LONGEST_NAME + LONGEST_DATE
    im              = Image.new("RGB", (img_width, img_height))
    draw            = ImageDraw.Draw(im, "RGBA")

    draw.rectangle([(0, 0), (img_width, img_height)], fill = "#FFFFFF", outline = "#FFFFFF")

    # Draw all the names and first dates
    for author in AUTHORS:
        draw.text((padding, padding + (padding * AUTHORS.index(author))), author, fill = "black", font = FONT)
        draw.text(((padding * 2) + LONGEST_NAME, padding + (padding * AUTHORS.index(author))), 
                  str(DATES[AUTHORS.index(author)]), fill = "black", font = FONT)

    # Draw all the blobs
    for commit in LOG:
        week_num = find_week(commit['date'])
        blockX = (padding * 3) + LONGEST_NAME + LONGEST_DATE + (padding * week_num)
        blockY = padding + (padding * AUTHORS.index(commit['author_name']))
        draw.rectangle([(blockX, blockY),(blockX + padding, blockY + padding)], fill = (48, 107, 209, 64))

    del draw
    im.save("result.png", "PNG")

if __name__ == "__main__":
    create_log(sys.argv[1])
    draw_viz()
