from dataclasses import dataclass, field
from typing import Dict


@dataclass
class RulesStorage:
    rules: Dict[str, str] = field(default_factory=dict)

    async def add_rule(self, rules: Dict[str, str]):
        self.rules.update(rules)
    
    async def delete_rule(self, rule_name:str):
        self.rules.pop(rule_name, None)
    
    async def get_data(self):
        return self.rules.copy()
