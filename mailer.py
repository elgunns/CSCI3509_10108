OUTBOX_PATH = "outbox.txt"


def send(to, subject, body):
    """Stand-in for a mail server: appends each message to outbox.txt."""
    with open(OUTBOX_PATH, "a") as f:
        f.write("TO: " + to + " | SUBJECT: " + subject + " | BODY: " + body + "\n")
