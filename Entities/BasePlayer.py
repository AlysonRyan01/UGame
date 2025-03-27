from abc import ABC, abstractmethod

class BasePlayer(ABC):
    def __init__(self, name):
        self.name = name
        self.score = 1500

    def update_score(self, roulette_score):
        self.score -= 400
        self.score += roulette_score

    def get_score(self):
        return self.score
