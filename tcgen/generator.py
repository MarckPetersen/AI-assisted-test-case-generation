from typing import Callable, List, Optional

from .models import Requirement, TestCase, TestLevel
from .risk import LEVEL_OBJECTIVES, risk_score, test_depth

# A designer turns a prompt into a list of "title|expected result" lines.
# Plug in an LLM client here; the default is a deterministic placeholder.
Designer = Callable[[str], List[str]]


def build_prompt(req: Requirement, level: TestLevel, technique: str, count: int) -> str:
    return (
        f"You are an ISTQB-certified test analyst.\n"
        f"Test level: {level.value}\nObjective: {LEVEL_OBJECTIVES[level]}\n"
        f"Test basis ({req.id}, criticality {req.criticality.name}): {req.text}\n"
        f"Apply the test design technique: {technique}.\n"
        f"Produce {count} test case(s), one per line, as 'title|expected result'."
    )


def _default_designer(prompt: str) -> List[str]:
    count = int(prompt.split("Produce ")[1].split(" ")[0])
    return [f"Test condition {i + 1}|Behaviour matches the test basis" for i in range(count)]


def generate(requirements: List[Requirement], level: TestLevel,
             designer: Optional[Designer] = None) -> List[TestCase]:
    designer = designer or _default_designer
    cases: List[TestCase] = []
    for req in requirements:
        score = risk_score(req)
        technique, count = test_depth(score)
        lines = designer(build_prompt(req, level, technique, count))
        for line in lines:
            title, _, expected = line.partition("|")
            cases.append(TestCase(
                id=f"TC-{len(cases) + 1:03d}", title=title.strip(),
                requirement_id=req.id, level=level,
                objective=LEVEL_OBJECTIVES[level], technique=technique,
                risk_score=score, expected_result=expected.strip()))
    return cases
