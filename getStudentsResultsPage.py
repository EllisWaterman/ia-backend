from scores import Scores

student = "Ellis Waterman"
teacher = "Mr. Foobar"
client = Scores(student, teacher)
scores = client.get_scores()
print(client.html_output(scores))

