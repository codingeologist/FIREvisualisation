# Welcome to FIRE visualisation webapp!

Hi, this is my little project for web visualisation and local database management with CRUD. I have used my python, HTML, CSS (mainly bootstrap), Flask module, SQLalchemy and Plolty.

# Setup venv
``` bash
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

# Build Docker Image
- build docker image with tag:$version
```bash
export APP_VERSION=0.1
docker build --tag firetracker:$APP_VERSION .
```

- show docker images list
```bash
docker images
```

- run docker image
```bash
docker run -d -p 5100:5100 firetracker:$APP_VERSION
```

# Localhost server
- [host: localhost port: 5000](http://localhost/5000)
- testing username/password: admin/admin

# Things to do

1. Replace password with password hash
2. align graphs in nice grid form (I was banging my head with aligning with bootstrap)
3. Create requirement.txt. Fortunately, pythonanywhere has built-in modules installed, so I did not install or specify and modules.
4. Write clean code

# NOTES 

## TODO
1. Make sqlite database persistent. ✅
2. Refactor login pipeline.
3. Refactor database, analysis classes. ✅
4. Dockerise app. ✅
