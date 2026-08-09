from abc import ABC, abstractmethod


class Runnable(ABC):
    @abstractmethod
    def invoke(self, *args, **kwargs):
        pass


class ChatPromptTemplate(Runnable):
    def __init__(self, template: str):
        self.template = template

    def invoke(self, **kwargs):
        return self.template.format(**kwargs)


class Model(Runnable):
    def __init__(self, name: str):
        self.name = name

    def invoke(self, prompt: str):
        # Simulate model response
        return f"Model {self.name} response to: {prompt}"


model: Runnable = Model(name="gpt-4o-mini")

print(model.invoke("What is Python?"))

prompt = ChatPromptTemplate(template="Explain {topic} in simple terms.")
print(prompt.invoke(topic="embeddings"))
