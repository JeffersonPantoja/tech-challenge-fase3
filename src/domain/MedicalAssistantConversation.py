from dataclasses import dataclass, field

from src.domain.MedicalAssistantMessage import MedicalAssistantMessage


@dataclass
class MedicalAssistantConversation:
    messages: list[MedicalAssistantMessage] = field(default_factory=list)

    def add_user_message(self, content: str) -> None:
        self.messages.append(MedicalAssistantMessage(role="user", content=content))

    def add_assistant_message(self, content: str) -> None:
        self.messages.append(MedicalAssistantMessage(role="assistant", content=content))
