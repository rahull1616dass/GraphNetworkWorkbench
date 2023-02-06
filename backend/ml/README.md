### Installation
#### Local

install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

clone the repo
```shell
git clone git@gitlab2.informatik.uni-wuerzburg.de:xtai_lab2/xtai_lab3.git
cd xtai_lab3/backend/ml
```

create new environment
```shell
conda env create --file requirements.yaml --name <env_name>
```

activate environment
```
conda activate <env_name>
```

install [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/)

start [redis](https://redis.io/) and [rabbitmq](https://www.rabbitmq.com/)
```shell
docker-compose up -f deployment/development/docker-compose.yaml -d
```

start task manager workers
```shell
celery -A task_manager_queue.tasks worker
```

start the web application
```shell
uvicorn app:create_app --factory
```

Root path `/` will be redirected to `/docs` where you can play around with endpoints

![Swagger screenshot](./docs/swagger.png)


#### Global
See details about CI/CD in [.gitlab-ci.yml](../../.gitlab-ci.yml) and in [deployment/global](deployment/global)

### Architecture

![Main workflow](./docs/architecture.png)


