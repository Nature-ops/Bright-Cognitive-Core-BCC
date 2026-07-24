from app.services.assessment_loader import AssessmentLoader


def main():

    loader = AssessmentLoader()

    assessment = loader.load(
        "knowledge/cloud/assessments/iam.yaml"
    )

    print("=" * 60)
    print(assessment.title)
    print("=" * 60)

    print(assessment.description)

    print("\nPassing Score")

    print(assessment.passing_score)

    print("\nQuestions")

    for question in assessment.questions:

        print()

        print(question.id)
        print(question.prompt)

        for option in question.options:
            print(f" - {option}")

        print(f"Answer: {question.answer}")


if __name__ == "__main__":
    main()