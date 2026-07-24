from app.services.skill_engine import SkillEngine


def main():

    engine = SkillEngine()

    engine.load_directory(
        "knowledge/cloud/skills"
    )

    print("=" * 60)
    print("Available Skills")
    print("=" * 60)

    for skill in engine.get_skills():

        print()

        print(skill.id)
        print(skill.name)

        if hasattr(skill, "description"):
            print(skill.description)


if __name__ == "__main__":
    main()