class Response:
    """ Definition of a Response """

    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.answer_ids = []

    def add_answer(self, answer_id):
        self.answer_ids.append(answer_id)

