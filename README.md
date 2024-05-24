# Patient Inviter
Sends email account registration invitations to patients.

## Description
This program sends email invitations (single or batched) to patients: the emails contain a deep link to allow downloading a mobile app from the email.  Email delivery is don by integrating with a third-party email service provider API (Postmark).

## Usage
There are two different usage modes, each with a corresponding shell wrapping script.

### 1. Single email invitations

This particular mode uses the transactional email stream API for single message delivery:

```
invite.sh <recipients_email_address>
```

#### Pre-requisites
You need to sepecify the required parameter configuration in a file named `configs/email_config.json`, following the form:

```
{
  "SERVER_TOKEN": <POST_MARK_SERVER_API_TOKEN>,
  "TEMPLATE_ID" : <TEMPLATE_ID_DEFINING_EMAIL_BODY_CONTENT>,
  "STREAM" : <TRANSACTIONAL_STREAM_NAME>,
  "SENDER" : <SENER_NAME_TO_BE_SHOWN_ON_THE_EMAIL>,
  "WEBLINK" : <DEEP_LINK_TO_APP_INSTALL>,
  "SUBJECT" : <EMAIL_SUBJECT>,
  "CONTACT" : <FROM_EMAIL_ADDRESS>,
  "CODE" : <ACCOUNT_REGISTRATION_SECURITY_CODE>
}
```
### 2. Multiple email invitations in one batch

This particular mode uses the broadcasting email stream API for batch message delivery:

```
send_emails.sh <batch_number>
```

#### Pre-requisites
You need to sepecify the required parameter configuration in a file named `configs/batch_config.json`, following the form:

```
{
  "SERVER_TOKEN": <POST_MARK_SERVER_API_TOKEN>,
  "TEMPLATE_ID" : <TEMPLATE_ID_DEFINING_EMAIL_BODY_CONTENT>,
  "STREAM" : <BROADCASTING_STREAM_NAME>,
  "SENDER" : <SENER_NAME_TO_BE_SHOWN_ON_THE_EMAIL>,
  "WEBLINK" : <DEEP_LINK_TO_APP_INSTALL>,
  "SUBJECT" : <EMAIL_SUBJECT>,
  "CONTACT" : <FROM_EMAIL_ADDRESS>,
  "CODE" : <ACCOUNT_REGISTRATION_SECURITY_CODE>
}
```
Additionally, you need to setup the target emails to be sent in the batch by creating the file `batches/batch<x>/emails.csv`

where:
 - `x` is the batch number to be passed to the `send_emails.sh` script
 - `emails.csv` contains the target emails separated by commas