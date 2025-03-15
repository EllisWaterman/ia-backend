import hashlib
from botocore.exceptions import ClientError
import logging
import boto3
import dominate
from dominate.tags import *
from boto3.dynamodb.types import TypeSerializer
import datetime
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

    def html_output(self, item):
        doc = dominate.document(title=f"Results for {self.student}, student of {self.teacher}")
        with doc.head:
            link(rel='stylesheet', href='style.css')
            script(type='text/javascript', src='script.js')
        with doc:
            with div(id='header'):
                h1(f"Results for {self.student}, student of {self.teacher}")
            with div():
                attr(cls='body')
                with table(border=1):
                    with tr():
                        th("Start Time")
                        th("End Time")
                        th("Factor Lower Bound")
                        th("Factor Upper Bound")
                        th("Number Correct")
                        th("Number Wrong")
                        th("Operator")
                    for row in item['problemSets']['problemSet']:
                        with tr():
                            td(self.unixtimeprettytime(row['problemSetStartTime']))
                            td(self.unixtimeprettytime(row['problemSetEndTime']))
                            td(row['factorLowerBound'])
                            td(row['factorUpperBound'])
                            td(row['numberCorrect'])
                            td(row['numberWrong'])
                            td(row['operator'])
        return(doc)

    def unixtimeprettytime(self,unix_time):
        return datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(unix_time)),"%D %I:%m %p")
   
    def get_scores(self):
        m = hashlib.sha1()
        m.update(f"{self.student} {self.teacher}".encode("utf-8"))
        key = m.hexdigest()

        try:
            response = self.table.get_item(Key={"studentTeacherHash": key})
        except ClientError as err:
            logger.error(
                "Couldn't get scores %s from table %s. Here's why: %s: %s",
                key,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response["Item"]
