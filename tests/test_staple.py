#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `staple` package."""

import pytest

from click.testing import CliRunner

from staple import staple
from staple import cli


def get_real_arrays(force_download=False):
    """
    From https://github.com/InsightSoftwareConsortium/SimpleITK-Notebooks/blob/master/Python/34_Segmentation_Evaluation.ipynb
    """
    import tempfile
    import urllib.request
    from pathlib import Path
    import SimpleITK as sitk
    this_dir = Path(__file__).parent
    urls_path = this_dir / 'itk_urls.txt'
    with open(urls_path) as f:
        urls = f.readlines()
    tempdir = Path(tempfile.gettempdir())
    arrays = []
    for i, url in enumerate(urls):
        filepath = tempdir / 'radiologist_{}.mha'.format(i)
        if not filepath.is_file() or force_download:
            urllib.request.urlretrieve(url, filepath)
        image = sitk.ReadImage(str(filepath), sitk.sitkUInt8)
        array = sitk.GetArrayFromImage(image)
        arrays.append(array)
    return arrays


@pytest.fixture
def probabilities_small():
    import numpy as np
    result = 0, 0, 0, 0, 1, 1, 1, 1
    return np.array(result, dtype=np.float64)


@pytest.fixture
def probabilities_real():
    import SimpleITK as sitk
    arrays = get_real_arrays()
    images = [sitk.GetImageFromArray(array) for array in arrays]
    staple_result = sitk.STAPLE(images)
    result = sitk.GetArrayFromImage(staple_result)
    return result


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


def test_staple_real(probabilities_real):
    import numpy as np
    arrays = get_real_arrays()
    s = staple.STAPLE(arrays)
    result = s.run()
    np.testing.assert_almost_equal(result, probabilities_real)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'staple.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
