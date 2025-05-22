import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import time
import schedule
import re

FROM_EMAIL = "72emailsender@gmail.com"
PASSWORD = "glzm avaw kenn erbq"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{1,}$'
    return re.match(pattern, email) is not None

def load_email_sequence():
    with open(r'C:\Users\giric\Pictures\Camera Roll\cash_register\email_sender\email_sequence.json', 'r') as file:
        return json.load(file)

def load_recipients():
    with open(r'C:\Users\giric\Pictures\Camera Roll\cash_register\email_sender\emails.json', 'r') as file:
        return json.load(file)

def save_recipients(users):
    with open(r'C:\Users\giric\Pictures\Camera Roll\cash_register\email_sender\emails.json', 'w') as file:
        json.dump(users, file, indent=2)

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(FROM_EMAIL, PASSWORD)
        server.send_message(msg)
        print(f"✅ Sent '{subject}' to {to_email}")

def should_send(last_sent_iso, delay_seconds):
    if last_sent_iso is None: # Ja sanemejs nav sanemis nevienu epastu that vinam tiks sutiti epasti
        return True
    last_sent_dt = datetime.fromisoformat(last_sent_iso)
    # atgriezt true ja current time ir (last_sent + delay) vai vairak, ja ne False
    return datetime.now() >= last_sent_dt + timedelta(seconds=delay_seconds)

def send_sequence_emails():
    email_sequence = load_email_sequence() # Ielade epastus un to savstarpejas laika atstarpes
    users = load_recipients()

#Loop
    for user in users:
        sequence_index = user.get("sequence_index", 0)
        # Jau lietotajiem visi epasti jau aizsutit, tos izlaiz
        if sequence_index >= len(email_sequence):
            continue  

        email = email_sequence[sequence_index]
        delay_seconds = email.get("delay", 0)
        recipient_email = user.get("recipient")
# ievaddatu validacija
        if not is_valid_email(recipient_email):
            print(f"❌ Invalid email address: {recipient_email}. Skipping user.")
            continue
# ievaddatu validacija
        if should_send(user.get("last_sent"), delay_seconds):
            subject = email["subject"].format(first_name=user.get("first_name", ""))
            message = email["message"].format(first_name=user.get("first_name", ""))
            try:
                send_email(recipient_email, subject, message)
                # atjauno epasta sutisanas indeksu un laiku pirms pedeja aizsutita epasta
                user["sequence_index"] = sequence_index + 1
                user["last_sent"] = datetime.now().isoformat()
            except Exception as e:
                print(f"❌ Error sending to {recipient_email}: {e}")
# saglaba lietotajus json faila ar izmainam
    save_recipients(users)

if __name__ == "__main__":
    schedule.every(5).seconds.do(send_sequence_emails)  
# Schedule send_sequence_emails() to run every 2 seconds (for testing)
    print("🚀 Starting automatic email sender with schedule...")
    while True:
        schedule.run_pending()# izdarit visu ko vajag laicigi
        time.sleep(1)#sekundi pagaidi pirms loop atkartosanas