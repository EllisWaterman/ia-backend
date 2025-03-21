from scores import Scores
print(Scores.scores_form())
exit()
student = "Ellis Waterman"
teacher = "Mr. Foobar"
client = Scores(student, teacher)
scores = client.get_scores()
print(type(str(client.html_output(scores))))
print(str(client.html_output(scores)))

