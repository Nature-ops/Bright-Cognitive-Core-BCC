from app.services.framework_engine import FrameworkEngine


def main():

    engine = FrameworkEngine()

    engine.load_directory(
        "knowledge/cloud/frameworks"
    )

    print("=" * 60)
    print("Available Frameworks")
    print("=" * 60)

    for framework in engine.get_frameworks():

        print()

        print(framework.id)
        print(framework.name)

        print(f"Milestones: {len(framework.milestones)}")


if __name__ == "__main__":
    main()