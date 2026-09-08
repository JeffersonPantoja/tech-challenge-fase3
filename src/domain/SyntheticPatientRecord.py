from dataclasses import dataclass


@dataclass(frozen=True)
class SyntheticPatientRecord:
    source: str
    patient_id: str
    chief_complaint: str
    history: str
    medications: str
    vitals: str
    assessment: str
    plan: str
