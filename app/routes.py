# -*- coding: utf-8


import json
import os
import urllib3
import certifi

from flask import render_template, flash, redirect, request, session, url_for, make_response
from app import app
from app.forms import SearchForm
from ges_search import get_results_for_edge
from visualize_data import visualize_image

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
max_num_imgs = 10

DETECTRON_URL = os.environ.get('DETECTRON_URL')
if DETECTRON_URL is None:
    DETECTRON_URL = 'detectron:8085/detectron'
SCENEGRAPH_URL = os.environ.get('SCENEGRAPH_URL')
if SCENEGRAPH_URL is None:
    SCENEGRAPH_URL = 'scene_graph:8080/sg_srvc'

print(DETECTRON_URL)
print(SCENEGRAPH_URL)


def remove_underscore(x):
    return x.split('_')[0]

def split_edge_key(x):
    return tuple(x.split('_'))

def parse_edges(subs, rels, objs):
    n = len(subs)
    edge_dict = {}
    for k in range(n):
        edge = (subs[k], rels[k], objs[k])
        edge = tuple(map(remove_underscore, edge))
        edge_key = '_'.join(edge)
        edge_dict[edge_key] = 1
    return map(split_edge_key, edge_dict.keys())


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Thomas'}
    return render_template('index.html',
            title='Visual Genome Semantic Image Search',
            user=user)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'POST':
        img_url = request.form.get('img_url', 'https://d3d00swyhr67nd.cloudfront.net/w1200h1200/STF/STF_STKMG_030.jpg')
        res = http.request('POST', DETECTRON_URL, fields={'data': img_url})
        cls_boxes = res.data
        if cls_boxes:
            sg_res = http.request('POST', SCENEGRAPH_URL, fields={'url':img_url, 'data': cls_boxes})
            # print(sg_res.status, sg_res.data)
        else:
            return make_response('That URL did not work. Try another one.')

        # I'm going on what I see in docker_flask_app/scripts/gen_sg.py
        sg_out_dict = json.loads(sg_res.data)
        subs = sg_out_dict.get('sub_list')
        objs = sg_out_dict.get('obj_list')
        rels = sg_out_dict.get('pred_list')
        if subs is None or objs is None or rels is None:
            return make_response("We aren't getting anything back from sg_srvg")
        assert len(subs) == len(objs) == len(rels)

        # Query Gremlin for the images in the database containing these edges.
        edges = parse_edges(subs, rels, objs)
        fnames = []
        for edge in edges:
	    fnames.extend(get_results_for_edge(edge))

        # Histogram to find number of times an image shows up in our search.
        fname_dict = {}
        for x in fnames:
            if x in fname_dict:
                fname_dict[x] += 1
            else:
                fname_dict[x] = 1

        # Sort results by most commonly occuring image.
        fname_list = [(fname_dict[x], x) for x in fname_dict]
        fname_list = sorted(fname_list, reverse=True)
        fname_list = [x[1] for x in fname_list]
        fname_list = fname_list[:max_num_imgs]
        for x in fname_list[:max_num_imgs]:
            visualize_image(x, edges=[edge])

        # Store these results in the session
        fname_list = [str(x) + '.png' for x in fname_list]
        # print(fname_list)
        session['fnames'] = fname_list
        return redirect(url_for('results'))
    else:
        return render_template('search.html', title='Search', form=form)#, fnames=fnames)

@app.route('/results', methods=['GET', 'POST'])
def results():
    fnames = session['fnames']
    # print(fnames)
    return render_template('results.html', fnames=fnames)
 
