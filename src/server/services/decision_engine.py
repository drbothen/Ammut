from typing import List, Dict, Any, Optional

from models.schemas import TargetProfile, ToolEffectiveness, AttackPattern
from models.enums import TargetType, AttackPhase
from .base import AbstractDecisionEngine

class IntelligentDecisionEngine(AbstractDecisionEngine):
    """Provides intelligent tool and attack pattern selection."""

    def __init__(self):
        self.tool_effectiveness: List[ToolEffectiveness] = []
        self.attack_patterns: Dict[str, AttackPattern] = {}
        self._load_initial_data()

    def _load_initial_data(self):
        # In a real application, this would be loaded from a database or config file.
        self.tool_effectiveness = [
            ToolEffectiveness(tool_name='nmap', target_type=TargetType.NETWORK, effectiveness_score=0.9),
            ToolEffectiveness(tool_name='gobuster', target_type=TargetType.WEB_APP, effectiveness_score=0.8),
            ToolEffectiveness(tool_name='nuclei', target_type=TargetType.WEB_APP, effectiveness_score=0.85),
            ToolEffectiveness(tool_name='sqlmap', target_type=TargetType.WEB_APP, effectiveness_score=0.95),
        ]

        self.attack_patterns = {
            "web_common": AttackPattern(
                pattern_id="web_common",
                name="Common Web Application Attack Pattern",
                target_type=TargetType.WEB_APP,
                phases=[AttackPhase.RECONNAISSANCE, AttackPhase.SCANNING],
                recommended_tools=['nmap', 'gobuster', 'nuclei']
            )
        }

    def select_tool(self, target_profile: TargetProfile, phase: str) -> Optional[str]:
        """Selects the best tool for a given target and attack phase."""
        applicable_tools = [t for t in self.tool_effectiveness if t.target_type == target_profile.target_type]
        
        if not applicable_tools:
            return None

        # Simple selection logic: return the tool with the highest effectiveness score.
        best_tool = max(applicable_tools, key=lambda t: t.effectiveness_score)
        return best_tool.tool_name

    def get_attack_pattern(self, target_type: str) -> Optional[AttackPattern]:
        """Retrieves an attack pattern for a given target type."""
        # Simplified logic for demonstration.
        pattern_key = f"{target_type.value.lower()}_common"
        return self.attack_patterns.get(pattern_key)

decision_engine = IntelligentDecisionEngine()
