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
docker-compose -f deployment/development/docker-compose.yaml up -d
```

Add environmental variables to the `.env` file in the root of this project

```shell
REDIS_HOST=localhost
REDIS_PORT=6379
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
```

start task manager workers
```shell
celery -A task_manager.tasks worker
```

start the web application
```shell
uvicorn app:create_app --factory
```

Root path `/` will be redirected to `/docs` where you can play around with endpoints

![Swagger screenshot](./docs/swagger.png)


#### Global
See details about CI/CD in [.gitlab-ci.yml](../../.gitlab-ci.yml) and in [deployment/global](deployment/global)

![CI/CD workflow](./docs/ci_cd.png)

### Architecture

![Main workflow](./docs/architecture.png)


