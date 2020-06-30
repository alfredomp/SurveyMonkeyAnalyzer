from enum import Enum

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
    BY_ETHNICITY = [(24, 47), (23, 46)]
    BY_GENDER = [(21, 44), (22, 45)]