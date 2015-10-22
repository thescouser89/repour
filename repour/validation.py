import logging

from voluptuous import *

from . import adjust as adjustmodule
from . import pull as pullmodule
from . import repo

#
# Primitives
#

nonempty_str = All(str, Length(min=1))
nonempty_noblank_str = All(str, Match(r'^\S+$'))
port_num = All(int, Range(min=1, max=65535))
name_str = Match(r'^[a-zA-Z0-9_.][a-zA-Z0-9_.-]*(?<!\.git)$')

#
# Adjust
#

adjust_raw = {
    "name": name_str,
    "ref": nonempty_str,
}

adjust = Schema(
    adjust_raw,
    required=True,
    extra=False,
)

#
# Pull
#
pull_scm = Schema(
    {
        "name": name_str,
        "type": Any(*pullmodule.scm_types),
        Optional("ref"): nonempty_str,
        "url": Url(), #pylint: disable=no-value-for-parameter
        Optional("adjust"): bool,
    },
    required=True,
    extra=False,
)

pull_archive = Schema(
    {
        "name": name_str,
        "type": pullmodule.archive_type,
        "url": Url(), #pylint: disable=no-value-for-parameter
        Optional("adjust"): bool,
    },
    required=True,
    extra=False,
)

pull_raw = Any(pull_scm, pull_archive)

pull = Schema(
    pull_raw,
    required=True,
    extra=False,
)

#
# Returns
#

error_validation = Schema(
    [{
        "error_message": str,
        "path": [str],
        "error_type": str,
    }],
    required=True,
    extra=False,
)

error_described = Schema(
    {
        "error_type": nonempty_str,
        "error_traceback": nonempty_str,
        str: object,
    },
    required=True,
    extra=False,
)

error_other = Schema(
    {
        "error_type": nonempty_str,
        "error_traceback": nonempty_str,
    },
    required=True,
    extra=False,
)

success_pull = Schema(
    {
        "branch": nonempty_str,
        "tag": nonempty_str,
        "url": {
            "readonly": Url(), #pylint: disable=no-value-for-parameter
            "readwrite": Url(), #pylint: disable=no-value-for-parameter
        },
    },
    required=True,
    extra=False,
)

success_adjust = success_pull

success_pull_adjust = Schema(
    {
        "branch": nonempty_str,
        "tag": nonempty_str,
        "url": {
            "readonly": Url(), #pylint: disable=no-value-for-parameter
            "readwrite": Url(), #pylint: disable=no-value-for-parameter
        },
        "pull": success_pull,
    },
    required=True,
    extra=False,
)

#
# Server configuration
#

server_config_raw = {
    "log": {
        "path": nonempty_str,
        "level": Any(*logging._nameToLevel.keys()),
    },
    "bind": {
        "address": Any(nonempty_str, None),
        "port": port_num,
    },
    "adjust_provider": {
        "type": Any(*adjustmodule.provider_types.keys()),
        "params": {Extra: object},
    },
    "repo_provider": {
        "type": Any(*repo.provider_types.keys()),
        "params": {Extra: object},
    },
}
server_config = Schema(
    server_config_raw,
    required=True,
    extra=False,
)
