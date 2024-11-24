"""
 local storage of user alert preferences.
"""
from flask import Flask, request, jsonify
from peewee import Model, SqliteDatabase, CharField, BooleanField


SERVER_IP = {"127.0.0.1"}
flask_app = Flask(__name__)

db = SqliteDatabase('user_alert_preferences.db')

class UserAlertPreference(Model):
    item_key = CharField()
    enabled = BooleanField()
    alert_level = CharField()

    class Meta:
        database = db

# Initialize database
db.connect()
db.create_tables([UserAlertPreference])



@flask_app.before_request
def restrict_ip():
    if request.remote_addr not in SERVER_IP:
        return jsonify({"error": "Forbidden"}), 403

@flask_app.route('/internal/update_preferences/', methods=['POST'])
def update_preferences():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    item_key = data.get("item_key")
    enabled = data.get("enabled")
    alert_level = data.get("alert_level")

    if not item_key or enabled is None or not alert_level:
        return jsonify({"error": "Missing required fields"}), 400

    preference, created = UserAlertPreference.get_or_create(
        item_key=item_key,
        defaults={"enabled": enabled, "alert_level": alert_level},
    )
    if not created:
        preference.enabled = enabled
        preference.alert_level = alert_level
        preference.save()

    return jsonify({"message": "Preference updated successfully"}), 200

if __name__ == '__main__':
    flask_app.run()