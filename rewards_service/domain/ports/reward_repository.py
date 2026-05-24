from abc import ABC, abstractmethod
from typing import Optional

from rewards_service.domain.model.reward_account import RewardAccount


class RewardRepository(ABC):
    @abstractmethod
    def find_by_card(self, card_number: str) -> Optional[RewardAccount]:
        raise NotImplementedError

    @abstractmethod
    def save(self, account: RewardAccount) -> None:
        raise NotImplementedError
