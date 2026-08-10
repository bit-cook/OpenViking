# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: AGPL-3.0

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]

IMPORT_CASES = [
    pytest.param(
        "from openviking.session.train.components.progress "
        "import ProgressSummaryColumn; assert ProgressSummaryColumn.__name__ == "
        "'ProgressSummaryColumn'",
        id="session-training-progress",
    ),
    pytest.param(
        "from openviking.storage.queuefs import QueueManager; "
        "from openviking.storage.vikingdb_manager import VikingDBManager; "
        "assert QueueManager.__name__ == 'QueueManager'; "
        "assert VikingDBManager.__name__ == 'VikingDBManager'",
        id="queuefs-and-vikingdb",
    ),
    pytest.param(
        "import openviking.service as service; "
        "expected = {'OpenVikingService', 'ComponentStatus', 'DebugService', "
        "'SystemStatus', 'FSService', 'RelationService', 'PackService', "
        "'SearchService', 'ResourceService', 'SessionService'}; "
        "assert set(service.__all__) == expected; "
        "assert all(getattr(service, name).__name__ == name for name in expected); "
        "from openviking.service import resource_service; "
        "assert resource_service.__name__ == 'openviking.service.resource_service'",
        id="service-public-exports",
    ),
]


@pytest.mark.parametrize("source", IMPORT_CASES)
def test_public_imports_work_in_fresh_process(source: str) -> None:
    result = subprocess.run(
        [sys.executable, "-c", source],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
