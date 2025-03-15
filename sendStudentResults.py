from scores import Scores
from datetime import datetime
import random

student_scores = {
            "problemSetStartTime": int(datetime.timestamp(datetime.now())),
            "problemSetEndTime": int(datetime.timestamp(datetime.now())) + random.randint(10,20),
            "numberCorrect": random.randint(0,10),
            "numberWrong": random.randint(0,10),
            "operator": "multiplication",
            "factorUpperBound": 9,
            "factorLowerBound": 2
        }

student = "Ellis Waterman"
teacher = "Mr. Foobar"
client = Scores(student, teacher)
print(client.send_scores(student_scores))
