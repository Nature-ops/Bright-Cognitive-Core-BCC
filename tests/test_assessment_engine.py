from app.services.assessment_engine import AssessmentEngine


def main():

    engine = AssessmentEngine()

    engine.load_directory(
        "knowledge/cloud/assessments"
    )

    print("=" * 60)
    print("Available Assessments")
    print("=" * 60)

    for assessment in engine.get_assessments():

        print()

        print(assessment.id)
        print(assessment.title)

        print(
            f"Questions: {len(assessment.questions)}"
        )

        print(
            f"Passing Score: {assessment.passing_score}"
        )


if __name__ == "__main__":
    main()