# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

from airflow import configuration
from airflow.executors.base_executor import BaseExecutor
from airflow.executors.local_executor import LocalExecutor
from airflow.executors.sequential_executor import SequentialExecutor

from airflow.exceptions import AirflowException


def _integrate_plugins():
    """Integrate plugins to the context."""
    from airflow.plugins_manager import executors_modules
    for executors_module in executors_modules:
        sys.modules[executors_module.__name__] = executors_module
        globals()[executors_module._name] = executors_module


def resolve_executor(name):
    if not name:
        return None

    if name == 'LocalExecutor':
        return LocalExecutor()
    elif name == 'SequentialExecutor':
        return SequentialExecutor()
    elif name == 'CeleryExecutor':
        from airflow.executors.celery_executor import CeleryExecutor
        return CeleryExecutor()
    elif name == 'DaskExecutor':
        from airflow.executors.dask_executor import DaskExecutor
        return DaskExecutor()
    elif name == 'MesosExecutor':
        from airflow.contrib.executors.mesos_executor import MesosExecutor
        return MesosExecutor()
    else:
        # Loading plugins
        _integrate_plugins()
        if name in globals():
            return globals()[_EXECUTOR]()
        else:
            raise AirflowException("Executor {0} not supported.".format(_EXECUTOR))

_EXECUTOR = configuration.get('core', 'EXECUTOR')

DEFAULT_EXECUTOR = resolve_executor(_EXECUTOR)

logging.info("Using executor " + _EXECUTOR)
