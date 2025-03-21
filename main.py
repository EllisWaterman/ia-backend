import json
from scores import Scores

def post_student_results(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(event["body"])
    }

def get_scores(event, context):
    student = "Ellis Waterman"
    teacher = "Mr. Foobar"
    client = Scores(student, teacher)
    scores = client.get_scores()
    print(event)
    return {
        'statusCode': 200,
        'body': str(client.html_output(scores)),
        'headers': {
            'content-type': 'text/html'
        }
    }
