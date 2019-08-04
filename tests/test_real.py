#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `staple` package."""

import pytest

from click.testing import CliRunner

from staple import staple
from staple import cli


def download_images(force_download=False):
    """
    From https://github.com/InsightSoftwareConsortium/SimpleITK-Notebooks/blob/master/Python/34_Segmentation_Evaluation.ipynb
    """
    import tempfile
    import urllib.request
    from pathlib import Path
    this_dir = Path(__file__).parent
    urls_path = this_dir / 'itk_urls.txt'
    with open(str(urls_path)) as f:
        urls = f.readlines()
    tempdir = Path(tempfile.gettempdir())
    filepaths = []
    for i, url in enumerate(urls):
        filepath = tempdir / 'radiologist_{}.mha'.format(i)
        if not filepath.is_file() or force_download:
            urllib.request.urlretrieve(url, str(filepath))
        filepaths.append(filepath)
    return filepaths


def get_real_arrays():
    """
    From https://github.com/InsightSoftwareConsortium/SimpleITK-Notebooks/blob/master/Python/34_Segmentation_Evaluation.ipynb
    """
    from pathlib import Path
    import SimpleITK as sitk
    arrays = []
    filepaths = download_images()
    for filepath in filepaths:
        image = sitk.ReadImage(str(filepath), sitk.sitkUInt8)
        array = sitk.GetArrayFromImage(image)
        arrays.append(array)
    return arrays


@pytest.fixture
def probabilities_real():
    import SimpleITK as sitk
    arrays = get_real_arrays()
    images = [sitk.GetImageFromArray(array) for array in arrays]
    staple_result = sitk.STAPLE(images)
    result = sitk.GetArrayFromImage(staple_result)
    return result


def test_staple_real(probabilities_real):
    import numpy as np
    arrays = get_real_arrays()
    s = staple.STAPLE(arrays, convergence_threshold=0)
    result = s.run()
    np.testing.assert_almost_equal(result, probabilities_real)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 2

    runner = CliRunner()
    filepaths = [str(path) for path in download_images()]
    import tempfile
    from pathlib import Path
    tempdir = Path(tempfile.gettempdir())
    out_path = str(tempdir / 'test_result.nii.gz')
    args = [*filepaths, out_path, '--convergence-threshold', 1]
    result = runner.invoke(cli.main, args)
    assert result.exit_code == 0
    assert 'Sensitivities' in result.output

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
