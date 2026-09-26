from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def chat(self, message):
        pass

    @abstractmethod
    def classify(self, message, instruction):
        pass
