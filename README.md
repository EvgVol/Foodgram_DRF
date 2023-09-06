# Foodgram - service for publishing and sharing recipes.
[![Certbot](https://img.shields.io/badge/-Certbot-003A6E?style=flat&logo=letsencrypt&logoColor=white)](https://certbot.eff.org/)
[![Workflow](https://github.com/EvgVol/foodgram_drf/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/evgvol//foodgram_drf/actions/workflows/foodgram_workflow.yml)
[![Python Version](https://img.shields.io/badge/Python-v3.11-blue)](https://www.python.org/downloads/release/python-3110/)
[![Django](https://img.shields.io/badge/Django-v4.2-green)](https://docs.djangoproject.com/en/4.2/)
[![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-v3.12-green)](https://www.django-rest-framework.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/-Docker_Compose-384d54?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13.0-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![codecov](https://codecov.io/gh/EvgVol/foodgram-project-react/branch/master/graph/badge.svg?token=FKKAKXU90C)](https://codecov.io/gh/EvgVol/foodgram-project-react)

```bash
.
│
├─ .github                     # Github Actions configuration
│   └─ workflows
│       └─ foodgram_workflow.yml
│
├─ backend                     # Directory for the backend part of the project
│   ├── users                  # Application related to users
│   ├── recipes                # Application related to recipes
│   ├── data                   # Static files for importing ingredients and tags
│   ├── backend                # Root settings and project configurations
│   ├── api                    # API endpoints, schemas, and serializers
│   ├── manage.py              # Django management file
│   ├── requirements.txt       # Dependencies for the project
│   ├── Dockerfile             # Dockerfile for building the backend image
│   ├── .gitkeep               # Empty file to keep the directory in Git
│   └── .env                   # File with confidential settings
│
├─ frontend                    # Directory for the frontend part of the project
│   ├── src                    # Main structure of React components
│   ├── public                 # Public files, such as the source index.html
│   ├── yarn.lock              # Dependencies and versions for yarn
│   ├── package.json           # Configuration file for Node.js project
│   └── Dockerfile             # Dockerfile for building the frontend image
│
├─ infra                       # Directory for infrastructure resources
│   ├── docker-compose.yml     # File for local deployment of the project
│   └── nginx.conf             # Configuration for the Nginx server
│
├─ tests                       # Directory for project tests
│   ├── fixtures               # Fixtures for pytest
│   ├── conftest.py            # Global pytest fixtures
│   ├── test_dockerfile.py     # Tests for Dockerfile
│   ├── test_favorite.py       # Tests for favorites
│   ├── test_following.py      # Tests for subscriptions
│   ├── test_ingredients.py    # Tests for ingredients
│   ├── test_recipes.py        # Tests for recipes
│   ├── test_requirements.py   # Tests for dependencies
│   ├── test_shopping.py       # Tests for shopping lists
│   ├── test_tags.py           # Tests for tags
│   └── test_users.py          # Tests for users
│
├─ .coverage                   # Code coverage report file
├─ .gitignore                  # File to specify Git ignored files/directories
├─ LICENSE.md                  # Project license
├─ pytest.ini                  # Configuration file for pytest
├─ README.md                   # Description and instructions for the project
└─ setup.cfg                   # Common settings for tools
```


# Descriptions
Service for publishing and sharing recipes.
Authorized users can subscribe to their favorite authors, add recipes to their favorites and shopping list, and download the shopping list. Unregistered users have access to registration, authorization, and viewing other users' recipes.

#

## Server Preparation

```bash
# In Settings - Secrets and variables, we create a variable with your data
# This is necessary to work with CI/CD, DockerHub, GitHub
SECRET_KEY='django-insecure-284jnm=8n5j4^#kfmroc%=@nj+qke7#n$gw54y0iba1-&##f(d'
DEBUG=False
ALLOWED_HOSTS='127.0.0.1, .localhost, 011.222.333.444'
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
DB_HOST='db'
DB_PORT=5432
HOST=011.222.333.444
USER=admin
PASSWORD=password
SSH_KEY='<< private SSH key >>'
DOCKER_USERNAME='login from DOCKER'
DOCKER_PASSWORD='password from DOCKER'

##to use SQLite3 database, specify: MODE=dev
```

We will perform all actions in Docker, docker-compose both on the local machine and on the Yandex.Cloud VM server.
We will pre-install the necessary components for work on the VM in the cloud:

*1. Connect to your server*

```bash
ssh admin@011.222.333.444
# admin: the name of the user under which the connection to the server will be made
# 011.222.333.444: Server IP address
```

*2. First update the existing package list:*

```bash
sudo apt update
```

*3. Now update the packages installed in the system and install security updates: the system was installed on your server from the internal repository of Yandex.Cloud, and it is unknown when it was updated. Trust, but update:*

```bash
sudo apt upgrade -y
```

*3. Install Docker on your server:*

```bash
sudo apt install docker.io
```

*4. The following command downloads version 1.26.0 and saves the executable file in the /usr/local/bin/docker-compose directory, as a result of which this software will be globally available under the name docker-compose:*

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

*5. Then you need to set the correct permissions to make the docker-compose command executable:*
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

*6. To check the success of the installation, run the following command:*

```bash
docker-compose --version
# The output will look like this:
#docker-compose version 1.26.0, build 8a1c60f6
```

*6. Copy the docker-compose files.yaml and nginx/default.conf from your project to the server in home/<your_isegame>/docker-compose.yaml and home/<your_isegame>/nginx/default.conf, respectively.:*

```bash
#These files need to be copied from the infra directory of the local
scp docker-compose machine.yml nginx.conf admin@011.222.333.444:/home/admin/
```
## Launch

The git push command is the project workflow trigger. When executing the git push command, a set of jobs command blocks will be launched (see the file [Workflow](https://github.com/EvgVol/Foodgram_DRF/actions/workflows/foodgram_workflow.yml)). The following blocks will be executed sequentially:

**build_and_push_to_docker_hub** - upon successful completion of the tests, an image is collected for the docker container and sent to DockerHub

**deploy** - after sending the image to DockerHub, the deployment of the project on the server begins.

After completing the above procedures, you need to establish a connection to the server:

```bash
ssh admin@011.222.333.444
```

Execute the commands one by one:

```bash
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py importcsv
```

The project is now available at http://011.222.333.444/.
[![example](https://raw.githubusercontent.com/EvgVol/foodgram_drf/master/animation.gif)]()
#

## The Chicken or the Egg?

Download the script to your working directory as init-letsencrypt.sh:

```bash
cd infra/
curl -L https://raw.githubusercontent.com/wmnnd/nginx-certbot/master/init-letsencrypt.sh > init-letsencrypt.sh
```
Edit the script to add in your domain(s) and your email address. If you’ve changed the directories of the shared Docker volumes, make sure you also adjust the data_path variable as well.

Then run:
```bash
chmod +x init-letsencrypt.sh
``` 
and

```bash
sudo ./init-letsencrypt.sh
```

Everything is in place now. The initial certificates have been obtained and our containers are ready to launch. Simply run docker-compose up and enjoy your HTTPS-secured website or app.

The project is now available at https://011.222.333.444/.


## Documentation to API   
To open the documentation locally, start the server and follow the link:
[http://011.222.333.444/api/docs/](http://011.222.333.444/api/docs/) or use the board on my server: [REDOC](https://ifood.sytes.net/api/docs/)

#  

## Test coverage

![codecov](https://codecov.io/gh/EvgVol/foodgram-project-react/branch/master/graphs/sunburst.svg?token=FKKAKXU90C)


</b></details>
<details>
<summary>What do I need to do to install a badge covering a project with tests? </summary><br><b>

*  #### 1. Register on the service: [codecov.io](https://codecov.io)


* #### 2. Configure integration, add a step to send data to the service
  #### Adding CODECOV_TOKEN to the secrets of this repository
  #### #### Below is the code that needs to be added to foodgram_workflow.yml (for a more complete example, see [here](https://github.com/codecov/codecov-action#usage )):
```bash
    - name: Upload coverage reports to Codecov
      uses: codecov/codecov-action@v2
      with:
        token: ${{ secrets.CODECOV_TOKEN }}
        files: ./coverage.xml
        flags: pytest
        name: foodgram-pytest-cov
        env_vars: OS,PYTHON
        fail_ci_if_error: true
        verbose: true
```

* #### 3. As soon as you make a pull request, you can get an analysis of the test coverage on the service [codecov.io ](https://codecov.io )


</b></details>



#            
