<a href="https://www.twilio.com">
  <img src="https://static0.twilio.com/marketing/bundles/marketing/img/logos/wordmark-red.svg" alt="Twilio" width="250" />
</a>

# Twilio Account Security Quickstart - Two-Factor Authentication and Phone Verification

> We are currently in the process of updating this sample template. If you are encountering any issues with the sample, please open an issue at [github.com/twilio-labs/code-exchange/issues](https://github.com/twilio-labs/code-exchange/issues) and we'll try to help you.

![](https://github.com/TwilioDevEd/account-security-quickstart-django/workflows/Django/badge.svg)

A simple Python and Django implementation of a website that uses Twilio Account Security services to protect all assets within a folder. Additionally, it shows a Phone Verification implementation.

It uses four channels for delivery: SMS, Voice, Soft Tokens, and Push Notifications. You should have the [Authy App](https://authy.com/download/) installed to try Soft Token and Push Notification support.

Learn more about Account Security and when to use the Authy API vs the Verify API in the [Account Security documentation](https://www.twilio.com/docs/verify/authy-vs-verify).


#### Two-Factor Authentication Demo
- URL path "/protected" is protected with both user session and Twilio Two-Factor Authentication
- One Time Passwords (SMS and Voice)
- SoftTokens
- Push Notifications (via polling)

#### Phone Verification
- Phone Verification
- SMS or Voice Call

### How to get an Authy API Key
You will need to create a new Authy application in the [console](https://www.twilio.com/console/authy/). After you give it a name you can view the generated Account Security production API key. This is the string you will later need to set up in your environmental variables.

![Get Authy API Key](api_key.png)

### Setup

This project only runs on Python 3.6+. In some environments when both version 2
and 3 are installed, you may substitute the Python executables below with
`python3` and `pip3` unless you use a version manager such as
[pyenv](https://github.com/pyenv/pyenv).

1. Clone this repo

2. Create a new virtual environment:

  * If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

    ```bash
    virtualenv venv
    source venv/bin/activate
    ```

  * If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

    ```bash
    mkvirtualenv lead-alerts-flask

3. Install the dependencies

  ```
  pip install -r requirements.txt
  ```

4. Register for a [Twilio Account](https://www.twilio.com/try-twilio).

5. Setup an Account Security app via the [Twilio Console](https://www.twilio.com/console/authy).

6. Grab an Application API key from the Dashboard and paste it in `.env.example`

7. Copy and save the `.env.example` file as `.env`

8. Run `./manage.py migrate` to apply migrations

9. Run `./manage.py runserver` from the cloned repo to run the app

10. The application should now be running on http://localhost:8000/, here you can
register a new user account and proceed with a phone verification.

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* The CodeExchange repository can be found [here](https://github.com/twilio-labs/code-exchange/).
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.
