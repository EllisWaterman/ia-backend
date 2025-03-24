import json
from scores import Scores

def post_student_results(event, context):
    student_scores = json.loads(event['body'])
    if not ("student" in student_scores and "teacher" in student_scores):
        return {
        'statusCode': 400,
        'body': "Malformed Student Score",
    }
    client = Scores(student_scores["student"], student_scores["teacher"])
    print(client.send_scores(student_scores))
    return {
        'statusCode': 200,
        'body': json.dumps(student_scores)
    }

def get_scores(event, context):
    if event['queryStringParameters'] and (student_name := event['queryStringParameters']['student_name']) and (teacher_name := event['queryStringParameters']['teacher_name']):
        print(f"student name {student_name}")
        print(f"teacher_name: {teacher_name}")
        client = Scores(student_name, teacher_name)
        scores = client.get_scores()
        html_output = client.html_output(scores)
    else: 
        html_output = Scores.scores_form()
    return {
        'statusCode': 200,
        'body': str(html_output),
        'headers': {
            'content-type': 'text/html'
        }
    }   
