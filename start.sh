#!/bin/bash
pkill -f gunicorn
gunicorn -w 1 -k sync -b 0.0.0.0:5000 app:app \
-D \
--access-logfile gunicorn.log \
--error-logfile gunicorn.log \
--capture-output \
--env PYTHONUNBUFFERED=1
