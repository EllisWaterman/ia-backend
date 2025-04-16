import hashlib
from botocore.exceptions import ClientError
import logging
import boto3
import dominate
from dominate.tags import *
from boto3.dynamodb.types import TypeSerializer
import datetime
import dominate.util
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
        new_record = {"studentTeacherHash": key, "studentName": self.student, "teacherName": self.teacher,
                      "problemSets": {"problemSet": [student_scores]}}
        try:
            if self.dynamodb.put_item(
                TableName=self.table_name,
                Item=serializer.serialize(new_record)["M"],
                ConditionExpression="attribute_not_exists(studentTeacherHash)"
                ):
                return
        except:
            print(f"Record {key} already exists.")
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

    @classmethod
    def scores_form(self):
        style_text = open("style.css").read()
        doc = dominate.document(title=f"Enter Student Info")
        with doc.head:
            with doc.head.add(dominate.tags.style()):
                dominate.util.raw(style_text)
            script(type='text/javascript', src='script.js')
        with doc:
            with div(id='header'):
                h1(f"Enter Student Info")
            with div():
                attr(cls='body')
                with form(action = "https://t2ujycl4jf.execute-api.us-east-1.amazonaws.com/Prod/student_scores", method='GET'):
                    with label(for_="student_name"):
                        dominate.util.raw("Student Name:")
                    input_(type="text", id="student_name", name="student_name")
                    br()
                    with label(for_="teacher_name"):
                        dominate.util.raw("Teacher Name:")
                    input_(type="text", id="teacher_name", name="teacher_name")
                    br()
                    with button(type="submit"):
                        dominate.util.raw("Submit")
        return(doc)

        # <label for="student_name">Student Name:</label>
        # <input type="text" id="student_name" name="student_name" required>
        # <br>
        # <label for="teacher_name">Teacher Name:</label>
        # <input type="text" id="teacher_name" name="teacher_name" required>
        # <br>
        # <button type="submit">Submit</button>

    def html_output(self, item):
        style_text = open("style.css").read()
        doc = dominate.document(title=f"Results for {self.student}, student of {self.teacher}")
        with doc.head:
            with doc.head.add(dominate.tags.style()):
                dominate.util.raw(style_text)
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
                        with tr(style="green" if row['numberWrong'] == 0 else ""):
                            td(self.unixtimeprettytime(row['problemSetStartTime']))
                            td(self.unixtimeprettytime(row['problemSetEndTime']))
                            td(row['factorLowerBound'])
                            td(row['factorUpperBound'])
                            td(row['numberCorrect'])
                            td(row['numberWrong'])
                            td(row['operatorType'])
        return(doc)

    def unixtimeprettytime(self,unix_time):
        return datetime.datetime.strftime(datetime.datetime.fromtimestamp(int(unix_time)),"%D %I:%M %p")
   
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
