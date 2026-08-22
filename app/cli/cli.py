from app.cli.menu import BrightMenu
from app.cli.renderer import BrightRenderer
from app.core.learning.session_controller import SessionController


class BrightCLI:

    def __init__(
        self,
        controller: SessionController,
    ):
        self.controller = controller
        self.renderer = BrightRenderer()
        self.menu = BrightMenu()

    def run(self):

        session = self.controller.start()

        if session is None:

            self.renderer.render_welcome()

            print()
            print("🎉 Learning framework completed!")
            print()
            print(
                "Congratulations! You have completed all milestones."
            )

            return

        self.renderer.render_welcome()

        self.renderer.render_framework(
            session.learning_plan.framework
        )

        self.renderer.render_milestone(
            session.learning_plan.milestone
        )

        while True:

            choice = self.menu.show_main_menu()

            result = self.handle_choice(choice)

            if not result:
                break

    def show_objectives(self):

        objectives = self.controller.objectives()

        completed = self.controller.completed_objectives()

        self.renderer.render_objectives(
            objectives,
            completed,
        )

    def show_resources(self):

        resources = self.controller.resources()

        self.renderer.render_resources(
            resources
        )

    def show_exercises(self):

        self.renderer.render_exercises(
            self.controller.exercises()
        )

    def take_assessment(self):

        assessment = (
            self.controller.current_assessment()
        )

        self.renderer.render_assessment(
            assessment
        )

    def show_progress(self):

        session = self.controller.study_engine.session

        if session is None:

            print("\nNo active learning session.")

            return

        framework = (
            session.learning_plan.framework
        )

        progress = (
            self.controller.milestone_progress()
        )

        completed = (
            self.controller.study_engine
            .framework_progress_service
            .get_progress(framework.id)
            .completed_milestones
        )

        self.renderer.render_milestone_progress(
            framework,
            completed,
            progress,
        )

    def handle_choice(
        self,
        choice: int,
    ) -> bool:

        if choice == 1:

            self.continue_learning()

        elif choice == 2:

            self.show_objectives()

        elif choice == 3:

            self.show_resources()

        elif choice == 4:

            self.show_exercises()

        elif choice == 5:

            self.take_assessment()

        elif choice == 6:

            self.show_progress()

        elif choice == 7:

            print("\nGoodbye!")

            return False

        else:

            print("\nInvalid option.")

        return True

    def continue_learning(self):

        state, item = (
            self.controller.learning_state()
        )

        if state == "objective":

            self.renderer.render_current_objective(
                item
            )

            input(
                "\nPress ENTER when completed..."
            )

            completed = (
                self.controller
                .complete_current_objective()
            )

            if completed is not None:

                self.renderer.render_objective_completed(
                    completed
                )

                self.renderer.render_progress(
                    self.controller.objective_progress()
                )

                next_state, next_item = (
                    self.controller.learning_state()
                )

                if next_state == "objective":

                    self.renderer.render_current_objective(
                        next_item
                    )

            return

        elif state == "exercise":

            self.renderer.render_current_exercise(
                item
            )

            input(
                "\nPress ENTER when completed..."
            )

            completed = (
                self.controller
                .complete_current_exercise()
            )

            if completed is not None:

                self.renderer.render_exercise_completed(
                    completed
                )

                self.renderer.render_exercise_progress(
                    self.controller.exercise_progress()
                )

            next_state, next_item = (
                self.controller.learning_state()
            )

            if next_state == "assessment":

                self.renderer.render_assessment(
                    next_item
                )

            return

        elif state == "assessment":

            self.run_assessment(
                item
            )

            return

        else:

            print()

            if self.controller.session_completed():

                print("🎉 Session completed!")

                print()
                print("Congratulations!")

                next_session = (
                    self.controller
                    .advance_to_next_milestone()
                )

                if next_session is None:

                    print()
                    print("🎉 Learning framework completed!")
                    print()
                    print(
                        "Congratulations! You have completed all milestones."
                    )

                else:

                    self.renderer.render_framework(
                        next_session.learning_plan.framework
                    )

                    self.renderer.render_milestone(
                        next_session.learning_plan.milestone
                    )

            return

    def run_assessment(
        self,
        assessment,
    ):

        answers = {}

        for index, question in enumerate(
            assessment.questions,
            start=1,
        ):

            self.renderer.render_question(
                question,
                index,
                len(assessment.questions),
            )

            while True:

                answer = input(
                    "\nYour answer: "
                ).strip()

                try:

                    answer_index = int(answer) - 1

                    selected_answer = (
                        question.options[answer_index]
                    )

                except (ValueError, IndexError):

                    print(
                        "Invalid input. "
                        "Please enter a valid number."
                    )

                    continue

                answers[question.id] = (
                    selected_answer
                )

                break

        result = (
            self.controller.submit_assessment(
                answers
            )
        )

        print()

        self.renderer.render_heading(
            "Assessment Result"
        )

        print(
            f"Correct: {result.correct_answers} / "
            f"{result.total_questions}"
        )

        print(
            f"Score: {result.score:.0f}%"
        )

        status = (
            "PASSED"
            if result.passed
            else "FAILED"
        )

        print(
            f"Status: {status}"
        )

        if result.passed:

            print()

            next_session = (
                self.controller
                .advance_to_next_milestone()
            )

            if next_session is None:

                print(
                    "🎉 Milestone completed!"
                )

                print()
                print("🎉 Learning framework completed!")
                print()
                print(
                    "Congratulations! You have completed all milestones."
                )

            else:

                print(
                    "🎉 Milestone completed!"
                )

                self.renderer.render_framework(
                    next_session.learning_plan.framework
                )

                self.renderer.render_milestone(
                    next_session.learning_plan.milestone
                )

        else:

            print()

            print(
                "Assessment not passed."
            )

            print(
                "Review the material and try again."
            )
