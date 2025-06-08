#!/bin/bash

# Install dependencies
if [ -f "package.json" ]; then
  npm install
fi

if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi

if [ -f "Pipfile" ]; then
  pipenv install
fi

if [ -f "Gemfile" ]; then
  bundle install
fi

if [ -f "Makefile" ]; then
  make install
fi

# Run the codebase
if [ -f "package.json" ]; then
  npm start &
fi

if [ -f "manage.py" ]; then
  python manage.py runserver &
fi

if [ -f "app.py" ]; then
  python app.py &
fi

if [ -f "main.py" ]; then
  python main.py &
fi

if [ -f "index.js" ]; then
  node index.js &
fi

wait
