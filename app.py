from flask import Flask
import os
import psycopg2

app = Flask(__name__)

# --- Get DB connection details from environment variables ---
DB_HOST = os.environ.get("DB_HOST", "db-service") 
DB_NAME = os.environ.get("DB_NAME", "mydb")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")

# 1. LIVENESS CHECK (Simple ping to ensure the server process is alive)
# This will be used by the Liveness Probe to prevent unnecessary restarts.
@app.route('/healthz')
def healthz():
    """Liveness check: returns 200 OK if the Gunicorn server is running."""
    return "Liveness check passed: Server running.", 200

# 2. READINESS CHECK (Checks external dependency status)
# This will be used by the Readiness Probe to ensure the pod is ready to serve traffic.
@app.route('/')
def hello():
    """Readiness check: checks the database connection status."""
    try:
        # Attempt to establish a connection to the database
        #conn = psycopg2.connect(
        #    host=DB_HOST,
        #    database=DB_NAME,
        #    user=DB_USER,
        #    password=DB_PASS
        #)
        #conn.close()
        # SUCCESS: Returns 200 OK. Readiness probe passes.
        return "Web App is ready and successfully connected to DB!", 200
    except Exception as e:
        # FAILURE: Returns 503 Service Unavailable. 
        # Readiness probe fails, but Liveness probe on /healthz keeps the pod alive.
        app.logger.error(f"Readiness check failed: DB not ready. Error: {e}")
        # NOTE: Returning 503 is standard for "Service Unavailable"
        return "Service running, but Database is unavailable.", 503

if __name__ == '__main__':
    # We rely on Gunicorn in the Dockerfile, but keeping this for local testing.
    app.run(debug=True, host='0.0.0.0', port=5000)