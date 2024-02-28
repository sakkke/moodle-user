from fastapi import FastAPI
from moodle_user_client import moodle_user

app = FastAPI()

@app.get('/api/v1/courses')
def get_courses():
    return moodle_user.get_courses()