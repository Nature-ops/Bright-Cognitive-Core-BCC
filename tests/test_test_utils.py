from unittest import TestCase

from tests.test_utils import iam_passing_answers


class TestUtilsTest(TestCase):
    def test_iam_passing_answers_returns_independent_answers(self):
        answers = iam_passing_answers()

        self.assertEqual(
            answers,
            {
                "iam-q1": "Identity and Access Management",
                "iam-q2": "IAM Role",
                "iam-q3": "Least privilege",
            },
        )

        answers["iam-q1"] = "changed"

        self.assertEqual(
            iam_passing_answers()["iam-q1"],
            "Identity and Access Management",
        )
