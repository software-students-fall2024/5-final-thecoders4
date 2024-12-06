# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

![CI](https://github.com/software-students-fall2024/5-final-thecoders4/actions/workflows/build.yml/badge.svg)

## Team members

* Wilson Xu [Profile](https://github.com/wilsonxu101)
* Hanna Han [Profile](https://github.com/HannaHan2)
* Sewon Kim [Profile](https://github.com/SewonKim0)
* Rhan Chen [Profile](https://github.com/xc528)

## Description

A web application designed to help users find the ideal dog breed based on their preferences and lifestyle. The app will present users with a series of questions about key dog traits, such as trainability, friendliness, energy level, and compatibility with children or other pets. Based on their responses, the app will recommend several suitable dog breeds, providing detailed information about each breed. If the app is unable to recommend a suitable breed, users will be encouraged to try again until a match is found.

## Docker Images

Provided below is a link to our custom docker image for the web-app subsystem.

[Docker Image Link](https://hub.docker.com/r/hannahan2/web-app)

## Run the software as users

Open a web browser and go to [link](http://165.227.79.238:5001/)

## Test and run the software as developers

1. Clone this repository to the editor in your computer

2. Set up a virtual environment and install dependencies: 
```
pip install pipenv
pipenv install
pipenv shell
```

3. Run tests and check the code coverage:

```
coverage run -m pytest
coverage report -m
```

4. Install and run the ```Docker Desktop```

5. Run the app: 
```
docker-compose up
```

6. View the app in your browser: 

open a web browser and go to [link](http://127.0.0.1:5001)