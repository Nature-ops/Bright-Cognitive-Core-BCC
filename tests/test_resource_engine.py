from app.services.resource_engine import ResourceEngine


def main():

    engine = ResourceEngine()

    engine.load_directory(
        "knowledge/cloud/resources"
    )

    print("=" * 60)
    print("Available Resources")
    print("=" * 60)

    for resource in engine.get_resources():

        print()

        print(resource.id)
        print(resource.title)

        if hasattr(resource, "url"):
            print(resource.url)


if __name__ == "__main__":
    main()