import os
import subprocess
import socket
import sys
import shutil
from argparse import ArgumentParser
import time

dirname = os.path.dirname(os.path.abspath(__file__))

class PortInUseError(BaseException):
    """Base class for other exceptions"""
    def __init__(self,value):
        self.value = value


class DockerNameInUse(BaseException):

    def __init__(self,value):
        self.value = value


class BlazegraphLoad():
    def __init__(self,ttl_path,wikibase_ui_port,wikibase_sparql,wikibase_proxy,wikibase_qs,wikibase_volume,
                 create_new,docker_name,stop_docker,blazegraph_image):
        self.ttl_path = os.path.join(dirname,ttl_path)
        self.wikibase_ui_port = wikibase_ui_port
        self.wikibase_sparql = wikibase_sparql
        self.wikibase_proxy = wikibase_proxy
        self.wikibase_qs = wikibase_qs
        self.wikibase_volume = wikibase_volume
        self.create_new = create_new
        self.docker_name = docker_name
        self.stop_docker = stop_docker
        self.blazegraph_image = blazegraph_image
        os.environ['WIKIBASE_UI'] = self.wikibase_ui_port
        os.environ['WIKIBASE_SPARQL'] = self.wikibase_sparql
        os.environ['WIKIBASE_PROXY'] = self.wikibase_proxy
        os.environ['WIKIBASE_QS'] = self.wikibase_qs
        os.environ['WIKIBASE_VOLUME'] = self.wikibase_volume
        os.environ['BLAZEGRAPH_IMAGE'] = self.blazegraph_image

    def check_availability(self):

        wikibase_ui = os.getenv('WIKIBASE_UI')
        wikibase_sparql = os.getenv('WIKIBASE_SPARQL')
        wikibase_proxy = os.getenv('WIKIBASE_PROXY')
        wikibase_qs = os.getenv('WIKIBASE_QS')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            wikibase_ui_usage = s.connect_ex(('localhost', int(wikibase_ui))) == 0
            wikibase_sparql_usage = s.connect_ex(('localhost', int(wikibase_sparql))) == 0
            wikibase_proxy_usage = s.connect_ex(('localhost', int(wikibase_proxy))) == 0
            wikibase_qs_usage = s.connect_ex(('localhost', int(wikibase_qs))) == 0
        docker_name_availability = subprocess.Popen(['docker', 'ps', '--filter', 'name={}'.format(self.docker_name)],
                                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            if self.create_new:
                if wikibase_ui_usage:
                    raise PortInUseError('Wikibase UI Port is in use')
                if wikibase_sparql_usage:
                    raise PortInUseError('Wikibase Sparql Port is in use')
                if wikibase_proxy_usage:
                    raise PortInUseError('Wikibase Proxy Port is in use')
                if wikibase_qs_usage:
                    raise PortInUseError('Wikibase QS Port is in use')
            if len(docker_name_availability.communicate()[0]) > 126:
                raise DockerNameInUse('Try changing docker container name')
            print(docker_name_availability)
        except PortInUseError as Argument:
            raise ('Error Message:', Argument)
            sys.exit(1)

        except DockerNameInUse as Argument:
            raise ('Error Message:', Argument)
            sys.exit(1)
        return True

    def load_data(self):
        l_data = subprocess.Popen(
            ['docker', 'exec', '{}_wdqs_1'.format(self.docker_name), '/wdqs/loadData.sh', '-n', 'wdq', '-d',
             '/instancestore/wikibase/mungeOut'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print(l_data.communicate()[0])

    def driver_fn(self):
        if self.create_new:
            all_parameters = self.check_availability()
            if all_parameters:
                create_docker = subprocess.Popen(
                    ['docker-compose', '-f', 'docker-compose.pipeline.yml', '-p', self.docker_name, 'up', '-d'],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                create_docker.communicate()

        if self.stop_docker == 'Yes' or self.stop_docker == 'yes':
            docker_stop = subprocess.Popen(
                ['docker-compose', '-f', 'docker-compose.pipeline.yml', '-p', self.docker_name, 'down', '-v'],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            docker_stop.communicate()
            sys.exit(1)

        if os.path.isdir(os.getenv('WIKIBASE_VOLUME') + '/mungeOut'):
            shutil.copy(self.ttl_path, os.path.join(os.getenv('WIKIBASE_VOLUME'), 'mungeOut/wikidump-000000001.ttl.gz'))
        else:
            os.mkdir(os.path.join(os.getenv('WIKIBASE_VOLUME'), 'mungeOut'))
            shutil.copy(self.ttl_path, os.path.join(os.getenv('WIKIBASE_VOLUME'), 'mungeOut/wikidump-000000001.ttl.gz'))

        time.sleep(40)

        print('Sleep time over; Loading started')

        self.load_data()
        os.remove(os.path.join(os.getenv('WIKIBASE_VOLUME'), 'mungeOut/wikidump-000000001.ttl.gz'))


def generate_arguments():
    parser = ArgumentParser()
    parser.add_argument('--wikibase_ui_port',help='Port on which wikibase UI should run',default='10001')
    parser.add_argument('--wikibase_sparql',help='Port on which wikibase SPARQL should run',default='10002')
    parser.add_argument('--wikibase_proxy',help='Port on which wikibase proxy should run',default='10003')
    parser.add_argument('--wikibase_qs',help='Port on which wikibase QS should run',default='10005')
    parser.add_argument('--wikibase_volume',help='Volume path on which the Blazegraph docker image should be mounted',default=os.path.join(dirname,'volume'))
    parser.add_argument('--create_new',help='Should a new docker container be created, True or False',default=False)
    parser.add_argument('ttl_path',help='Path of the ttl file that needs to be loaded')
    parser.add_argument('--docker_name',help='Name the docker container',default='blazegraphpipeline')
    parser.add_argument('--stop_docker_container',help = 'To stop custom docker, pass the port numbers as well. If used '
                                                         'standalone, it will stop the default running docker', default='No')
    parser.add_argument('--blazegraph_image',help='Name of the default blazegraph image to use',default='wikibase/wdqs:0.3.10')
    return parser


if __name__ == '__main__':
    parser = generate_arguments()
    args = parser.parse_args()
    wikibase_ui_port = args.wikibase_ui_port
    wikibase_sparql_port = args.wikibase_sparql
    wikibase_proxy_port = args.wikibase_proxy
    wikibase_qs_port = args.wikibase_qs
    wikibase_volume = args.wikibase_volume
    create_new = args.create_new
    ttl_path = args.ttl_path
    docker_name = args.docker_name
    stop_docker = args.stop_docker_container
    blazegraph_image = args.blazegraph_image
    loader_obj = BlazegraphLoad(ttl_path,wikibase_ui_port,wikibase_sparql_port,wikibase_proxy_port,wikibase_qs_port,
                                wikibase_volume,create_new,docker_name,stop_docker,blazegraph_image)
    loader_obj.driver_fn()