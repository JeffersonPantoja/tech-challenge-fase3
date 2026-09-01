from dataclasses import dataclass


@dataclass(frozen=True)
class CurationStats:
    kept: int = 0
    discarded_empty_fields: int = 0
    discarded_duplicates: int = 0
    discarded_too_short: int = 0
