import boto3
import json
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from botocore.exceptions import ClientError
import logging
import hashlib
from decimal import Decimal
import simplejson as json
logger = logging.getLogger(__name__)

class Scores:
    def __init__(self, student, teacher):
        self.dynamodb = boto3.client('dynamodb')
        self.resource = boto3.resource('dynamodb')
        self.table_name = 'StudentScoresV02'
        self.table = self.resource.Table(self.table_name)
        self.student = student
        self.teacher = teacher
    
    def send_scores(self, student_scores):
        m = hashlib.sha1()
        m.update(f"{self.student} {self.teacher}".encode("utf-8"))
        key = m.hexdigest()
        serializer = TypeSerializer()
        new_problem_set_dynamodb = {"L": [serializer.serialize(student_scores)]}
        return self.dynamodb.update_item(
            TableName=self.table_name,
            Key={"studentTeacherHash": {"S": key}},
            UpdateExpression="SET problemSets.#ps = list_append(problemSets.#ps, :newItem)",
            ExpressionAttributeNames={"#ps": "problemSet"},
            ExpressionAttributeValues={":newItem": new_problem_set_dynamodb},
            ConditionExpression="attribute_exists(problemSets.#ps)",  # Ensure the list exists
            ReturnValues="UPDATED_NEW"
        )



def dynamodb_to_standard_json(dynamodb_json):
    deserializer = TypeDeserializer()
    return {key: deserializer.deserialize(value) for key, value in dynamodb_json.items()}

dynamodb_json = {
    "studentTeacherHash": {"S": "86ab3688746fe086927d415eedfc1cd4c46498b3"},
    "problemSets": {
        "M": {
            "problemSet": {
                "L": [
                    {
                        "M": {
                            "factorLowerBound": {"N": "2"},
                            "factorUpperBound": {"N": "9"},
                            "numberCorrect": {"N": "5"},
                            "numberWrong": {"N": "5"},
                            "operator": {"S": "multiplication"},
                            "problemSetEndTime": {"N": "1740800962"},
                            "problemSetStartTime": {"N": "1740800932"},
                        }
                    },
                    {
                        "M": {
                            "factorLowerBound": {"N": "2"},
                            "factorUpperBound": {"N": "12"},
                            "numberCorrect": {"N": "7"},
                            "numberWrong": {"N": "3"},
                            "operator": {"S": "division"},
                            "problemSetEndTime": {"N": "1741920474"},
                            "problemSetStartTime": {"N": "1741920504"},
                        }
                    }
                ]
            }
        }
    },
    "studentName": {"S": "Ellis Waterman"},
    "teacherName": {"S": "Mr. Foobar"}
}
student_scores = {
            "problemSetStartTime": 1740800932,
            "problemSetEndTime": 1740800962,
            "numberCorrect": 5,
            "numberWrong": 5,
            "operator": "multiplication",
            "factorUpperBound": 9,
            "factorLowerBound": 2
        }

student = "Ellis Waterman"
teacher = "Mr. Foobar"
client = Scores(student, teacher)
print(client.send_scores(student_scores))
exit
# Convert to standard JSON
standard_json = dynamodb_to_standard_json(dynamodb_json)

# Pretty-print the output
global someScore; (standard_json)