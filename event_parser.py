def get_pipeline_metadata(event):
    detail = event['detail']
    pipeline_execution_id = detail['execution-id']
    pipeline_name = detail['pipeline']
    return pipeline_execution_id, pipeline_name


def is_pipeline_state_update(event):
    return event['detail-type'] == "CodePipeline Pipeline Execution State Change"


def is_pipeline_stage_state_update(event):
    return event['detail-type'] == "CodePipeline Stage Execution State Change"


def get_pipeline_stages(event):
    return event['detail']['stage']


def get_pipeline_states(event):
    return event['detail']['state']


def get_codebuild_from_pipeline_metadata(event):
    detail = event['detail']
    pipeline_name = detail['additional-information']['initiator'][13:]
    build_id = detail['build-id']
    build_project_name = detail['project-name']

    return pipeline_name, build_id, build_project_name


def is_codebuild_phases_updatable(event):
    return 'phases' in event['detail']['additional-information']


def get_codebuild_phases(event):
    return event['detail']['additional-information']['phases']


def has_phase_context(phase):
    return 'phase-context' in phase


def get_phase_context(phase):
    return phase['phase-context']


def get_phase_status(phase):
    if 'phase-status' in phase:
        return phase['phase-status']
    else:
        return 'IN_PROGRESS'


def get_phase_type(phase):
    if 'phase-type' in phase: 
        return phase['phase-type']
    else:
        return None


def get_phase_duration(phase):
    if 'duration-in-seconds' in phase:
        return phase['duration-in-seconds']
    else:
        return None
