#! /usr/bin/env python
# -*- coding: utf-8

import urllib3
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from StringIO import StringIO
from visual_genome import api as vg
from PIL import Image as PIL_Image
urllib3.disable_warnings()

def visualize_regions(image, regions):
    http = urllib3.PoolManager()
    response = http.request('GET', image.url)
    img = PIL_Image.open(StringIO(response.data))
    plt.imshow(img)
    ax = plt.gca()
    for region in regions:
        ax.add_patch(Rectangle((region.x, region.y),
                               region.width,
                               region.height,
                               fill=False,
                               edgecolor='red',
                               linewidth=3))
        ax.text(region.x,
                region.y,
                region.phrase,
                style='italic',
                bbox={'facecolor':'white', 'alpha':0.7, 'pad':10}
            )

    fig = plt.gcf()
    plt.tick_params(labelbottom=False, labelleft=False)
    fname = 'app/static/{}.png'.format(image.id)
    print("Saving {}".format(fname))
    plt.savefig(fname)
    plt.gcf().clear()
    plt.gca().clear()
    return fname


def select_regions(edge, regions):
    obj1, rel, obj2 = edge
    show_me = []
    for k, x in enumerate(regions):
        phrase = x.phrase
        if obj1 in phrase and obj2 in phrase and rel in phrase:
            show_me.append(k)

    return show_me

def visualize_image(image_id, edges=None, region_range="all"):
    image = vg.get_image_data(id=image_id)
    regions = vg.get_region_descriptions_of_image(id=image_id)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    if edges is None:
        if region_range == "all":
            fname = visualize_regions(image, regions)
        else:
            start, stop = region_range
            fname = visualize_regions(image, regions[start:stop])
    else:
        show_me = []
        for edge in edges:
            show_me.extend(select_regions(edge, regions))
        filtered_regions = [regions[k] for k in show_me]
        fname = visualize_regions(image, filtered_regions)

    return fname
