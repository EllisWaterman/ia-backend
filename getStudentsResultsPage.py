import boto3
from botocore.exceptions import ClientError
import logging
import hashlib
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal
import simplejson as json
import dominate
from dominate.tags import *
logger = logging.getLogger(__name__)


class Scores:
    def __init__(self, student, teacher):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('StudentScoresV02')
        self.student = student
        self.teacher = teacher

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
                            td(row['problemSetStartTime'])
                            td(row['problemSetEndTime'])
                            td(row['factorLowerBound'])
                            td(row['factorUpperBound'])
                            td(row['numberCorrect'])
                            td(row['numberWrong'])
                            td(row['operator'])
        return(doc)

    
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



student = "Ellis Waterman"
teacher = "Mr. Foobar"
client = Scores(student, teacher)
scores = client.get_scores()
print(client.html_output(scores))

