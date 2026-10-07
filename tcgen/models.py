from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class TestLevel(str, Enum):
    COMPONENT = "component"
    INTEGRATION = "integration"
    SYSTEM = "system"
    ACCEPTANCE = "acceptance"


class Criticality(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Result(str, Enum):
    NOT_RUN = "not run"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Requirement:
    """An item of the test basis."""
    id: str
    text: str
    criticality: Criticality = Criticality.MEDIUM
    likelihood: int = 2  # risk likelihood of failure, 1 (low) .. 3 (high)


@dataclass
class TestCase:
    id: str
    title: str
    requirement_id: str
    level: TestLevel
    objective: str
    technique: str
    risk_score: int
    expected_result: str = ""
    steps: List[str] = field(default_factory=list)
    result: Result = Result.NOT_RUN
