from rewards_service.domain.model.dinner_event import DinnerEvent
from rewards_service.domain.model.reward_account import RewardAccount
from rewards_service.domain.policy.points_policy import PointsPolicy
from rewards_service.domain.ports.notification_publisher import NotificationPublisher
from rewards_service.domain.ports.reward_repository import RewardRepository


class ProcessDinnerUseCase:
    def __init__(
        self,
        repository: RewardRepository,
        policy: PointsPolicy,
        notifier: NotificationPublisher,
    ) -> None:
        self._repository = repository
        self._policy = policy
        self._notifier = notifier

    def execute(self, event: DinnerEvent) -> RewardAccount:
        account = self._repository.find_by_card(event.card_number)
        if account is None:
            account = RewardAccount(card_number=event.card_number)
        points = self._policy.calculate(event.amount)
        account.add_points(points)
        self._repository.save(account)
        self._notifier.publish_reward_processed(
            card_number=account.card_number,
            points_added=points,
            total_points=account.points,
        )
        return account
