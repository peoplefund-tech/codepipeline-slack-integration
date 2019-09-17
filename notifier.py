import logging
import json

from event_parser import (
    get_pipeline_metadata,
    get_codebuild_from_pipeline_metadata,
    is_codebuild_phases_updatable,
    get_codebuild_phases,
)
from slack_helper import find_slack_message_for_update
from message_builder import (
    MessageBuilder,
    post_message
)
from aws_client import (
    find_revision_info,
    find_pipeline_from_build,
)
from ecs_alarm import alarm_task


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run(event, context):
    logger.info('event received.')
    logger.info(json.dumps(event, indent=2))
    if event['source'] == "aws.codepipeline":
        process_code_pipeline(event)
    elif event['source'] == "aws.codebuild":
        process_code_build(event)
    elif event['source'] == "aws.ecs":
        alarm_task(event)

def process_code_pipeline(event):
    pipeline_execution_id, pipeline_name = get_pipeline_metadata(event)
    message = find_slack_message_for_update(pipeline_execution_id)
    message_builder = MessageBuilder(message, pipeline_execution_id, pipeline_name)
    message_builder.update_pipeline_message(event=event)

    if message_builder.has_revision_info_field():
        revision_info = find_revision_info(pipeline_execution_id, pipeline_name)
        message_builder.attach_revision_info(revision_info)

    post_message(message_builder=message_builder)


def process_code_build(event):
    pipeline_name, build_id, build_project_name = get_codebuild_from_pipeline_metadata(event)
    stage_name, pipeline_execution_id, action_state = find_pipeline_from_build(pipeline_name, build_id)

    if not pipeline_execution_id:
        return

    message = find_slack_message_for_update(pipeline_execution_id)
    message_builder = MessageBuilder(message, pipeline_execution_id, pipeline_name)

    if is_codebuild_phases_updatable(event):
        phases = get_codebuild_phases(event)
        message_builder.update_build_stage_info(stage_name, phases, action_state, build_project_name)

    post_message(message_builder=message_builder)