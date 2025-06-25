import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# E-Mail senden
def send_email(name, email, message):
    smtp_server = os.environ.get("SMTP_SERVER")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    email_to   = os.environ.get("EMAIL_TO")

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = email_to
    msg["Subject"] = "Neue Nachricht von der Website"

    body = f"""
    Neue Nachricht von {name} ({email}):

    {message}
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, email_to, msg.as_string())
        print("E-Mail gesendet ✅")
    except Exception as e:
        print("Fehler beim Senden der E-Mail ❌", str(e))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # E-Mail versenden
        send_email(name, email, message)

        return redirect(url_for("thank_you"))
    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
