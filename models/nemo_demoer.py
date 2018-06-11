from mongoengine import Document, StringField

class Demoer(Document):
    user_id = StringField(required=True)
    password = StringField(required=True)
    household_id = StringField(required=True)
    container_url = StringField(required=True)