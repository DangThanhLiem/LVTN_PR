import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize_firebase():
    cred = credentials.Certificate("D:\LVTN_FR\serviceAccountKey.json")
    firebase_admin.initialize_app(cred,{
         'projectId': 'face-recognitionb2014580'
    })
    db = firestore.client()
    return db
