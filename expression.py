from abc import ABC, abstractmethod

class Expression(ABC):

    @abstractmethod
    def print(self):
        pass