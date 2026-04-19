from .fogg_behavioral_model import Patient


class Profile1Patient(Patient):
    """Profile 1: sensitive to both stress and fatigue.
    Stress (high arousal + negative valence) collapses trigger to 0.
    Insufficient sleep (<7h) penalises ability by -2.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('behavior_threshold', 20)
        super().__init__(**kwargs)

    def get_trigger(self):
        is_stressed = (self.arousal == 2 and self.valence == 0)
        if is_stressed:
            return 0
        return super().get_trigger()

    def get_ability(self):
        base = super().get_ability()
        hours_slept = self.awake_list[-24:].count('sleeping')
        if hours_slept < 7:
            base -= 2
        return base
