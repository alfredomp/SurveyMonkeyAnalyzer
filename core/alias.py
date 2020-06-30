from core.Question import Question
from core.PossibleAnswer import PossibleAnswer
from core.Response import Response

def alias_question(q1, q2):
    aliased = Question(q1.id, q1.text)
    aliased.possible_answers = list(q1.possible_answers)
    aliased.responses = list(q1.responses)

    # assumes that answer order lines up between questions
    aliased_answer_ids = {}
    skipped = 0
    for i in range(len(q2.possible_answers)):
        q2_answer = q2.possible_answers[i]
        if q2_answer.id == 157: # special casing one mismatched question
          aliased.possible_answers.append(q2_answer)
          aliased_answer_ids[q2_answer.id] = q2_answer.id
          skipped = 1
          continue

        aliased_answer_ids[q2_answer.id] = q1.possible_answers[i - skipped].id

    for original in q2.responses:
      response = Response(original.participant_id)
      response.answer_ids = [aliased_answer_ids[aid] for aid in original.answer_ids]
      aliased.responses.append(response)

    return aliased