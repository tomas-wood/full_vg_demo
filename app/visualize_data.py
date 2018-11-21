#! /usr/bin/env python
# -*- coding: utf-8

import urllib3
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from StringIO import StringIO
from visual_genome import api as vg
from PIL import Image as PIL_Image
import os
import json
import shutil
# urllib3.disable_warnings()

VG_DIR = '/app/visual_genome/'
if not os.path.exists(VG_DIR):
    VG_DIR = '../visual_genome/'
VG_IMG_DIR = VG_DIR + 'VG_100K/'

def load_region_map(fname=VG_DIR+'region_descriptions.json'):
    with open(fname,'r') as f:
        return json.load(f)

region_map = load_region_map()



def visualize_regions(image_id, regions):
    #http = urllib3.PoolManager()
    #response = http.request('GET', image.url)
    #print(image.url)
    #print(response.status)
    fname_src = VG_IMG_DIR + str(image_id) + ".jpg"
    # img = PIL_Image.open(fname)
    # plt.imshow(img)
    # ax = plt.gca()
    # for region in regions:
    #     ax.add_patch(Rectangle((region.get('x'), region.get('y')),
    #                            region.get('width'),
    #                            region.get('height'),
    #                            fill=False,
    #                            edgecolor='red',
    #                            linewidth=3))
    #     ax.text(region.get('x'),
    #             region.get('y'),
    #             region.get('phrase'),
    #             style='italic',
    #             bbox={'facecolor':'white', 'alpha':0.7, 'pad':10}
    #         )
    #
    # fig = plt.gcf()
    # plt.tick_params(labelbottom=False, labelleft=False)
    fname_dst = 'app/static/{}.png'.format(image_id)
    shutil.copy(fname_src, fname_dst)
    # print("Saving {}".format(fname))
    # plt.savefig(fname)
    # plt.gcf().clear()
    # plt.gca().clear()
    return fname_dst


def select_regions(edge, regions):
    obj1, rel, obj2 = edge
    show_me = []
    for k, x in enumerate(regions):
        phrase = x.get('phrase')
        if obj1 in phrase and obj2 in phrase and rel in phrase:
            show_me.append(k)

    return show_me

def visualize_image(image_id, edges=None, region_range="all"):
    # TODO: load in the image from ~/visual_genome/images/VG_100K/<img_id>.jpg,
    # but not here.
    # image = vg.get_image_data(id=image_id)
    fname = visualize_regions(image_id, [])
    # TODO: load in the regions from a mapping we've downloaded
    # regions = region_map.get(str(image_id))
    # fig = plt.gcf()
    # fig.set_size_inches(18.5, 10.5)
    # if edges is None:
    #     if region_range == "all":
    #         fname = visualize_regions(image_id, regions)
    #     else:
    #         start, stop = region_range
    #         fname = visualize_regions(image_id, regions[start:stop])
    # else:
    #     show_me = []
    #     for edge in edges:
    #         show_me.extend(select_regions(edge, regions))
    #     filtered_regions = [regions[k] for k in show_me]
    #     fname = visualize_regions(image_id, filtered_regions)

    return fname
