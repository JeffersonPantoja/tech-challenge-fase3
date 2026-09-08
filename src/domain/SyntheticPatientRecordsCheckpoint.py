from dataclasses import dataclass, field


@dataclass(frozen=True)
class SyntheticPatientRecordsCheckpoint:
    processed_sources: set[str] = field(default_factory=set)
    failed_sources: set[str] = field(default_factory=set)
