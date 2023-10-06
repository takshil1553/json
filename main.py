from flask import Flask, request
import logging
import json

# Define the Flask application
app = Flask(__name__)

# Define the custom JSONFormatter class
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno,
            "remote_addr": request.remote_addr if hasattr(request, "remote_addr") else "",
            "request_id": request.environ.get("HTTP_X_REQUEST_ID", ""),
            "custom_key": getattr(record, "custom_key", "xyz"), 
            "custom_value": getattr(record, "custom_value", "Abcd"),  
            "user_id": (123),
            "action": ("login"),
        }
        return json.dumps(log_data)

# Configure the logger with the custom formatter
json_handler = logging.StreamHandler()
json_handler.setFormatter(JSONFormatter())

app.logger.addHandler(json_handler)
app.logger.setLevel(logging.INFO)

# Define the route function
@app.route("/")
def index():
    user_id = 123
    action = "login"
    # print(f"user_id: {user_id}, action: {action}")

    logger = logging.getLogger("main")
    print("Before logger.info")
    logger.info(f"This is an info message", extra={"user_id": user_id, "action": action})
    print("After logger.info")
    logger.error("This is an error message", extra={"custom_key": "custom_value"})
    return "Hello, R@v@n!"

# Run the Flask application
if __name__ == "__main__":
    app.run()
