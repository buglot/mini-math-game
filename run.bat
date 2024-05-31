@ECHO OFF
echo new venv
python -m venv .env
\env\Scripts\activate
pip install -r requirement.txt
python app.py
PAUSE
