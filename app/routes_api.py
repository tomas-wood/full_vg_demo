# -*- coding: utf-8


import json
import os
import urllib3
import certifi

from flask import (
    render_template,
    flash,
    redirect,
    request,
    session,
    url_for,
    make_response,
    jsonify
    )
from flask_restful import Resource, Api
from app import app
from ges_search import get_results_for_edge
from visualize_data import visualize_image

api = Api(app)

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
max_num_imgs = 10

DETECTRON_URL = os.environ.get('DETECTRON_URL')
if DETECTRON_URL is None:
    # Using docker-compose
    DETECTRON_URL = 'detectron:8085/detectron'
    # Outside docker
    # DETECTRON_URL = '0.0.0.0:8085/detectron'
SCENEGRAPH_URL = os.environ.get('SCENEGRAPH_URL')
if SCENEGRAPH_URL is None:
    # Using docker-compose
    SCENEGRAPH_URL = 'scene_graph:8080/sg_srvc'
    # Outside docker
    #SCENEGRAPH_URL = '0.0.0.0:8080/sg_srvc'

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

def gather_query_results(edges):
    fnames = []
    for edge in edges:
        fnames.extend(get_results_for_edge(edge))
    fname_dict = {}
    for x in fnames:
        if x in fname_dict:
            fname_dict[x] += 1
        else:
            fname_dict[x] = 1
    fname_list = [(fname_dict[x], x) for x in fname_dict]
    fname_list = sorted(fname_list, reverse=True)
    fname_list = [x[1] for x in fname_list]
    fname_list = fname_list[:max_num_imgs]
    for x in fname_list:
        visualize_image(x, edges=[edge])

    return ["{}.png".format(x) for x in fname_list]


class SemanticSearchImage(Resource):
    def post(self):
        img_url = request.form["data"]
        res = http.request("POST", DETECTRON_URL, fields={"data": img_url})

        if res.status == 200:
            cls_boxes = res.data
        else:
            print("We didn't get a 200 response from detectron")
            return jsonify([])

        if cls_boxes:
            sg_res = http.request("POST", SCENEGRAPH_URL, fields={"url": img_url, "data":cls_boxes})
        else:
            print("So we got a 200 response from detectron but cls_boxes is None")
            return jsonify([])

        if sg_res.status == 200:
            sg_out_dict = json.loads(sg_res.data)
            subs = sg_out_dict.get('sub_list')
            objs = sg_out_dict.get('obj_list')
            rels = sg_out_dict.get('pred_list')
            if not ( subs and objs and rels):
                return jsonify([])
            assert len(subs) == len(objs) == len(rels)

        else:
            print("We didn't get a 200 status from sg_res. Returning empty list")
            return jsonify([])

        edges = parse_edges(subs, rels, objs)
        print(edges)
        fnames = gather_query_results(edges)
        return jsonify(fnames)


class SemanticSearchText(Resource):
    def post(self):
        edges_raw = request.form["data"]
        edges = json.loads(edges_raw)
        fnames = gather_query_results(edges)
        return jsonify(fnames)

api.add_resource(SemanticSearchImage, "/image_search")
api.add_resource(SemanticSearchText, "/text_search")
