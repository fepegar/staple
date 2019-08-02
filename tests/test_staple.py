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
    s = staple.STAPLE(arrays)
    result = s.run()
    np.testing.assert_equal(result, probabilities_small)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'staple.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
