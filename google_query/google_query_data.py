# -*- coding: UTF-8 -*-
import json
import os

regions, regions_coords = None, None

file_dir = os.path.split(os.path.realpath(__file__))[0]
if regions is None:
    with open(os.path.join(file_dir, 'regions.json'), 'r') as fin:
        text = fin.read()
        regions = json.loads(text)
if regions_coords is None:
    with open(os.path.join(file_dir, 'regions_coords.json'), 'r') as fin:
        text = fin.read()
        regions_coords = json.loads(text)
