"""
Simple local test site for uptime/downtime demos.

Run:
    python test_site_uptime.py

Site will serve on http://127.0.0.1:8002/
Click "Take Down" to simulate downtime (returns 503).
Click "Bring Up" to restore service (returns 200).
"""

from flask import Flask, request, redirect

app = Flask(__name__)

# In-memory flag to simulate downtime
is_down = False


def render_page():
    """Return HTML based on current state."""
    if is_down:
        body = """
        <div style="background-color: #2d1b1b; color: #ff6b6b; padding: 20px; font-family: Arial, sans-serif; text-align: center; min-height: 100vh;">
            <h1 style="font-size: 48px; color: #ff4444; margin: 20px 0;">
                🔴 SERVICE DOWN
            </h1>
            <h2 style="font-size: 32px; color: #ff6666; margin: 20px 0;">
                Website is Currently Offline
            </h2>
            <p style="font-size: 24px; color: #ff8888; margin: 30px 0;">
                HTTP 503 - Service Unavailable
            </p>
            <p style="font-size: 18px; color: #ffaaaa; margin: 20px 0;">
                This simulates a website downtime scenario. Restore it to bring the service back online.
            </p>
            <form method="post" action="/toggle" style="margin-top: 40px;">
                <input type="hidden" name="state" value="up" />
                <button type="submit" style="background-color: #00ff00; color: #000; padding: 15px 30px; font-size: 18px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold;">
                    🔵 Bring Up
                </button>
            </form>
        </div>
        """
    else:
        body = """
        <div style="background-color: #1b2d1b; color: #6bff6b; padding: 20px; font-family: Arial, sans-serif; text-align: center; min-height: 100vh;">
            <h1 style="font-size: 48px; color: #44ff44; margin: 20px 0;">
                🟢 SERVICE ONLINE
            </h1>
            <h2 style="font-size: 32px; color: #66ff66; margin: 20px 0;">
                Website is Running Normally
            </h2>
            <p style="font-size: 24px; color: #88ff88; margin: 30px 0;">
                HTTP 200 - OK
            </p>
            <p style="font-size: 18px; color: #aaffaa; margin: 20px 0;">
                This website is currently online and responding normally.
            </p>
            <form method="post" action="/toggle" style="margin-top: 40px;">
                <input type="hidden" name="state" value="down" />
                <button type="submit" style="background-color: #ff4444; color: white; padding: 15px 30px; font-size: 18px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold;">
                    🔴 Take Down
                </button>
            </form>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8" />
      <title>WebGuard Uptime Demo</title>
    </head>
    <body style="margin: 0; padding: 0;">
      {body}
    </body>
    </html>
    """


@app.route("/", methods=["GET"])
def index():
    global is_down
    if is_down:
        # Return 503 Service Unavailable when down
        return render_page(), 503
    else:
        # Return 200 OK when up
        return render_page(), 200


@app.route("/toggle", methods=["POST"])
def toggle():
    global is_down
    desired = request.form.get("state")
    
    if desired == "down":
        is_down = True
    elif desired == "up":
        is_down = False
    
    return redirect("/")


if __name__ == "__main__":
    print("=" * 60)
    print("WebGuard Uptime Test Site")
    print("=" * 60)
    print("Server running on http://127.0.0.1:8002/")
    print("Use this to test downtime detection and notifications")
    print("=" * 60)
    app.run(host="127.0.0.1", port=8002, debug=False)

