from mongoengine import *
from models.nemo_demoer import Demoer
import validators

class NemoDemoerMongoDBClient(object):
    def enroll_demoer(self, user_id, password, household_id, container_url):
        if not user_id:
            return "No user ID provided with enroll request"
        if not password:
            return "Please specify a secure password for this user"
        if not household_id:
            return "Please specify the VocalPassword household_id connected to this demo instance user"
        if not container_url:
            return "URL missing for demo instance!"

        if validators.url(container_url) == False:
            return "Invalid URL. Please enter in the format: http://www.nuance.com"

        if self.check_user_exists == True:
            return "Unable to enroll! User ID already exists"
        else:
            try:
                Demoer.objects(user_id=user_id).update_one(upsert=True, set__password=password, set__household_id=household_id, set__container_url=container_url)
            except Exception as e:
                return("Error \n %s" % (e))
            return {'status': 'enrollment complete for user {}'.format(user_id)}

    def delete_demoer(self, user_id):
        if not user_id:
            return "No user ID provided with DELETE request"

        if self.check_user_exists == True:
            try:
                Demoer.objects(user_id=user_id).delete()
            except Exception as e:
                return("Error \n %s" % (e))
            return {'status': 'User with ID: {} was deleted'.format(user_id)}
        else:
            return "No user exists with ID: {} to DELETE".format(user_id)

    def check_user_exists(self, user_id):
        try:
            user = Demoer.objects(user_id=user_id)
        except Exception as e:
            return("Error \n %s" % (e))
        if len(user) > 0:
            return True
        else:
            return False

    def demoer_login(self, user_id, password):
        try:
            user = Demoer.objects(user_id=user_id, password=password)
        except Exception as e:
            return("Error \n %s" % (e))

        if len(user) > 0:
            return user[0].container_url
        else:
            return "Invalid Credentials, please try again"