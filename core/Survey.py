from core.Participant import Participant
from core.Question import Question

# TODO: Check that a new answer does not have an id of an answer already inserted
# TODO: Manages cases where question are not found


class Survey:
    """ Definition of a Survey """

    def __init__(self, name):
        self.name = name
        self.participants = []
        self.questions = []
        self.answers = {}

    def add_question_with_answers(self, question_id, question_text, possible_answers):
        question = Question(question_id, question_text)
        question.set_possible_answers(possible_answers)
        self.questions.append(question)
        for answer in possible_answers:
            self.answers[answer["id"]] = answer

    def add_participant(self, participant_id):
        participant = Participant(participant_id)
        self.participants.append(participant)

    def find_question_with_answer_id(self, answer_id, answer_text):
        for question in self.questions:
            if question.has_answer_id(answer_id, answer_text):
                return question

    def find_question_by_id(self, question_id):
        for question in self.questions:
            if question.id == question_id:
                return question

    def find_answer_by_id(self, answer_id):
        return self.answers.get(answer_id)

    def add_answer_to_question(self, participant_id, answer_id, answer_text):
        question = self.find_question_with_answer_id(answer_id, answer_text)
        question.add_response(participant_id, answer_id, answer_text)

    def get_participant_ids_in_question(self, question_id):
        question = self.find_question_by_id(question_id)
        return question.get_participant_ids()

    def print_summary_question_by_id(self, question_id):
        question = self.find_question_by_id(question_id)
        question.print_summary()

    def print_summary_question_by_id_in_participant_ids(self, question_id, participants_ids):
        question = self.find_question_by_id(question_id)
        question.print_summary_in_participant_ids(participants_ids)

    def print_questions(self):
        for question in self.questions:
            print(question.id, ":", question.text)

    def print_questions_with_possible_answers(self):
        for question in self.questions:
            print(question.id, ":", question.text)
            question.print_possible_answers()

    def print_question_with_possible_answers_and_num_participants(self):
        for question in self.questions:
            print(question.id, ":", question.text)
            question.print_possible_answers()

    def print_concatenate_question_results(self, question_id_1, question_id_2):
        question_1 = self.find_question_by_id(question_id_1)
        question_2 = self.find_question_by_id(question_id_2)

        dic_answer_participant_id = question_1.get_participant_ids_per_answer()

        for answer_id_in_question_1 in dic_answer_participant_id:
            participants_answer_id_in_question_1 = dic_answer_participant_id[answer_id_in_question_1]["participant_ids"]
            print("\t Answer:", dic_answer_participant_id[answer_id_in_question_1]["text"])

            question_2.print_summary_in_participant_ids(participants_answer_id_in_question_1)

