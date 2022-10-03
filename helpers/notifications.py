"""
    Notification functions used in this project.
    Includes Email (SMTP via TLS) and Slack.
"""

import json
import smtplib
from email.mime.text import MIMEText
import traceback
import logging
import requests
from settings import EMAIL_NOTIFICATIONS_ENABLED, SLACK_NOTIFICATIONS_ENABLED,\
    SLACK_SEND_SUCCESS_CODE, TO_ADDRS, FROM_ADDR_EMAIL, FROM_ADDR_PASSWORD,\
    SMTP_HOST, SMTP_TLS_PORT
from helpers.formatters import format_proc_details
logging.basicConfig(level=logging.DEBUG)


def send_slack_message(msg):
    """ Sends a Slack message to specified Slack Incoming Webhook. """
    try:
        res = requests.post(
            url='SLACK_WEBHOOK_URL',
            data=json.dumps({'text': msg}),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if res.status_code == SLACK_SEND_SUCCESS_CODE:
            logging.info(
                'Slack message sent successfully. Status Code: %d',
                res.status_code,
            )
            return True
        logging.info(
            'Slack message sending failure. Status Code: %d',
            res.status_code,
        )
        return False

    # pylint: disable=bare-except
    except:
        logging.info(
            'Exception occurred while sending Slack message. Traceback: %s',
            traceback.format_exc(),
        )
        return False


def send_email(to_addrs, msg_str):
    """ Sends an email to specified email addresses."""
    try:
        msg = MIMEText(msg_str)
        msg['Subject'] = 'High Resource Consumption Detected'
        msg['From'] = FROM_ADDR_EMAIL
        msg['To'] = ','.join(to_addrs)

        smtp = smtplib.SMTP(SMTP_HOST, port=SMTP_TLS_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_ADDR_EMAIL, FROM_ADDR_PASSWORD)
        smtp.sendmail(
            from_addr=FROM_ADDR_EMAIL,
            to_addrs=to_addrs,
            msg=msg.as_string(),
        )
        smtp.quit()
        logging.info('Email sent successfully to %s.', to_addrs)
        return True
    # pylint: disable=bare-except
    except:
        logging.info(
            'Exception occurred while sending email. Traceback: %s',
            traceback.format_exc(),
        )
        return False


def _get_ticks_window_secs(hog_procs):
    max_ticks = 0
    for proc in hog_procs:
        num_ticks = proc['num_ticks_cpu'] or proc['num_ticks_mem']
        if num_ticks > max_ticks:
            max_ticks = num_ticks
    return max_ticks


def send_hogging_slack(hog_procs):
    """ Creates and sends the final Slack messages with the processes info. """

    if not SLACK_NOTIFICATIONS_ENABLED:
        return False

    # pylint: disable=consider-using-f-string
    msg_str = 'I am under heavy load for more than {} seconds '.format(
        _get_ticks_window_secs(hog_procs)
    ) + 'from processes as below:\n\n' + format_hogging_procs(hog_procs)
    logging.info(msg_str)
    return send_slack_message(msg_str)


def send_hogging_email(hog_procs):
    """ Creates and sends the final Email messages with the processes info. """

    if not EMAIL_NOTIFICATIONS_ENABLED:
        return False

    msg_str = 'High Consumption Processes as below:\n\n' +\
        format_hogging_procs(hog_procs)
    logging.info(msg_str)
    return send_email(to_addrs=TO_ADDRS, msg_str=msg_str)


def format_hogging_procs(hog_procs):
    """ Returns a formatted string containing processes information. """
    return '\n'.join(format_proc_details(hog_procs=hog_procs))
