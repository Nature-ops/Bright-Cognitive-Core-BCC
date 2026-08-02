from app.cli.cli import BrightCLI
from app.core.learning.session_controller import SessionController


def main():

    controller = SessionController(
        "knowledge/cloud/frameworks/aws-sa.yaml"
    )

    cli = BrightCLI(controller)

    cli.run()



if __name__ == "__main__":
    main()