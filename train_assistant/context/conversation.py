from typing import Optional

class ConversationContext:
    def __init__(self):
        self.history = []
        self.last_route = None

    def get_history(self) -> str:
        return "\n".join(self.history[-4:])  # Keep last 4 messages
    
    def update_last_route(self, route: str):
        self.last_route = route
    
    def get_last_route(self) -> Optional[str]:
        return self.last_route

context = ConversationContext()