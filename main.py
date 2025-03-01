import json

def post_student_results(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(event["body"])
    }
