import numpy as np
from .fogg_behavioral_model import Patient


class Profile2Patient(Patient):
    """Profile 2: competitive + peer-motivated + stress/fatigue-sensitive.
    - Motivation bonus when current intra-day RR exceeds peer baseline mean for that day.
    - Motivation bonus when activity_p >= personal daily best (on pace to break record).
    - Stress (high arousal + negative valence) collapses trigger to 0 (as Profile 1).
    - Insufficient sleep penalises ability by -2 (as Profile 1).
    """
    def __init__(self, peer_rr_baseline=None, **kwargs):
        kwargs.setdefault('behavior_threshold', 20)
        # Must set before super().__init__() because it calls reset() -> get_motivation()
        self.peer_rr_baseline = peer_rr_baseline if peer_rr_baseline is not None else np.zeros(56)
        self.day_index = 0
        self.personal_best_daily = None
        super().__init__(**kwargs)

    def update_after_day(self):
        if self.personal_best_daily is None or self.activity_p > self.personal_best_daily:
            self.personal_best_daily = self.activity_p
        self.day_index += 1
        super().update_after_day()

    def get_motivation(self):
        base = super().get_motivation()
        # Peer comparison bonus
        current_rr = self.activity_p / self.activity_s if self.activity_s > 0 else 0.0
        if len(self.peer_rr_baseline) == 0:
            peer_bonus = 0
        else:
            day = min(self.day_index, len(self.peer_rr_baseline) - 1)
            peer_bonus = 1 if current_rr > self.peer_rr_baseline[day] else 0
        # Personal record bonus
        record_bonus = 1 if (
            self.personal_best_daily is not None and
            self.activity_p >= self.personal_best_daily
        ) else 0
        return base + peer_bonus + record_bonus

    def get_trigger(self):
        is_stressed = (self.arousal == 2 and self.valence == 0)
        if is_stressed:
            return 0
        return super().get_trigger()

    def get_ability(self):
        base = super().get_ability()
        if self.awake_list[-24:].count('sleeping') < 7:
            base -= 2
        return base
