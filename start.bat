@echo off
cd /d "%~dp0"
echo Open http://localhost:8302 in your browser (Ctrl+C to stop)
start "" http://localhost:8302
python serve.py 8302
