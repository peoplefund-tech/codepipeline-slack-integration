from slackclient import SlackClient
import os
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

slack_client = SlackClient(os.getenv("SLACK_TOKEN"))
sc_bot = SlackClient(os.getenv("SLACK_BOT_TOKEN"))
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "builds_test")
SLACK_BOT_NAME = os.getenv("SLACK_BOT_NAME", "PipelineBot")
SLACK_BOT_ICON = os.getenv("SLACK_BOT_ICON", ":robot_face:")


def find_slack_message_for_update(pipeline_execution_id):
    channel_id = find_channel_id(SLACK_CHANNEL)
    slack_messages = get_slack_messages_from_channel(channel_id=channel_id)

    for message in slack_messages:
        if message.get('username', '') != SLACK_BOT_NAME:
            continue

        attachments = message.get('attachments', [])
        for attachment in attachments:
            if attachment['footer'] == pipeline_execution_id:
                return message

    return None


def find_channel_id(channel_name):
    res = slack_client.api_call("channels.list", exclude_archived=1)

    if 'error' in res:
        if not isinstance(res['error'], str):
            err_message = ''
        else:
            err_message = res['error']
        raise ValueError(f'can not read channel list. error message from slack:{err_message}')

    channels = res['channels']

    for channel in channels:
        if channel['name'] == channel_name:
            return channel['id']

    raise ValueError(f'can not find channel. channel name:{channel_name}')


def get_slack_messages_from_channel(channel_id):
    res = slack_client.api_call('channels.history', channel=channel_id)

    if 'error' in res:
        if not isinstance(res['error'], str):
            err_message = ''
        else:
            err_message = res['error']
        raise ValueError(f'can not read channel list. error message from slack:{err_message}')

    return res['messages']


def update_message(channel_id, message_id, attachments):
    res = slack_client.api_call(
        "chat.update",
        channel=channel_id,
        ts=message_id,
        icon_emoji=SLACK_BOT_ICON,
        username=SLACK_BOT_NAME,
        attachments=attachments
    )

    if 'error' in res:
        if not isinstance(res['error'], str):
            err_message = ''
        else:
            err_message = res['error']
        raise ValueError(f'can update message. error message from slack:{err_message}')

    return res


def send_message(channel_id, attachments):
    res = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        icon_emoji=SLACK_BOT_ICON,
        username=SLACK_BOT_NAME,
        attachments=attachments
    )

    if 'error' in res:
        if not isinstance(res['error'], str):
            err_message = ''
        else:
            err_message = res['error']
        raise ValueError(f'can update message. error message from slack:{err_message}')

    return res
