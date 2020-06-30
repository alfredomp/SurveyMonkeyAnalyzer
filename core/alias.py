from core.Question import Question
from core.PossibleAnswer import PossibleAnswer
from core.Response import Response

def alias_question(q1, q2):
    aliased = Question(q1.id, q1.text)
    aliased.possible_answers = list(q1.possible_answers)
    aliased.responses = list(q1.responses)

    # assumes that answer order lines up between questions
    aliased_answer_ids = {}
    for i in range(len(q2.possible_answers)):
        if i >= len(q1.possible_answers):
          aliased_answer_ids[q2.possible_answers[i].id] = q2.possible_answers[i].id
        else:
          aliased_answer_ids[q2.possible_answers[i].id] = q1.possible_answers[i].id

    for original in q2.responses:
      response = Response(original.participant_id)
      response.answer_ids = [aliased_answer_ids[aid] for aid in original.answer_ids]
      aliased.responses.append(response)

    return aliased