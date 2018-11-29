### Install
1. Run `python download_vg.py` from the command line to download the visual
genome dataset.
2. Generate a GES API token using the technique found [here](https://github.com/huawei-tomas/genauth_gesapi)
and set the environmental variable `GES_API_TOKEN` to the token value with a 
command like `export GES_API_TOKEN=cat /path/to/token` but with the appropriate characters around `cat path/to/token`. 
Email me to get the environmental variables needed to access the GES API. It's easiest to place them
in a file like `/path/to/genauth_gesapi/.ges_environ` and source the file before
generating an authorization key or turning the GES graph on or off with python test.py -a start.
<!-- 3. Clone https://github.com/huawei-tomas/detectron_service, cd into 
detectron_service, and run 
```
nvidia-docker build -t odellus/detectron_srvc:version10 .
```
to build a local version of the detectron service (having trouble pushing to 
DockerHub because of a known [issue](https://github.com/docker/for-mac/issues/1396).-->  
3. Change the line in docker-compose.yml from /home/thomas/code/visual_genome to the absolute path of visual genome at `../visual_genome`.
3 and a half. If you are using CUDA 9.0 then change the docker-compose.yml to pull odellus/detectron_srvc:version10 (or :version11).
4. Run `docker-compose up` to build the web server and pull the detectron 
and scene graph services from DockerHub*.  

*This step is still untested.
