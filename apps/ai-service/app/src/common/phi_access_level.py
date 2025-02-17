from enum import Enum


class PhiAccessLevel(str, Enum):
    METRICS_ONLY: str = "METRICS_ONLY"
    NONE: str = "NONE"
    PATIENT_LEVEL_CONDITIONAL: str = "PATIENT_LEVEL_CONDITIONAL"
    PATIENT_LEVEL_FULL = "PATIENT_LEVEL_FULL"
