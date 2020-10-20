import os
import subprocess
import socket
import sys
import shutil
from argparse import ArgumentParser
import time

dirname = os.path.dirname(os.path.abspath(__file__))

class BlazegraphLoad():
    def __init__(self,wikibase_ui_port,wikibase_sparql,wikibase_proxy,wikibase_qs,wikibase_volume,
                 docker_name,blazegraph_image):
        #self.ttl_path = os.path.join(dirname,ttl_path)
        self.wikibase_ui_port = wikibase_ui_port
        self.wikibase_sparql = wikibase_sparql
        self.wikibase_proxy = wikibase_proxy
        self.wikibase_qs = wikibase_qs
        self.wikibase_volume = wikibase_volume
        #self.create_new = create_new
        self.docker_name = docker_name
        #self.stop_docker = stop_docker
        self.blazegraph_image = blazegraph_image
        os.environ['WIKIBASE_UI'] = self.wikibase_ui_port
        os.environ['WIKIBASE_SPARQL'] = self.wikibase_sparql
        os.environ['WIKIBASE_PROXY'] = self.wikibase_proxy
        os.environ['WIKIBASE_QS'] = self.wikibase_qs
        os.environ['WIKIBASE_VOLUME'] = self.wikibase_volume
        os.environ['BLAZEGRAPH_IMAGE'] = self.blazegraph_image


    def driver_fn(self):

        
        docker_stop = subprocess.Popen(
            ['docker-compose', '-f', 'docker-compose.pipeline.yml', '-p', docker_name, 'down', '-v'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        docker_stop.communicate()
        sys.exit(1)


def generate_arguments():
    parser = ArgumentParser()
    parser.add_argument('--wikibase_ui_port',help='Port on which wikibase UI should run',default='10001')
    parser.add_argument('--wikibase_sparql',help='Port on which wikibase SPARQL should run',default='10002')
    parser.add_argument('--wikibase_proxy',help='Port on which wikibase proxy should run',default='10003')
    parser.add_argument('--wikibase_qs',help='Port on which wikibase QS should run',default='10005')
    parser.add_argument('--wikibase_volume',help='Volume path on which the Blazegraph docker image should be mounted',default=os.path.join(dirname,'volume'))
    parser.add_argument('--docker_name',help='Name the docker container',default='blazegraphpipeline')
    '''parser.add_argument('--stop_docker_container',help = 'To stop custom docker, pass the port numbers as well. If used '
                                                         'standalone, it will stop the default running docker', default='yes')'''
    parser.add_argument('--blazegraph_image',help='Image Name of blazegraph to be used',default='wikibase/wdqs:0.3.10')
    return parser


if __name__ == '__main__':
    parser = generate_arguments()
    args = parser.parse_args()
    wikibase_ui_port = args.wikibase_ui_port
    wikibase_sparql_port = args.wikibase_sparql
    wikibase_proxy_port = args.wikibase_proxy
    wikibase_qs_port = args.wikibase_qs
    wikibase_volume = args.wikibase_volume
    docker_name = args.docker_name
    blazegraph_image = args.blazegraph_image
    loader_obj = BlazegraphLoad(wikibase_ui_port,wikibase_sparql_port,wikibase_proxy_port,wikibase_qs_port,
                                wikibase_volume,docker_name,blazegraph_image)
    loader_obj.driver_fn()