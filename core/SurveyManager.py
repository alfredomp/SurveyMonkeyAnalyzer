import csv
import itertools
import pandas

from core.Survey import Survey
from core.alias import alias_question

NO_ANSWER = "Unknown"

class SurveyManager:
    """ Definition of a Survey Manager"""

    def __init__(self):
        self.survey = None

    def read_first_and_second_rows(self, first_row, second_row):
        """ Read the first row. This defines the data to be collected for each
            # answer and the questions. Every question has a N of empty entries
            # after its definintion. This means that each question has N+1
            # possible answers
        """

        # print("first_row:", len(first_row))
        # print("first_row:", len(second_row))

        row_number_entries = len(second_row)

        # The first 9 entries are not questions but information about each answer
        general_info = dict()
        general_info["Respondent_ID"] = 0
        general_info["Collector_ID"] = 1
        general_info["Start_Date"] = 2
        general_info["End_Date"] = 3
        general_info["IP_Address"] = 4
        general_info["Email_Address"] = 5
        general_info["First_Name"] = 6
        general_info["Last_Name"] = 7
        general_info["Custom_Data_1"] = 8

        new_question_text = None
        new_question_possible_answers = []
        current_question_id = 1
        first_question = True

        for entry_number in range(9, row_number_entries):

            entry_first_row = first_row[entry_number]
            entry_second_row = second_row[entry_number]

            # If there is a new question to be created. Post the previous question.
            if entry_first_row != "":
                if first_question:
                    first_question = False
                else:
                    self.survey.add_question_with_answers(current_question_id,
                                                          new_question_text,
                                                          new_question_possible_answers)

                    current_question_id = current_question_id + 1
                    new_question_possible_answers = []

                new_question_text = entry_first_row
                answer = {'id': entry_number, 'text': entry_second_row}
                new_question_possible_answers.append(answer)
            else:
                answer = {'id': entry_number, 'text': entry_second_row}
                new_question_possible_answers.append(answer)

            # Post the last question
            if entry_number == row_number_entries - 1:
                self.survey.add_question_with_answers(current_question_id,
                                                      new_question_text,
                                                      new_question_possible_answers)

    def load_survey(self, survey_file_path):

        self.survey = Survey("New survey")

        with open(survey_file_path) as survey_file:

            reader = csv.reader(survey_file, delimiter=',')

            row_number = 1
            first_row = None
            second_row = None

            for row in reader:

                if row_number == 1:
                    first_row = row
                elif row_number == 2:
                    second_row = row
                    self.read_first_and_second_rows(first_row, second_row)
                else:
                    # Fill out the survey with responders and responses
                    row_number_entries = len(row)

                    participant_id = row[0]
                    self.survey.add_participant(participant_id)

                    for entry_number in range(9, row_number_entries):
                        answer_text = row[entry_number]
                        if answer_text != "":
                            self.survey.add_answer_to_question(participant_id,
                                                               entry_number,
                                                               answer_text)
                row_number = row_number + 1

            # self.survey.print_question_with_possible_answers_and_num_participants()

    def get_stats_question(self, question_id):
        self.survey.print_summary_question_by_id(question_id)

    def to_group_key(self, participant_id, question_ids, key_prefix = []):
        key = key_prefix
        for qid in question_ids:
            response = self.to_question(qid).get_responses_participant(participant_id)
            response_aid = response.answer_ids[0] if response else None
            key.append(response_aid)
        return tuple(key)

    def to_question(self, question_id):
        if isinstance(question_id, int):
            return self.survey.find_question_by_id(question_id)
        return alias_question(
            self.survey.find_question_by_id(question_id[0]),
            self.survey.find_question_by_id(question_id[1])
        )

    def to_answer(self, answer_id):
        answer = self.survey.find_answer_by_id(answer_id)
        return answer["text"] if answer else ""

    def get_stats_question_by_group(self, target_question_id, group_by_question_ids):
        # { [answer_id]: [participant_id] }
        groups = {}
        by_answer = self.to_question(target_question_id).get_participant_ids_per_answer()
        for aid in by_answer:
            answer_info = by_answer[aid]
            answer_pids = answer_info["participant_ids"]

            for pid in answer_pids:
                key = self.to_group_key(pid, group_by_question_ids, [aid])
                groups.setdefault(key, [])
                groups[key].append(pid)

        return groups

    def get_df_question_by_group(self, target_question_id, group_by_question_ids):
        groups = [self.to_question(qid) for qid in group_by_question_ids]
        target = self.to_question(target_question_id)
        answers = [a for a in target.possible_answers]
        columns =  [g.text for g in groups] + [a.text for a in answers]

        per_target = target.get_participant_ids_per_answer()
        keys = itertools.product(*[[a.text for a in gq.possible_answers] + [NO_ANSWER] for gq in groups])
        data = {k[0]: {} for k in keys} # ensure expected ordering
        for aid, answer_info in per_target.items():
            atext = self.to_answer(aid)
            pids = set(answer_info["participant_ids"])
            for pid in pids:
                responses = [gq.get_responses_participant(pid) for gq in groups]
                keys = itertools.product(*[[self.to_answer(raid) for raid in r.answer_ids] if r else [NO_ANSWER] for r in responses])
                for key in keys:
                    data[key[0]].setdefault(atext, set())
                    data[key[0]][atext].add(pid)
                
        rows = [[k, *[len(v.get(a.text, [])) for a in answers]] for k, v in data.items()]
        # stats = self.get_stats_question_by_group(target_question_id, group_by_question_ids)

        
        # data = [
        #     [self.to_answer(aid) for aid in key[1:]] + [len(pids) if key[0] == a.id else 0 for a in answers]
        #     for key, pids in stats.items()
        # ]
        # import pdb; pdb.set_trace()
        df = pandas.DataFrame(rows, columns=columns)
        # df = df.sort_values(columns[:len(groups)])

        return df

    def print_stats_question_by_group(self, target_question_id, group_by_question_ids):
        print(self.to_question(target_question_id).text)
        for qid in group_by_question_ids:
            print(self.to_question(qid).text)
            
        stats = self.get_stats_question_by_group(target_question_id, group_by_question_ids)
        for answer_ids, participant_ids in stats.items():
            label = (self.survey.find_answer_by_id(aid) for aid in answer_ids)
            label = ",".join([raw["text"] if raw else "None" for raw in label])
            print(f"{label}: {len(participant_ids)}")

    def get_stats_concatenated_questions(self, question_ids):

        # Get the summary of the first question
        self.survey.print_summary_question_by_id(question_ids[0])

        self.survey.print_concatenate_question_results(question_ids[0], question_ids[1])
