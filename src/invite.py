import requests

"""
Script to send doclisten invitations to patients.
"""
import json
import sys

POSTMARK_ENDPOINT = "https://api.postmarkapp.com/email/withTemplate"


class EmailSender:
    def __init__(self, config_file, email):
        self.data = EmailSender.__load_data(config_file)
        self.recipient = email.strip()

    def __load_data(config_file):
        with open(config_file) as f:
            return json.load(f)

    @property
    def server_token(self):
        return self.data["SERVER_TOKEN"]

    @property
    def post_data(self):
        return {
            "From": self.data["CONTACT"],
            "To": self.data["CONTACT"],
            "Bcc": self.recipient,
            "ReplyTo": self.data["CONTACT"],
            "MessageStream": self.data["STREAM"],
            "TemplateId": self.data["TEMPLATE_ID"],
            "TemplateModel": {
                "sender": self.data["SENDER"],
                "weblink": self.data["WEBLINK"],
                "subject": self.data["SUBJECT"],
                "code": self.data["CODE"],
            },
        }

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": self.server_token,
        }

    def send_invitation(self):
        response = requests.post(POSTMARK_ENDPOINT, headers=self.headers, json=self.post_data)
        if response:
            print(f"Invitation successfully sent to: {self.recipient}")
        else:
            print(
                f"Error encountered during send: {response.status_code}: {response.text}"
            )


def main():
    if len(sys.argv) != 3:
        print(f"\n Usage: {sys.argv[0]} <config_file.json> <recipient_email_address>\n")
        exit(1)

    # print(f"Using config_file: {sys.argv[1]}, emails_file: {sys.argv[2]}")
    config = EmailSender(sys.argv[1], sys.argv[2])
    # print(config.headers)
    config.send_invitation()


if __name__ == "__main__":
    main()
