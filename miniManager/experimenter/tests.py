from django.test import TestCase
from experimenter.listener import ExperimentListener


class ExperimentListenerTest(TestCase):
    ROUND_ID = 1
    def test_constructor(self):
        experimentListener = ExperimentListener(self.ROUND_ID)
        self.assertEqual(experimentListener.roundID, self.ROUND_ID)
        self.assertEqual(experimentListener.started, False)

