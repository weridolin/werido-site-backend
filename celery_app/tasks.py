import os,sys
from core.celery import app

@app.task(name="celeryTask.remove_file")
def remove_file(file_path): 
    if isinstance(file_path,list):
        for path in file_path:
            if os.path.exists(path):
                os.remove(path)
    else:
        if os.path.exists(file_path):
            os.remove(file_path)