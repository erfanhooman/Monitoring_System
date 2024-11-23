"""
 local storage of user alert preferences.
"""

from peewee import Model, SqliteDatabase, CharField, BooleanField

db = SqliteDatabase('user_alert_preferences.db')

class UserAlertPreference(Model):
    item_key = CharField()
    enabled = BooleanField()
    alert_level = CharField()  # 'warning' or 'critical'

    class Meta:
        database = db

# Initialize database
db.connect()
db.create_tables([UserAlertPreference])


"""
script to fetch preferences from the server via an API.
"""

import requests

def sync_preferences(server_url, monitored_computer_id):
    response = requests.get(f"{server_url}/api/alert_preferences/{monitored_computer_id}/")
    if response.status_code == 200:
        preferences = response.json()
        # Update local database
        UserAlertPreference.delete().execute()
        for pref in preferences:
            UserAlertPreference.create(
                item_key=pref['item_key'],
                enabled=pref['enabled'],
                alert_level=pref['alert_level']
            )