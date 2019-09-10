import boto3
client = boto3.client('codepipeline')


def find_revision_info(pipeline_execution_id, pipeline_name):
    res = client.get_pipeline_execution(
        pipelineName=pipeline_name,
        pipelineExecutionId=pipeline_execution_id
    )['pipelineExecution']

    if 'artifactRevisions' in res:
        return res[0]
    else:
        return None


def find_pipeline_from_build(pipeline_name, build_id):
    res = client.get_pipeline_state(
        name=pipeline_name
    )['stageStates']

    for stage_state in res:
        for action_state in stage_state['actionStates']:
            execution_id = action_state['latestExecution']['externalExecutionId']
            if execution_id and build_id.endswith(execution_id):
                pipeline_execution_id = stage_state['latestExecution']['pipelineExecutionId']
                stage_name = stage_state['stageName']

                return stage_name, pipeline_execution_id, action_state

    return None, None, None
