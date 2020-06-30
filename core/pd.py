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
    indices = [i for i, c in enumerate(df.columns) if not c.startswith('Unnamed')]
    questions = [c for c in df.columns if not c.startswith('Unnamed')]
    slices = [slice(i, j) for i, j in zip(indices, indices[1:] + [None])]
    data = [df.iloc[:, q].apply(parse_response, axis=1)[1:] for q in slices]
    df = pandas.concat(data, axis=1)
    df.columns = questions
    
    cache = pathlib.Path(get_cache_file(filepath))
    cache.parent.mkdir(exist_ok=True)
    df.to_pickle(cache)

    return df

def get_cache_file(filepath: str):
    return os.path.join(tempfile.gettempdir(), filepath)

def parse_response(s):
    try:
        return s[~s.isnull()][0]
    except IndexError:
        return numpy.nan

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