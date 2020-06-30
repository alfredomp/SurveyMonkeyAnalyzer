from core.PossibleAnswer import PossibleAnswer
from core.Response import Response


class Question:
    """Definition of a Question"""

    def __init__(self, question_id, question_text):
        self.id = question_id
        self.text = question_text
        self.possible_answers = []
        self.responses = []

    def set_possible_answers(self, possible_answers):
        self.possible_answers = []
        for answer in possible_answers:
            answer_id = answer["id"]
            answer_text = answer["text"]
            answer_new = PossibleAnswer(answer_id, answer_text)
            self.possible_answers.append(answer_new)

    def get_or_create_response_of_participant(self, participant_id):
        for response in self.responses:
            if response.participant_id == participant_id:
                return response
        response = Response(participant_id)
        self.responses.append(response)
        return response

    def add_response(self, participant_id, answer_id, answer_text):
        response = self.get_or_create_response_of_participant(participant_id)
        response.add_answer(answer_id)

    def has_answer_id(self, answer_id, answer_text):
        for possible_answer in self.possible_answers:
            if possible_answer.id == answer_id:
                return True
        return False

    def get_participant_ids(self):
        participant_ids = []
        for response in self.responses:
            participant_ids.append(response.participant_id)
        return participant_ids

    def get_responses_participant(self, participant_id):
        for response in self.responses:
            if response.participant_id == participant_id:
                return response

    def get_participant_ids_per_answer(self):
        responses_per_possible_answer = {}

        for possible_answer in self.possible_answers:
            responses_per_possible_answer[possible_answer.id] = {}
            responses_per_possible_answer[possible_answer.id]['text'] = possible_answer.text
            responses_per_possible_answer[possible_answer.id]['participant_ids'] = []

        for response in self.responses:
            for answer_id in response.answer_ids:
                responses_per_possible_answer[answer_id]['participant_ids'].append(response.participant_id)

        return responses_per_possible_answer

    def print_summary(self):
        responses_per_possible_answer = {}

        for possible_answer in self.possible_answers:
            responses_per_possible_answer[possible_answer.id] = {}
            responses_per_possible_answer[possible_answer.id]['text'] = possible_answer.text
            responses_per_possible_answer[possible_answer.id]['number'] = 0

        for response in self.responses:
            for answer_id in response.answer_ids:
                responses_per_possible_answer[answer_id]['number'] += 1

        print("Question:", self.text)
        for response_id in responses_per_possible_answer:
            print(responses_per_possible_answer[response_id]['text'], ": ",
                  responses_per_possible_answer[response_id]['number'])

    def print_summary_in_participant_ids(self, participant_ids):
        responses_per_possible_answer = {}
        participants_with_no_answer = 0

        for possible_answer in self.possible_answers:
            responses_per_possible_answer[possible_answer.id] = {}
            responses_per_possible_answer[possible_answer.id]['text'] = possible_answer.text
            responses_per_possible_answer[possible_answer.id]['number'] = 0

        for participant_id in participant_ids:
            response_participant = self.get_responses_participant(participant_id)
            if not response_participant:
                participants_with_no_answer += 1
            else:
                for answer_id in response_participant.answer_ids:
                    responses_per_possible_answer[answer_id]['number'] += 1

        print("\t---------------------------------------------")
        print("\tQuestion:", self.text)
        for response_id in responses_per_possible_answer:
            print("\t", responses_per_possible_answer[response_id]['text'], ": ",
                  responses_per_possible_answer[response_id]['number'])

        print("\tNo responses from previous question:", participants_with_no_answer)

    def print_possible_answers(self):
        for answer in self.possible_answers:
            print("\t", answer.id, ":", answer.text)
        print("\t Responses:", len(self.responses))
