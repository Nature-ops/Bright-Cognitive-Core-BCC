
from app.services.framework_loader import FrameworkLoader

def main():
    framework = FrameworkLoader.load(
        "knowledge/cloud/frameworks/aws-sa.yaml"
    )

    print("=" * 50)
    print(framework)
    print("=" * 50)

    print()

    print("Framework:", framework.name)
    print("Domain:", framework.domain)
    print("Version:", framework.version)

    print()

    print("Milestones:")

    for milestone in framework.milestones:
        print(f"- {milestone.title}")


if __name__ == "__main__":
    main()