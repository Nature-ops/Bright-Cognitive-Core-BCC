from unittest import TestCase

from pydantic import ValidationError

from app.models.exercise import Exercise
from app.services.exercise_engine import ExerciseEngine
from app.services.exercise_loader import ExerciseLoader


class ExerciseObjectiveMappingTest(TestCase):
    def test_exercise_accepts_ordered_objective_ids_without_mutating_input(self):
        objective_ids = ["iam-users", "iam-policies"]

        exercise = Exercise(
            id="iam-lab",
            title="IAM Hands-on Lab",
            description="Practice IAM.",
            steps=["Create an IAM user."],
            verification="Sign in as the IAM user.",
            objective_ids=objective_ids,
        )
        exercise.objective_ids.append("other-objective")

        self.assertEqual(
            objective_ids,
            ["iam-users", "iam-policies"],
        )
        self.assertEqual(
            exercise.objective_ids,
            ["iam-users", "iam-policies", "other-objective"],
        )

    def test_objective_ids_default_to_an_empty_list_for_existing_content(self):
        exercise = Exercise(
            id="legacy-lab",
            title="Legacy Lab",
            description="Existing exercise content.",
            steps=["Complete the exercise."],
            verification="Verify completion.",
        )

        self.assertEqual(exercise.objective_ids, [])

    def test_iam_exercise_loads_explicit_objectives_in_yaml_order(self):
        exercise = ExerciseLoader().load(
            "knowledge/cloud/exercises/iam.yaml"
        )

        self.assertEqual(exercise.id, "iam-lab")
        self.assertEqual(
            exercise.objective_ids,
            ["iam-users", "iam-policies"],
        )

    def test_existing_exercises_load_with_empty_objective_ids(self):
        engine = ExerciseEngine()
        engine.load_directory("knowledge/cloud/exercises")

        self.assertEqual(
            engine.get_exercise("ec2-lab").objective_ids,
            [],
        )
        self.assertEqual(
            engine.get_exercise("s3-lab").objective_ids,
            [],
        )
        self.assertEqual(
            engine.get_exercise("vpc-lab").objective_ids,
            [],
        )

    def test_malformed_objective_ids_fail_model_validation(self):
        with self.assertRaises(ValidationError):
            Exercise(
                id="invalid-lab",
                title="Invalid Lab",
                description="Invalid exercise content.",
                steps=["Complete the exercise."],
                verification="Verify completion.",
                objective_ids="iam-users",
            )
