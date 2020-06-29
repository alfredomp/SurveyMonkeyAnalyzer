# Script that reads a csv with the raw data exported from Survey Monkey, and
# creates and populates a survey
# Author: Alfredo Morales Pinzón
# Date: June 28, 2020

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import argparse
from core.SurveyManager import SurveyManager

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
print("survey_filepathsurvey_filepath:", survey_filepath)
print("")


# =============================================================================
# Main code
# =============================================================================

survey_manager = SurveyManager()

survey_manager.load_survey(survey_filepath)
print(survey_manager.get_stats_question_by_group(14, [23, 24]))
# survey_manager.get_stats_concatenated_questions([1, 14])

# print("__________________________________________")
# survey_manager.get_stats_question(24)
# print("__________________________________________")
# survey_manager.get_stats_question(47)
