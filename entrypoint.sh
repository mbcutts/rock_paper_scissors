#!/bin/bash
service nginx start
cd /app
gunicorn --bind unix:/app/gunicorn.sock main:app