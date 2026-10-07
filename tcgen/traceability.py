from typing import Dict, List

from .models import Requirement, Result, TestCase


def traceability_matrix(requirements: List[Requirement], cases: List[TestCase]) -> Dict[str, List[str]]:
    """Requirement id -> ids of test cases covering it (empty list = uncovered)."""
    matrix = {r.id: [] for r in requirements}
    for tc in cases:
        matrix.setdefault(tc.requirement_id, []).append(tc.id)
    return matrix


def evaluate_exit_criteria(requirements: List[Requirement], cases: List[TestCase],
                           min_pass_rate: float = 0.95, high_risk_threshold: int = 8) -> dict:
    """Evaluate simple exit criteria and give a basis for the acceptance decision.

    Criteria: every requirement covered; all tests executed; pass rate >= min_pass_rate;
    no failed/blocked test with risk score >= high_risk_threshold.
    """
    matrix = traceability_matrix(requirements, cases)
    uncovered = [r for r, tcs in matrix.items() if not tcs]
    not_run = [t.id for t in cases if t.result == Result.NOT_RUN]
    passed = sum(t.result == Result.PASSED for t in cases)
    pass_rate = passed / len(cases) if cases else 0.0
    open_high_risk = [t.id for t in cases
                      if t.result in (Result.FAILED, Result.BLOCKED) and t.risk_score >= high_risk_threshold]
    met = not uncovered and not not_run and pass_rate >= min_pass_rate and not open_high_risk and bool(cases)
    return {"exit_criteria_met": met, "uncovered_requirements": uncovered,
            "not_run": not_run, "pass_rate": pass_rate, "open_high_risk": open_high_risk}
