from .fogg_behavioral_model import Patient


class Profile3Patient(Patient):
    """Profile 3: personal-record-motivated, fatigue-sensitive, stress-neutral.
    - Motivation bonus when activity_p >= personal daily best (on pace to break record).
    - Insufficient sleep penalises ability by -2.
    - Stress (high arousal) has no special treatment beyond base model (neutral).
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('behavior_threshold', 20)
        # Must set before super().__init__() because it calls reset() -> get_motivation()
        self.personal_best_daily = None
        super().__init__(**kwargs)

    def update_after_day(self):
        if self.personal_best_daily is None or self.activity_p > self.personal_best_daily:
            self.personal_best_daily = self.activity_p
        super().update_after_day()

    def get_motivation(self):
        base = super().get_motivation()
        record_bonus = 1 if (
            self.personal_best_daily is not None and
            self.activity_p >= self.personal_best_daily
        ) else 0
        return base + record_bonus

    def get_ability(self):
        base = super().get_ability()
        if self.awake_list[-24:].count('sleeping') < 7:
            base -= 2
        return base
