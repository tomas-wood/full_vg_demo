#! /usr/bin/env python
# -*- coding: utf-8

import wget
import os
import subprocess
import shutil

imgs1_url = "https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip"
imgs2_url = "https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip"
regions_url = "https://visualgenome.org/static/data/dataset/region_descriptions.json.zip"

def fetch_data():
    dloads = [imgs1_url, imgs2_url, regions_url]
    if not os.path.exists("./visual_genome"):
        os.mkdir("./visual_genome")
        os.chdir("./visual_genome")
        fnames = []
        for url in dloads:
            fname = wget.download(url)
            fnames.append(fname)
        for fname in fnames:
            p = subprocess.Popen("unzip {}".format(fname), shell=True)
            p.communicate()
        os.chdir("visual_genome")
        src_dir = "VG_100K_2"
        dst_dir = "VG_100K"
        contents = os.listdir(src_dir)
        for img in contents:
            shutil.move("{}/{}".format(src_dir, img), "{}/{}".format(dst_dir, img))
        shutil.rmtree(src_dir)
        os.chdir("..")
    else:
        print("directory visual_genome already exists")

if __name__ == "__main__":
    fetch_data()
