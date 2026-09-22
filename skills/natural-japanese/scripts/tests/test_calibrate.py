import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from calibrate import _bin_for_length


def test_calibrate_bin_for_length():
    assert _bin_for_length(500) == "~1000字"
    assert _bin_for_length(1000) == "~2000字"
    assert _bin_for_length(2500) == "~4000字"
    assert _bin_for_length(5000) == "4000字~"
