import attrs
from fileformats.generic import Directory
import logging
import os
from pydra.compose import python


logger = logging.getLogger(__name__)


@python.define
class TrainingSetCreator(python.Task["TrainingSetCreator.Outputs"]):
    """
    Examples
    -------

    >>> from fileformats.generic import Directory
    >>> from pydra.tasks.fsl.v6.fix.training_set_creator import TrainingSetCreator

    """

    mel_icas_in: list[Directory]

    class Outputs(python.Outputs):
        mel_icas_out: list[Directory]

    @staticmethod
    def function(mel_icas_in: list[Directory]) -> list[Directory]:
        mel_icas_out = attrs.NOTHING
        self_dict = {}
        mel_icas = [
            item
            for item in mel_icas_in
            if os.path.exists(os.path.join(item, "hand_labels_noise.txt"))
        ]
        if len(mel_icas) == 0:
            raise Exception(
                "%s did not find any hand_labels_noise.txt files in the following directories: %s"
                % (self_dict["__class__"].__name__, mel_icas)
            )

        mel_icas = [
            item
            for item in mel_icas_in
            if os.path.exists(os.path.join(item, "hand_labels_noise.txt"))
        ]
        outputs = {}
        mel_icas_out = mel_icas

        return mel_icas_out
