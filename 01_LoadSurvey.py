# Script that reads a csv with the raw data exported from Survey Monkey, and
# creates and populates a survey
# Author: Alfredo Morales Pinzón
# Date: June 28, 2020

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import argparse
from pathlib import Path
from enum import Enum
from core.SurveyManager import SurveyManager
from core.plot import fix_legend

# -----------------------------------------------------------------------------
# Parse the inputs
# -----------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file_path_survey", required=True,
    help="File path to the survey.")
args = parser.parse_args()

# -----------------------------------------------------------------------------
# Get the inputs and set log dictionary
# -----------------------------------------------------------------------------

input_files = {}

survey_filepath = args.file_path_survey

print("")
print("survey_filepath:", survey_filepath)
print("")


# =============================================================================
# Main code
# =============================================================================

survey_manager = SurveyManager()
survey_manager.load_survey(survey_filepath)

DELIMITER = "__________________________________________"

# question ids
class Questions(Enum):
    HEALTH_INSURANCE = (2, 25)
    ONE_CARE = (3, 26)
    LONG_TERM_SUPPORT_SERVICES = (4, 27)
    SENIOR_CARE_OPTIONS = (5, 28)
    GERIATRIC_SUPPORT_SERVICES = (6, 29)
    PRIMARY_CARE_CONTACT = (7, 30)
    PRIMARY_CARE_HELP = (8, 31)
    PRIMARY_CARE_SERVICES = (9, 32)
    SPECIALIST_TROUBLE = (10, 33)
    MENTAL_HEALTH_TROUBLE = (11, 34)
    SUBSTANCE_USE_TROUBLE = (12, 35)
    PPE = (13, 36)
    MASSHEALTH_PCA = (14, 37)
    PCA_COVERAGE = (15, 38)
    FOOD_TROUBLE = (16, 39)
    FOOD_TROUBLE_CAUSE = (17, 40)
    MEDICAL_DISCRIMINATION = (18, 41)
    MEDICAL_DISCRIMINATION_SPECIFIC = (19, 42)

class Demographics(Enum):
    BY_AGE = [(20, 43)]
    BY_ETHNICITY = [(24, 47)] #, (23, 46)]
    BY_GENDER = [(21, 44)] #, (22, 45)]

# sanity check
# survey_manager.print_stats_question_by_group(14, [23, 24])
# print(DELIMITER)
# survey_manager.print_stats_question_by_group(37, [46, 47])
# print(DELIMITER)
# survey_manager.print_stats_question_by_group((14, 37), Demographics.BY_ETHNICITY.value)

for question in Questions:
    for demographic in Demographics:
        out = Path(f"images/{question.name}_{demographic.name}.png")
        out.parent.mkdir(exist_ok=True)
        print(f"Generating: {out}")

        # survey_manager.print_stats_question_by_group(question.value, demographic.value)
        df = survey_manager.get_df_question_by_group(question.value, demographic.value)
        plot = df.plot.barh(x=df.columns[0], y=df.columns[1:], figsize=(12, 8))
        plot = fix_legend(plot, len(df[df.columns[0]].unique()))
        
        plot.get_figure().savefig(out)
        # plot.get_figure().close()
        # import pdb; pdb.set_trace()
        # print(DELIMITER)

# survey_manager.get_stats_concatenated_questions([1, 14])

# print("__________________________________________")
# survey_manager.get_stats_question(24)
# print("__________________________________________")
# survey_manager.get_stats_question(47)
