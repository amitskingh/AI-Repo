from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str

    def format(self) -> str:
        return f"{self.role}: {self.content}"


class ChatBot:
    def __init__(
        self,
        name: str,
        model_name: str,
        temperature: float = 0.2,
    ):
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0.")

        self.name = name
        self.model_name = model_name
        self.temperature = temperature
        self.history: list[Message] = []

    def greet(self):
        return f"Hello! I am {self.name}, your friendly chatbot."

    def add_message(self, role: str, content: str) -> Message:
        message = Message(role, content)
        self.history.append(message)
        return message

    def generate_reply(self, prompt: str) -> str:
        self.add_message(
            role="user",
            content=prompt,
        )

        reply = f"I am {self.name}, using {self.model_name}. You asked: {prompt}"

        self.add_message(
            role="assistant",
            content=reply,
        )

        return reply

    def show_history(self) -> str:
        formatted_messages = [message.format() for message in self.history]
        return "\n".join(formatted_messages)

    def clear_history(self) -> None:
        self.history.clear()


bot = ChatBot(
    name="Python Mentor",
    model_name="example-model",
    temperature=0.2,
)

reply_1 = bot.generate_reply("What is a function?")

reply_2 = bot.generate_reply("Why do classes exist?")

print(reply_1)
print()
print(reply_2)
print()
print("Conversation history:")
print(bot.show_history())
# Show the internal state of the bot's history just like how langchain does it. This is useful for debugging and understanding the flow of messages.
print(bot.history)  # This will print the list of Message objects in the history.
