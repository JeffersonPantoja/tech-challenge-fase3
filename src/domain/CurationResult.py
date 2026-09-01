from dataclasses import dataclass, field

from src.domain.QARecord import QARecord
from src.domain.CurationStats import CurationStats


@dataclass
class CurationResult:
    records: list[QARecord] = field(default_factory=list)
    stats: CurationStats = field(default_factory=CurationStats)
