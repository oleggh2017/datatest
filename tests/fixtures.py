import time
import pytest   # noqa
import docker   # noqa
from .helpers import (get_session_id,
                      ping_container,
                      load_assets_to_source_db,
                      load_struct_to_destination_db,
                      )
from settings import settings


BASE_DOCKER_IMAGE = 'percona/percona-server:5.7.32'
TIME_SLEEP = 1

class Container(object):
    def __init__(self, db_port: int, container_name: str):
        self.container = None
        self.session_id = get_session_id()
        self.docker_client = docker.client.from_env()
        self.db_port = db_port
        self.container_name = container_name

        self.credentials = {'host': 'localhost',
                            'port': self.db_port,
                            'database': 'sandbox',
                            'user': 'etl',
                            'password': 'etl_contest',
                            'autocommit': True}

        self.env = {'MYSQL_DATABASE': 'sandbox',
                    'MYSQL_USER': 'etl',
                    'MYSQL_PASSWORD': 'etl_contest',
                    'MYSQL_ROOT_PASSWORD': 'root_etl_contest'}

        self.ports = {3306: self.db_port}

    def create_container(self):
        self.container = self.docker_client.containers.run(
            image=BASE_DOCKER_IMAGE,
            ports=self.ports,
            environment=self.env,
            name=f'{self.container_name}{self.session_id}',
            detach=True)

    def get_test_container(self):
        running_containers = self.docker_client.containers.list()
        for running_container in running_containers:
            if self.container_name in running_container.name:
                return running_container

    def kill_test_container(self):
        test_db_container = self.get_test_container()
        if test_db_container:
            test_db_container.stop()
            test_db_container.remove()

    def __enter__(self):

        print(f'Run {self.session_id} on port {self.db_port}')
        self.docker_client.images.pull(BASE_DOCKER_IMAGE)

        try:
            self.create_container()
        except docker.errors.APIError:
            self.kill_test_container()
            self.create_container()

        time.sleep(TIME_SLEEP)
        ping_container(self.credentials, self.session_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.container.stop()
        time.sleep(TIME_SLEEP)
        self.docker_client.close()


@pytest.fixture(scope='session')
def mysql_source_image():
    with Container(db_port=settings.source_port, container_name='source') as c:
        load_assets_to_source_db(c.credentials)
        yield c.credentials


@pytest.fixture(scope='session')
def mysql_destination_image():
    with Container(db_port=settings.destination_port, container_name='destination') as c:
        load_struct_to_destination_db(c.credentials)
        yield c.credentials
