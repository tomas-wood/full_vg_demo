import urllib3
import json
import certifi
from visualize_data import visualize_image
import os

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

token = os.environ['GES_API_TOKEN']

# Headers are how we pass through the token.
headers = {"Content-Type":"application/json"}
headers["X-Language"] = "en-us"
headers["X-Auth-Token"] = token

my_project_id = "bb4478f419c34cd7889b0ab8639e81e6"
my_graph_id = "98d86aeb-1f84-4178-ac50-d034c1adb8bc"
my_region = "ges.cn-north-1"

# action = "start"
# action = "stop"
action = "execute-gremlin-query"

base = "{}.myhuaweicloud.com".format(my_region)
url = "https://{}/v1.0/{}/graphs/{}/action?action_id={}".format(
    base, my_project_id, my_graph_id, action
    )


def query_for_edge(edge):
    obj1, rel, obj2 = edge
    print(edge)
    query = \
    "g.V().has('LabelName', '{}').\
    outE().has('Predicate', '{}').\
    inV().has('LabelName', '{}').\
    values('ImageID')".format(
        obj1, rel, obj2
    )
    data = {"command":query}
    #print(json.dumps(data))
    r = http.request("POST", url, headers=headers, body=json.dumps(data))
    #print(r.status)
    # We don't want a JSON string. We want a python dictionary.
    output = json.loads(r.data)
    res = output.get('data')
    if res is None:
        print("You've got to set GES_TOKEN_API to a valid token")
        return None
    else:
        outputs = res.get("outputs")[:-1]
        if outputs is None:
             print("something wrong with getting the outputs")
             return None
    return list(set(outputs))


def get_results_for_edge(edge):
    q = query_for_edge(edge)
    fnames = []
    if len(q) < 1:
        print("Have you set GES_API_TOKEN?")
        return []
    for x in q:
        print(x)
        #fnames.append(visualize_image(x, edges=[edge]))
        #print("Error in creating visualization for edge {}. Continuing.".format(edge))
        fnames.append(x)
    print(edge)
    print(q)
    # fnames = [fname.split('/')[-1] for fname in fnames]
    return fnames
