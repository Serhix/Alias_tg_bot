from mongoengine import connect
from src.conf.config import settings

connect(host=settings.database_url, ssl=True)