import logging
from datetime import datetime
import traceback
import yaml
import textwrap
import types

# =======================================================================================
# MISC.PY - Miscellaneous Utilities
# =======================================================================================
# This section of the misc.py module is dedicated to miscellaneous utility classes and
# functions that don't necessarily fit into the main thematic modules of the application
# but are essential for handling specific tasks such as file manipulation, string
# processing, or any other utility operations needed across the project.
# =======================================================================================
# =======================================================================================
# LOGGING FORMATTER
# =======================================================================================
# This section contains the class definition for the YAML formatter for the
# logging facility.
# =======================================================================================


class EnhancedYamlFormatter(logging.Formatter):
    last_timestamp = ""
    timestamp_counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        yaml.add_representer(str, self.representer_multiline_str, Dumper=yaml.SafeDumper)
        yaml.add_representer(object, lambda dumper, obj: dumper.represent_str(str(obj)))

    @staticmethod
    def representer_multiline_str(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    def format(self, record):
        timestamp_format = "%Y-%m-%d %H:%M:%S"
        formatted_timestamp = datetime.utcfromtimestamp(record.created).strftime(timestamp_format)

        # Check if this timestamp is the same as the last one
        if formatted_timestamp == self.last_timestamp:
            self.timestamp_counter += 1
        else:
            self.last_timestamp = formatted_timestamp
            self.timestamp_counter = 1  # Reset counter for new timestamp

        # Append the counter to the timestamp to make it unique
        unique_timestamp = f"{formatted_timestamp}.{self.timestamp_counter}"

        message = record.msg
        if isinstance(message, dict) or isinstance(message, types.SimpleNamespace):
            message = self.convert_to_dict(message)
            message = yaml.dump(message, Dumper=yaml.SafeDumper, default_flow_style=False, sort_keys=False)

        structured_log = {
            "time": unique_timestamp,
            "level": record.levelname,
            "line": record.lineno,
            "function": record.funcName,
            "file": record.filename,
            "message": message,
        }

        if record.exc_info:
            tb_list = traceback.format_exception(*record.exc_info)
            indented_tb = textwrap.indent("".join(tb_list), prefix="    ")
            structured_log["exception"] = indented_tb

        log_entry = {unique_timestamp: structured_log}

        return yaml.dump(log_entry, Dumper=yaml.SafeDumper, default_flow_style=False, sort_keys=False)

    def convert_to_dict(self, obj):
        if isinstance(obj, types.SimpleNamespace):
            return {k: self.convert_to_dict(v) for k, v in vars(obj).items()}
        elif isinstance(obj, dict):
            return {k: self.convert_to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_to_dict(v) for v in obj]
        else:
            return obj.__str__().strip('"')
