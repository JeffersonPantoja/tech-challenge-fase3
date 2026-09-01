from dataclasses import dataclass
from pathlib import Path

from src.domain.CurationStats import CurationStats


@dataclass(frozen=True)
class BuildDatasetResult:
    records_count: int
    output_path: Path
    curation_stats: CurationStats
