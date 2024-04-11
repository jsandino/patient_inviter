import unittest

from src.invite import EmailSender


class EmailSenderTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sender = EmailSender("test/sample_config.json", "test/sample_emails.csv")
        return super().setUp()

    def test_data_loading(self):
        """
        EmailSender constructor loads data from file
        """
        self.assertTrue(self.sender.data)

    def test_server_token(self):
        """
        EmailSender returns server token
        """
        self.assertEquals(self.sender.server_token, "token-123")

    def test_post_data_from(self):
        """
        EmailSender post data includes "From" field
        """
        self.assertField("From", "contact@sandino.ca")

    def test_post_data_to(self):
        """
        EmailSender post data includes "To" field
        """
        self.assertField("To", "contact@sandino.ca")

    def test_post_data_reply_to(self):
        """
        EmailSender post data includes "ReplyTo" field
        """
        self.assertField("ReplyTo", "contact@sandino.ca")

    def test_post_data_message_stream(self):
        """
        EmailSender post data includes "MessageStream" field
        """
        self.assertField("MessageStream", "invitations")

    def test_post_data_template_id(self):
        """
        EmailSender post data includes "TemplateId" field
        """
        self.assertField("TemplateId", "template-45")

    def test_post_data_bcc(self):
        """
        EmailSender post data includes "Bcc" field
        """
        self.assertField("Bcc", "joe@test.com,mary@test.com,jim@test.com")        
        

    def test_post_data_template_model(self):
        """
        EmailSender post data includes "TemplateModel" object
        """
        model = self.sender.post_data["TemplateModel"]
        self.assertTrue(model)
        self.assertField("sender", "Joe Baz", object=model)
        self.assertField("weblink", "https://domain.page.link/SMj5", object=model)
        self.assertField("subject", "An invitation", object=model)
        self.assertField("code", "ABC123", object=model)

    def test_headers_accept(self):
      """
      EmailSender headers include "Accept"
      """
      headers = self.sender.headers
      self.assertEquals(headers["Accept"], "application/json")

    def test_headers_content_type(self):
      """
      EmailSender headers include "Content-Type"
      """
      headers = self.sender.headers
      self.assertEquals(headers["Content-Type"], "application/json")      

    def test_headers_token(self):
      """
      EmailSender headers include "X-Postmark-Server-Token"
      """
      headers = self.sender.headers
      self.assertEquals(headers["X-Postmark-Server-Token"], "token-123")


    def assertField(self,  fieldName, expectedValue, object=None):
        object = self.sender.post_data if not object else object
        self.assertTrue(object[fieldName])
        self.assertEquals(object[fieldName], expectedValue)
