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

## Setup Instructions

In order to run this project locally, you must enter the following command in the terminal at the project root directory.

```
docker compose up
```