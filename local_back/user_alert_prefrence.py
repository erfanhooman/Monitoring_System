"""
 local storage of user alert preferences.
"""
from flask import Flask, request, jsonify
from peewee import Model, SqliteDatabase, CharField, BooleanField
from logging_config import get_logger

SERVER_IP = {"127.0.0.1"}
flask_app = Flask(__name__)
logger = get_logger(__name__)

db = SqliteDatabase('user_alert_preferences.db')

class UserAlertPreference(Model):
    item_key = CharField()
    enabled = BooleanField()
    alert_level = CharField()

    class Meta:
        database = db

# Initial DB
try:
    db.connect()
    db.create_tables([UserAlertPreference])
    logger.info("Database connected and tables initialized.")
except Exception as e:
    logger.exception("Error initializing database.")



@flask_app.before_request
def restrict_ip():
    if request.remote_addr not in SERVER_IP:
        logger.warning(f"Unauthorized access attempt from {request.remote_addr}.")
        return jsonify({"error": "Forbidden"}), 403

@flask_app.route('/internal/update_preferences/', methods=['POST'])
def update_preferences():
    try:
        data = request.json
        if not data:
            logger.error("Invalid payload: No JSON data provided.")
            return jsonify({"error": "Invalid payload"}), 400

        item_key = data.get("item_key")
        enabled = data.get("enabled")
        alert_level = data.get("alert_level")

        if not item_key or enabled is None or not alert_level:
            logger.error(f"Missing required fields in payload: {data}")
            return jsonify({"error": "Missing required fields"}), 400

        preference, created = UserAlertPreference.get_or_create(
            item_key=item_key,
            defaults={"enabled": enabled, "alert_level": alert_level},
        )
        if not created:
            preference.enabled = enabled
            preference.alert_level = alert_level
            preference.save()

        logger.info(f"Preference updated: {item_key} - Enabled: {enabled}, Level: {alert_level}")
        return jsonify({"message": "Preference updated successfully"}), 200

    except Exception as e:
        logger.exception("Error updating preferences.")
        return jsonify({"error": "Internal Server Error"}), 500

@flask_app.route('/internal/delete_preferences/', methods=['POST'])
def delete_preferences():
    try:
        data = request.json
        if not data:
            logger.error("Invalid payload: No JSON data provided for deletion.")
            return jsonify({"error": "Invalid payload"}), 400

        item_key = data.get("item_key")

        if not item_key:
            logger.error("Missing item_key in payload for deletion.")
            return jsonify({"error": "item_key is required"}), 400

        # Check if the item exists and delete it
        deleted_count = UserAlertPreference.delete().where(UserAlertPreference.item_key == item_key).execute()

        if deleted_count > 0:
            logger.info(f"Deleted preference with item_key {item_key} from local database.")
            return jsonify({"message": "Preference deleted successfully"}), 200
        else:
            logger.warning(f"Preference with item_key {item_key} not found in local database.")
            return jsonify({"error": "Preference not found"}), 404

    except Exception as e:
        logger.exception("Error deleting preference from local database.")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    logger.info("Starting Flask application.")
    flask_app.run()