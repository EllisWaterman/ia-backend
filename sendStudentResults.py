from scores import Scores
from datetime import datetime
import random

student_scores = {
            "student": "Ellis Waterman1",
            "teacher": "Mr. Foobar",
            "problemSetStartTime": int(datetime.timestamp(datetime.now())),
            "problemSetEndTime": int(datetime.timestamp(datetime.now())) + random.randint(10,20),
            "numberCorrect": random.randint(0,10),
            "numberWrong": random.randint(0,10),
            "operatorType": "multiplication",
            "factorUpperBound": 9,
            "factorLowerBound": 2
        }
client = Scores(student_scores["student"], student_scores["teacher"])
print(client.send_scores(student_scores))
