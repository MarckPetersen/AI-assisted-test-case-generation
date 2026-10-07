import unittest

from tcgen.generator import generate
from tcgen.models import Criticality, Requirement, Result, TestLevel
from tcgen.risk import risk_score, test_depth
from tcgen.traceability import evaluate_exit_criteria, traceability_matrix


class TestTcgen(unittest.TestCase):
    def setUp(self):
        self.reqs = [
            Requirement("R1", "Payment is authorised", Criticality.CRITICAL, 3),
            Requirement("R2", "Footer shows copyright", Criticality.LOW, 1),
        ]

    def test_risk_drives_depth(self):
        self.assertEqual(risk_score(self.reqs[0]), 12)
        self.assertEqual(test_depth(12)[1], 5)
        self.assertEqual(test_depth(1)[1], 1)

    def test_generation_and_traceability(self):
        cases = generate(self.reqs, TestLevel.SYSTEM)
        self.assertEqual(len(cases), 6)
        m = traceability_matrix(self.reqs, cases)
        self.assertEqual(len(m["R1"]), 5)
        self.assertEqual(len(m["R2"]), 1)

    def test_exit_criteria(self):
        cases = generate(self.reqs, TestLevel.SYSTEM)
        self.assertFalse(evaluate_exit_criteria(self.reqs, cases)["exit_criteria_met"])
        for c in cases:
            c.result = Result.PASSED
        self.assertTrue(evaluate_exit_criteria(self.reqs, cases)["exit_criteria_met"])
        cases[0].result = Result.FAILED
        self.assertFalse(evaluate_exit_criteria(self.reqs, cases)["exit_criteria_met"])


if __name__ == "__main__":
    unittest.main()
