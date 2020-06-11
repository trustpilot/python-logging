import json
from io import StringIO

import trustpilot_json_logging


def test_advanced():
    buffer = StringIO()
    logging = trustpilot_json_logging.setup_logging(
        "INFO", buffer, ignore={"elasticsearch": "WARNING"}
    )

    logging.info({"message": "i just arrived", "age": 32, "location": "north pole"})

    buffer.seek(0)
    output = buffer.read()
    print(output)
    lines = [json.loads(line) for line in output.split("\n") if line]
    assert lines == [
        {
            "message": "Setup logging with level:WARNING, ignore: [elasticsearch=WARNING]",
            "Module": "root",
            "Severity": "INFO",
        },
        {
            "message": "i just arrived",
            "age": 32,
            "location": "north pole",
            "Module": "root",
            "Severity": "INFO",
        },
    ]


def test_uppercasing_if_string():
    buffer = StringIO()
    logging = trustpilot_json_logging.setup_logging(
        "info", buffer, ignore={"elasticsearch": "warning"}
    )

    logging.info({"message": "i just arrived", "age": 32, "location": "north pole"})

    buffer.seek(0)
    output = buffer.read()
    print(output)
    lines = [json.loads(line) for line in output.split("\n") if line]
    assert lines == [
        {
            "message": "Setup logging with level:WARNING, ignore: [elasticsearch=WARNING]",
            "Module": "root",
            "Severity": "INFO",
        },
        {
            "message": "i just arrived",
            "age": 32,
            "location": "north pole",
            "Module": "root",
            "Severity": "INFO",
        },
    ]

