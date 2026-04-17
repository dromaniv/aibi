from environment.fogg_behavioral_model import Patient


class Profile0Patient(Patient):
    """Profile 0: neutral, low-sensitivity patient.
    No peer comparison, no record motivation, not blocked by stress or fatigue.
    Effectively the base Patient with behavior_threshold=20.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault('behavior_threshold', 20)
        super().__init__(**kwargs)
