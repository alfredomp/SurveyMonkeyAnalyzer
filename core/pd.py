import os
import sys
import pathlib
import tempfile
import pandas
import numpy

def main():
    filepath = sys.argv[1]

    print(f"survey filepath: {filepath}")
    df = load_surveymonkey_df(filepath)
    print(f"survey responses: {len(df)}")

    status = df["How would you describe yourself?"]
    age = df["How old are you?"]
    gender = df[""]

    question_columns = df.columns[10:33]
    for question in question_columns:
        pass

    status = df["How would you describe yourself?"]
    import pdb; pdb.set_trace()
    

def load_surveymonkey_df(filepath: str, use_cache=False) -> pandas.DataFrame:
    if not use_cache:
        return create_surveymonkey_df(filepath)
    try:
        return pandas.read_pickle(get_cache_file(filepath))
    except FileNotFoundError:
        return create_surveymonkey_df(filepath)

def create_surveymonkey_df(filepath: str):
    df = pandas.read_csv(filepath)

    # credit: https://stackoverflow.com/a/49584888
    # survey specific: need to map guardian questions to self-reported questions
    indices = [i for i, c in enumerate(df.columns) if not c.startswith('Unnamed')]
    is_self_or_grdn = indices[9:10]
    self_reported = indices[10:33]
    grdn_reported = indices[33:]

    import pdb; pdb.set_trace()

    self_reported_slices = get_slices(self_reported)
    self_reported_answers = df.loc[0][9:]
    self_reported_data = [df.iloc[1:, s].apply(parse_response, axis=1) for s in self_reported_slices]

    grdn_reported_slices = get_slices(grdn_reported)
    grdn_reported_answers = df.loc[0][9:]
    grdn_data = [df.iloc[:, s].apply(response_mapper(self_reported_answers, grdn_reported_answers), axis=1)[1:] for s in grdn_reported_slices]

    questions = [df.columns[is_self_or_grdn], *df.columns[self_reported]]
    
    import pdb; pdb.set_trace()
    df = pandas.concat(self_reported_data + grdn_data, axis=1)
    df.columns = questions
    import pdb; pdb.set_trace()

    # survey specific: need to map second branch questions to first branch
    
    cache = pathlib.Path(get_cache_file(filepath))
    cache.parent.mkdir(exist_ok=True)
    df.to_pickle(cache)

    return df

def get_cache_file(filepath: str):
    return os.path.join(tempfile.gettempdir(), filepath)

def get_slices(indices: list):
    return [slice(i, j) for i, j in zip(indices, indices[1:] + [None])]

def parse_response(response):
    try:
        return response[~response.isnull()][0]
    except IndexError:
        return numpy.nan

def response_mapper(self_answers, grdn_answers):
    lookup = {numpy.nan: numpy.nan}
    skipped = 0
    for i, a in enumerate(grdn_answers):
        if grdn_answers[i] in ("They are no longer getting meals from school"):
            skipped += 1
        lookup[grdn_answers[i]] = self_answers[i - skipped]

    def parser(s):
        return lookup.get(parse_response(s))
    return parser

if __name__ == "__main__":
    main()

    # self.survey = Survey("New survey")
    # with open(filepath) as survey_file:
        

    #     reader = csv.reader(survey_file, delimiter=',')

    #     row_number = 1
    #     first_row = None
    #     second_row = None

    #     for row in reader:

    #         if row_number == 1:
    #             first_row = row
    #         elif row_number == 2:
    #             second_row = row
    #             self.read_first_and_second_rows(first_row, second_row)
    #         else:
    #             # Fill out the survey with responders and responses
    #             row_number_entries = len(row)

    #             participant_id = row[0]
    #             self.survey.add_participant(participant_id)

    #             for entry_number in range(9, row_number_entries):
    #                 answer_text = row[entry_number]
    #                 if answer_text != "":
    #                     self.survey.add_answer_to_question(participant_id,
    #                                                         entry_number,
    #                                                         answer_text)
    #         row_number = row_number + 1