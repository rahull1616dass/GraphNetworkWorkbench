### Installation
#### Local installation

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
docker-compose up -f deployment/local/docker-compose.yaml -d
```

start task manager workers
```shell
celery -A task_manager_queue worker
```

start the web application
```shell
uvicorn app:create_app --factory
```

#### Global deployment
See details about CI/CD in [.gitlab-ci.yml](https://gitlab2.informatik.uni-wuerzburg.de/xtai_lab2/xtai_lab3/-/blob/main/.gitlab-ci.yml) and in [deployment/global]()

### 1. Write App (Flask, TensorFlow)
- The code to build, train, and save the model is in the `test` folder.
- Implement the app in `main.py`
### 2. Setup Google Cloud 
- Create new project
- Activate Cloud Run API and Cloud Build API

### 3. Install and init Google Cloud SDK
- https://cloud.google.com/sdk/docs/install

### 4. Dockerfile, requirements.txt, .dockerignore
- https://cloud.google.com/run/docs/quickstarts/build-and-deploy#containerizing

### 5. Cloud build & deploy
```
gcloud builds submit --tag gcr.io/graphlearningworkbench/index
gcloud run deploy --image gcr.io/graphlearningworkbench/index --platform managed
```

### Test
- Test the code with `test/test.py`

### Watch the video tutorial
- How To Deploy ML Models With Google Cloud Run

[![Alt text](https://img.youtube.com/vi/vieoHqt7pxo/hqdefault.jpg)](https://youtu.be/vieoHqt7pxo)
