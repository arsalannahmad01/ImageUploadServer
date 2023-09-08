import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb+srv://arsalan:arsalan01@cluster0.zftx9hl.mongodb.net/Images?retryWrites=true&w=majority'