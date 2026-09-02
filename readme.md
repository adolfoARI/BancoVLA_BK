Remove-Item -Recurse -Force venv 
py -3.13 -m venv venv  
.\venv\Scripts\Activate.ps1  
pip install -r requirements.txt   
python manage.py runserver           