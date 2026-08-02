from app.cli.renderer import BrightRenderer
from app.core.learning.session_controller import SessionController


def main():

    controller = SessionController(
        "knowledge/cloud/frameworks/aws-sa.yaml"
    )

    session = controller.start()

    renderer = BrightRenderer()

    renderer.render_framework(
        session.learning_plan.framework
    )

    renderer.render_milestone(
        session.learning_plan.milestone
    )

    renderer.render_objectives(
        session.objectives
    )

    renderer.render_resources(
        session.resources
    )

    renderer.render_exercises(
        session.exercises
    )

    renderer.render_assessment(
        session.assessment
    )

    print("\nRenderer test passed.")


if __name__ == "__main__":
    main()