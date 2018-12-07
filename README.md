### Install
1. Run `python download_vg.py` from the command line to download the visual
genome dataset.
2. Generate a GES API token using the technique found [here](https://github.com/huawei-tomas/GES-API)
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
3. Change the line in docker-compose.yml from /home/thomas/code/visual_genome to the absolute path of visual genome at `../visual_genome`. If you are using CUDA 9.0 then change the docker-compose.yml to pull odellus/detectron_srvc:version10 (or :version11).
4. Run `docker-compose up` to build the web server and pull the detectron 
and scene graph services from DockerHub.
5. Point your client to 0.0.0.0:5000/search to access the demo API.

<!-- 
https://d3d00swyhr67nd.cloudfront.net/w1200h1200/STF/STF_STKMG_030.jpg
https://media-cdn.tripadvisor.com/media/photo-s/04/35/6f/4e/vilamendhoo-island-resort.jpg
http://www.performancewatersports.com/img/moomba-boats.jpg
https://www.thenewsminute.com/sites/default/files/styles/news_detail/public/Kamali_surfergirl_7_750_JamieThomas.jpg?itok=DIpEaX8B
https://images.pexels.com/photos/257894/pexels-photo-257894.jpeg
-->
