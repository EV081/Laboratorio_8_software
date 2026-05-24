from typing import Dict, Optional

from rewards_service.domain.model.reward_account import RewardAccount
from rewards_service.domain.ports.reward_repository import RewardRepository


class InMemoryRewardRepository(RewardRepository):
    def __init__(self) -> None:
        self._accounts: Dict[str, RewardAccount] = {}

    def find_by_card(self, card_number: str) -> Optional[RewardAccount]:
        return self._accounts.get(card_number)

    def save(self, account: RewardAccount) -> None:
        self._accounts[account.card_number] = account
