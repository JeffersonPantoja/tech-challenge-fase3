from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NormalizePatientIdsResult:
    records_count: int
    output_path: Path
