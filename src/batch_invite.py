"""
Script to send doclisten invitations to patients.
"""
import requests
import pprint
import json
import sys
import csv

POSTMARK_ENDPOINT = "https://api.postmarkapp.com/email/batchWithTemplates"


class EmailSender:
    def __init__(self, config_file, emails_file):
        self.data = EmailSender.__load_data(config_file)
        self.recipients = EmailSender.__load_emails(emails_file)

    def __load_data(config_file):
        with open(config_file) as f:
            return json.load(f)

    def __load_emails(emails_file):
        with open(emails_file) as f:
            return f.read().replace("\n","").split(",")

    @property
    def server_token(self):
        return self.data["SERVER_TOKEN"]

    @property
    def post_data(self):
        recipients = [self.recipient(email) for email in self.recipients]
        return { "Messages" : recipients }
    
    def recipient(self, email):
        return {
            "From": self.data["CONTACT"],
            "To": email,
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

    def send_invitations(self):
        response = requests.post(POSTMARK_ENDPOINT, headers=self.headers, json=self.post_data)
        if response:
            print(f"Invitation successfully sent to: {self.recipients}")
        else:
            print(
                f"Error encountered during send: {response.status_code}: {response.text}"
            )


def main():
    if len(sys.argv) != 3:
        print(f"\n Usage: {sys.argv[0]} <config_file.json> <emails_file.csv>\n")
        exit(1)

    # print(f"Using config_file: {sys.argv[1]}, emails_file: {sys.argv[2]}")
    config = EmailSender(sys.argv[1], sys.argv[2])
    # print(config.headers)
    config.send_invitations()


if __name__ == "__main__":
    main()
