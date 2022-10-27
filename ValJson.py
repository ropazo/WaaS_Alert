import json
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "OperationId": {"type": "string"},
        "Status": {"type": "string"},
        "value_a": {"type": "string"},
        "value_b": {"type": "string"},
    },
}

my_json = {
    "OperationId": "50676784-211a-4fc6-a410-8bdd658b0759",
    "Status": "ERROR",
    "Message": "El horario de atención al cliente está completo para los próximos días. Inténtelo más tarde.",
    "FailureReason": "TASK_FINISHED"
}

validate(instance=my_json, schema=schema)
