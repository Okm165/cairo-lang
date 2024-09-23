from dataclasses import field
from typing import List
import marshmallow.fields as mfields
import marshmallow_dataclass
from starkware.starkware_utils.marshmallow_dataclass_fields import additional_metadata
from starkware.starkware_utils.validated_dataclass import ValidatedMarshmallowDataclass
from starkware.cairo.bootloaders.simple_bootloader.objects import TaskSpec, TaskSchema


@marshmallow_dataclass.dataclass(frozen=True)
class ApplicativeBootloaderInput(ValidatedMarshmallowDataclass):
    aggregator_task: TaskSpec = field(
        metadata=additional_metadata(marshmallow_field=mfields.Nested(TaskSchema))
    )

    tasks: List[TaskSpec] = field(
        metadata=additional_metadata(
            marshmallow_field=mfields.List(mfields.Nested(TaskSchema))
        )
    )
