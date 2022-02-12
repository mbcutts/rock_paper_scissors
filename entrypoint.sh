#!/bin/bash
service nginx start
gunicorn --bind 0.0.0.0:5000 manage:app