#!/bin/bash
exec uv run --quiet --with fonttools --with brotli --with shapely --with playwright==1.63.0 --with pillow --with numpy --with opencv-python-headless --python 3.12 python "$@"
