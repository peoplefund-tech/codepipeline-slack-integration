from event_parser import (
    get_ecs_task_stopped_reason,
    get_ecs_task_infos,
    get_ecs_container_infos,
)
from slack_helper import (
    send_message,
    SLACK_CHANNEL,
    find_channel_id
)


def alarm_task(event):
    task_stopped_reason = get_ecs_task_stopped_reason(event)
    if task_stopped_reason is None:
        return

    if 'deployment' in task_stopped_reason:
        return
    
    else:
        channel_id = find_channel_id(SLACK_CHANNEL)
        cluster_name, group, task_id, task_definition_name = get_ecs_task_infos(event)

        link = "https://ap-northeast-2.console.aws.amazon.com" \
               "/ecs/home?region=ap-northeast-2#/clusters/{}/tasks/{}/details".format(
                    cluster_name,
                    task_id
                )

        container_infos = get_ecs_container_infos(event)
        container_info_message = "{:^20} {:^20}\n".format('name', 'reason')
        
        for container_info in container_infos:
            container_info_message += "{:^20} {:^20}\n".format(
                container_info['name'],
                container_info['reason'],
            )
            
        fields = [
            {
                "title": ':scream: Task abnormal termination :scream:',
                "value": "Reason: {}".format(task_stopped_reason),
                "short": False
            },
            {
                "title": 'Cluster name',
                "value": cluster_name,
                "short": True
            },
            {
                "title": 'Group',
                "value": group,
                "short": True
            },
            {
                "title": 'Task id',
                "value": task_id,
                "short": True
            },
            {
                "title": 'Task definition name',
                "value": task_definition_name,
                "short": True
            },
            {
                "title": 'Container Info',
                "value": "```\n{}\n```".format(container_info_message),
                "short": False
            },
        ]

        action = [{
                "type": "button",
                "text": "Task details",
                "url": link
        }]
        
        message = [
            {
                "fields": fields,
                "color": 'danger',
                "actions": action
            }
        ]

        send_message(
            channel_id,
            message
        )
