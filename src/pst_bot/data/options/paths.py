from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	...

# WARNING!
WORKDIR: Path = Path(__file__).parent.parent.parent
