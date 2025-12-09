"""
Simple local test site for defacement demos.

Run:
    python test_site.py

Site will serve on http://127.0.0.1:8001/
Click "Deface me" to switch to defaced content.
Click "Restore original" to revert.
Click "Update" to simulate a legitimate website update.
"""

from flask import Flask, request, redirect

app = Flask(__name__)

# In-memory flags to simulate different states
is_defaced = False
is_updated = False


def render_page():
    """Return HTML based on current state."""
    if is_defaced:
        body = """
        <div style="background-color: #1a0000; color: #ff0000; padding: 20px; font-family: 'Courier New', monospace; text-align: center; min-height: 100vh;">
            <h1 style="font-size: 48px; color: #ff0000; text-shadow: 2px 2px 4px #000; margin: 20px 0;">
                💀 HACKED 💀
            </h1>
            <h2 style="font-size: 32px; color: #ff3333; text-shadow: 2px 2px 4px #000; margin: 20px 0;">
                ⚠️ WEBSITE DEFACED ⚠️
            </h2>
            <p style="font-size: 24px; color: #ff6666; margin: 30px 0;">
                YOUR SITE HAS BEEN COMPROMISED!
            </p>
            <p style="font-size: 18px; color: #ff9999; margin: 20px 0;">
                This is what a defaced website looks like. Restore it to clear the alert.
            </p>
            <form method="post" action="/toggle" style="margin-top: 40px;">
                <input type="hidden" name="state" value="restore" />
                <button type="submit" style="background-color: #00ff00; color: #000; padding: 15px 30px; font-size: 18px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold;">
                    Restore Original
                </button>
            </form>
        </div>
        """
    elif is_updated:
        body = """
        <div style="background-color: #1a1a2e; color: #00d4ff; padding: 20px; font-family: Arial, sans-serif; min-height: 100vh;">
            <h1 style="color: #00d4ff; font-size: 36px;">WebGuard Test Page - Updated</h1>
            <p style="color: #66e0ff; font-size: 18px; margin: 20px 0;">
                This is an updated version of the website with new styling and content.
                This represents a legitimate update that should not trigger defacement alerts.
            </p>
            <p style="color: #99e6ff; font-size: 16px; margin: 20px 0;">
                Background and text colors have been changed to demonstrate a website update.
            </p>
            <div style="margin-top: 30px;">
                <form method="post" action="/toggle" style="display: inline-block; margin-right: 10px;">
                    <input type="hidden" name="state" value="original" />
                    <button type="submit" style="background-color: #4a4a6e; color: #00d4ff; padding: 10px 20px; font-size: 16px; border: none; cursor: pointer; border-radius: 5px;">
                        Back to Original
                    </button>
                </form>
                <form method="post" action="/toggle" style="display: inline-block;">
                    <input type="hidden" name="state" value="deface" />
                    <button type="submit" style="background-color: #6a0000; color: #ff6666; padding: 10px 20px; font-size: 16px; border: none; cursor: pointer; border-radius: 5px;">
                        Deface Me
                    </button>
                </form>
            </div>
        </div>
        """
    else:
        body = """
        <div style="background-color: #f5f5f5; color: #333; padding: 20px; font-family: Arial, sans-serif; min-height: 100vh;">
            <h1 style="color: #333; font-size: 36px;">WebGuard Test Page</h1>
            <p style="color: #666; font-size: 18px; margin: 20px 0;">
                This is the original, clean version of the page.
            </p>
            <p style="color: #888; font-size: 16px; margin: 20px 0;">
                Use the buttons below to test defacement detection and website updates.
            </p>
            <div style="margin-top: 30px;">
                <form method="post" action="/toggle" style="display: inline-block; margin-right: 10px;">
                    <input type="hidden" name="state" value="deface" />
                    <button type="submit" style="background-color: #dc3545; color: white; padding: 10px 20px; font-size: 16px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold;">
                        Deface Me
                    </button>
                </form>
                <form method="post" action="/toggle" style="display: inline-block;">
                    <input type="hidden" name="state" value="update" />
                    <button type="submit" style="background-color: #007bff; color: white; padding: 10px 20px; font-size: 16px; border: none; cursor: pointer; border-radius: 5px; font-weight: bold;">
                        Update
                    </button>
                </form>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8" />
      <title>WebGuard Defacement Demo</title>
    </head>
    <body style="margin: 0; padding: 0;">
      {body}
    </body>
    </html>
    """


@app.route("/", methods=["GET"])
def index():
    return render_page()


@app.route("/toggle", methods=["POST"])
def toggle():
    global is_defaced, is_updated
    desired = request.form.get("state")
    
    if desired == "deface":
        is_defaced = True
        is_updated = False
    elif desired == "restore" or desired == "original":
        is_defaced = False
        is_updated = False
    elif desired == "update":
        is_defaced = False
        is_updated = True
    
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=False)
