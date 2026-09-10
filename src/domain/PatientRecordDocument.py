from dataclasses import dataclass


@dataclass(frozen=True)
class PatientRecordDocument:
    source: str
    patient_id: str
    content: str
