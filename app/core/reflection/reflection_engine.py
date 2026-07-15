from datetime import UTC, datetime
from app.core.base.cognitive_engine import CognitiveEngine
from app.core.reflection.insights import Insight
from app.core.reflection.reflection_rules import ReflectionRules
from app.core.state.cognitive_state import CognitiveState
from app.services.insight_service import InsightService
from app.utils.logger import logger


class ReflectionEngine:

    def __init__(self):
        self.insight_service = InsightService()

    def _now(
        self,
    )-> str:
        return datetime.now(UTC).isoformat()

    def process(
        self,
        state: CognitiveState
    ) -> CognitiveState:

        text = state.message.lower()
        
        insight = None
        
        if self._detect_achievement(text):

            insight = self._create_achievement_insight()

        elif self._detect_goal_progress(text):

            insight = self._create_goal_insight()

        elif self._detect_habit(text):

            insight = self._create_habit_insight()
        
        if insight:   
             
             self._save_insight(insight)

        return state



    def _save_insight(
        self,
        insight: Insight  

    ) -> None:  
            
        self.insight_service.add(insight)           

        logger.info(
            f"Reflection created {insight.category} insight: {insight.title}"
        )

            
        
      
    

    def _detect_achievement(
        self,
        text: str
    ) -> bool:

        for keyword in ReflectionRules.ACHIEVEMENTS:

            if keyword in text:
                return True

        return False
    

    def _create_learning_insight(
        self
    ) -> Insight:

        return Insight(
            title="Learning Milestone",
            description="User completed a learning objective.",
            category="learning",
            confidence=0.95,
            source="reflection",
            created_at=self._now(),
        )



    def _create_goal_insight(
        self,
        
    ) -> Insight:

        return Insight(
            title="Goal Progress",
            description="User made progress toward a goal.",
            category="goal",
            confidence=0.90,
            source="reflection",
            created_at=self._now(),
    )
        



    def _create_achievement_insight(
        self,
        
    ) -> Insight:

        return Insight(
            title="Achievement",
            description="User achieved an important milestone",
            category="achievement",
            confidence=0.90,
            source="reflection",
            created_at=self._now(),
    )
        




    def _create_habit_insight(
        self,
        
    ) -> Insight:

        return Insight(
            title="Habit",
            description="Reflection detected a recurring behavior.",
            category="habit",
            confidence=0.90,
            source="reflection",
            created_at=self._now(),
    )
        




    def _detect_goal_progress(
        self,
        text: str
    ) -> bool:
        return False



    def _detect_task_completion(
        self,
        text: str
    ) -> bool:
        return False




    def _detect_habit(
        self,
        text: str
    ) -> bool:
        return False



    def _detect_preference_change(
        self,
        text: str
    ) -> bool:
        return False

