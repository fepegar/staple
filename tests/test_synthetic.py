#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `staple` package."""

import pytest

from click.testing import CliRunner

from staple import staple
from staple import cli


@pytest.fixture
def probabilities_small():
    import numpy as np
    result = 0, 0, 0, 0, 1, 1, 1, 1
    return np.array(result, dtype=np.float64)


def test_staple_small(probabilities_small):
    import numpy as np
    segmentations = (
        (0, 0, 0, 0, 0, 1, 1, 0),
        (0, 0, 0, 0, 1, 1, 1, 1),
        (1, 1, 1, 0, 1, 1, 1, 1),
        (0, 0, 0, 0, 1, 1, 1, 0),
        (0, 1, 0, 0, 0, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
    )
    arrays = [np.array(s, dtype=np.float64) for s in segmentations]
    s = staple.STAPLE(arrays, convergence_threshold=0)
    result = s.run()
    np.testing.assert_almost_equal(result, probabilities_small)
