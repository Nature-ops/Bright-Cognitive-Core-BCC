





class BrightRenderer:
    """Responsible for rendering information to the terminal."""

    def __init__(self):
        pass

    def render_welcome(self):

        
        print("Bright Assistant") 

        print("The Engineering Operating System")
        

    def render_framework(self, framework) -> None:

        self.render_heading("Framework")

        print(framework.name)


    def render_milestone(self, milestone) -> None:

        self.render_heading("Current Milestone")

        print(milestone.title)

        if milestone.description:

            print()

            print(milestone.description)



    def render_resources(
        self,
        resources,
    ) -> None:

        self.render_heading("Resources")

        for resource in resources:

            print(f"• {resource.title}")

            if resource.url:

                print(f"  {resource.url}")


    def render_exercises(
        self,
        exercises,
    ) -> None:

        self.render_heading("Exercises")

        if not exercises:

            print("No exercises.")

            return

        for exercise in exercises:

            print(f"• {exercise.title}")


    def render_assessment(
        self,
        assessment,
    ) -> None:

        self.render_heading("Assessment")

        if assessment is None:

            print("No assessment.")

            return

        print(assessment.title)


    def divider(self) -> None:

        print("=" * 50)


    def render_heading(
        self,
        title: str,
    ) -> None:

        print()

        print(title)

        print("-" * len(title))


    def render_banner(
        self,
        title: str,
    ) -> None:

        print("=" * 50)

        print(title)

        print("=" * 50)


    def render_current_objective(
        self,
        objective,
    ):

        self.render_heading(
            "Current Objective"
        )

        if objective is None:

            print("No objectives remaining.")

            return

        print(objective.title)


    def render_progress(
        self,
        progress: float,
    ):

        print()

        print(
            f"Progress: {progress:.0f}%"
        )


    def render_objective_completed(
        self,
        objective,
    ) -> None:

        print()

        print(f"✓ {objective.title} completed.")



    def render_objectives(
        self,
        objectives,
        completed_ids,
    ):

        self.render_heading("Objectives")

        if not objectives:

            print("No objectives.")

            return

        for objective in objectives:

            mark = (
                "✓"
                if objective.id in completed_ids
                else "☐"
            )

            print(
                f"{mark} {objective.title}"


            )

    def render_current_exercise(
        self,
        exercise,
    ):

        self.render_heading(
            "Current Exercise"
        )

        if exercise is None:

            print("No exercises remaining.")

            return

        print(exercise.title)   



    def render_exercise_completed(
        self,
        exercise,
    ):

        print()

        print(f"✓ {exercise.title} completed.")


    def render_exercise_progress(
        self,
        progress: float,
    ):

        print()

        print(
            f"Exercise Progress: {progress:.0f}%"
        )

    def render_milestone_progress(
        self,
        framework,
        completed_ids,
        progress: float,
    ) -> None:

        self.render_heading("Progress")

        print()
        print(f"Framework: {framework.name}")

        print()
        print("Milestones")
        print("----------")

        for milestone in framework.milestones:

            mark = (
                "✓"
                if milestone.id in completed_ids
                else "○"
            )

            print(f"{mark} {milestone.title}")

        print()
        print(f"Overall Progress: {progress:.0f}%")

        completed = sum(
            1
            for milestone in framework.milestones
            if milestone.id in completed_ids
        )

        total = len(framework.milestones)

        print()
        print(f"Completed: {completed} / {total}")

    


    def render_question(
        self,
        question,
        number: int,
        total: int,
    ):

        self.render_heading(
            f"Question {number} of {total}"
        )

        print(question.prompt)

        print()

        for index, option in enumerate(
            question.options,
            start=1):

            print(f"{index}. {option}")





           


            


        
                