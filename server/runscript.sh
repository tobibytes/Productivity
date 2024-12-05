#!/bin/bash

cd services
cd authService
echo ".git" > .dockerignore
cd ..
cd googleService
echo ".git" > .dockerignore

cd ..
cd notionService
echo ".git" > .dockerignore
cd ..
cd slackService
echo ".git" > .dockerignore

cd ..
cd githubService
echo ".git" > .dockerignore

cd ..
