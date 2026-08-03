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

        objectives = (
            self.controller.objectives()
        )

        completed = (
            self.controller.completed_objectives()
        )

        self.renderer.render_objectives(
            objectives,
            completed,
        )

    def show_resources(self):
        print("Resources coming soon.")

    def show_exercises(self):
        print("Exercises coming soon.")

    def take_assessment(self):
        print("Assessment coming soon.")

    def show_progress(self):
        print("Progress coming soon.")





    

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
        objective = self.controller.current_objective()
    
        self.renderer.render_current_objective(
            objective
        )
    
        if objective is None:
            print()

            print("All objectives have been completed.")

            return
    
        input(
            "\nPress ENTER when completed..."
        )
    
        completed = (
            self.controller.complete_current_objective()
        )
    
        if completed is not None:
    
           self.renderer.render_objective_completed(
            completed
            )
           self.renderer.render_progress(
                self.controller.objective_progress()
              )
           next_objective = self.controller.current_objective()

           self.renderer.render_current_objective(
               next_objective
              )
        
            

                    