from core.Question import Question
from core.PossibleAnswer import PossibleAnswer
from core.Response import Response

def alias_question(q1, q2):
    aliased = Question(q1.id, q1.text)
    aliased.possible_answers = list(q1.possible_answers)
    aliased.responses = list(q1.responses)

    aliased_answers = {}
    for i in range(len(q2.possible_answers)):
        if i > len(q1.possible_answers):
          aliased_answers[q2.possible_answers[i]] = q2.possible_answers[i]
        else:
          aliased_answers[q2.possible_answers[i]] = q1.possible_answers[i]

    for original in q2.responses:
      response = Response(original.participant_id)
      response.answer_ids = [aliased_answers[answer].id for answer in q2.possible_answers]

      aliased.responses.append(response)

    return aliased