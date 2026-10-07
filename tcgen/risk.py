from .models import Requirement, TestLevel

# Typical objectives and test bases per ISTQB test level.
LEVEL_OBJECTIVES = {
    TestLevel.COMPONENT: "Verify component logic against the component specification / detailed design",
    TestLevel.INTEGRATION: "Verify interfaces and interactions between components or systems",
    TestLevel.SYSTEM: "Verify end-to-end behaviour and non-functional characteristics against system requirements",
    TestLevel.ACCEPTANCE: "Establish confidence that the system meets user/business needs and is ready to be accepted",
}

# Depth of testing by risk score: (technique, minimum number of test cases).
_DEPTH = [
    (12, "boundary value analysis + equivalence partitioning + decision table", 5),
    (8, "boundary value analysis + equivalence partitioning", 3),
    (4, "equivalence partitioning", 2),
    (0, "experience-based (error guessing)", 1),
]


def risk_score(req: Requirement) -> int:
    """Risk = likelihood (1-3) x impact (criticality 1-4)."""
    if not 1 <= req.likelihood <= 3:
        raise ValueError("likelihood must be between 1 and 3")
    return req.likelihood * int(req.criticality)


def test_depth(score: int):
    """Return (technique, number of test cases) for a risk score."""
    for threshold, technique, count in _DEPTH:
        if score >= threshold:
            return technique, count
    raise ValueError("invalid risk score")
