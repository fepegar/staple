======
STAPLE
======


.. image:: https://img.shields.io/pypi/v/staple.svg
        :target: https://pypi.python.org/pypi/staple

.. image:: https://img.shields.io/travis/fepegar/staple.svg
        :target: https://travis-ci.org/fepegar/staple

.. image:: https://readthedocs.org/projects/staple/badge/?version=latest
        :target: https://staple.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/fepegar/staple/shield.svg
     :target: https://pyup.io/repos/github/fepegar/staple/
     :alt: Updates



Python implementation of the Simultaneous Truth and Performance Level
Estimation (STAPLE) algorithm for generating ground truth volumes from
a set of binary segmentations.

The STAPLE algorithm is described in
`S. Warfield, K. Zou, W. Wells, Validation of image segmentation and
expert quality with an expectation-maximization algorithm in MICCAI 2002:
Fifth International Conference on Medical Image Computing and
Computer-Assisted Intervention, Springer-Verlag, Heidelberg, Germany, 2002,
pp. 298-306 <https://www.ncbi.nlm.nih.gov/pubmed/15250643/>`_.


Installation
------------

::

   $ pip install staple


Usage
-----

::

$ staple seg_1.nii.gz seg_2.nii.gz seg_3.nii.gz result.nii.gz


Caveats
-------

- The `SimpleITK implementation <https://itk.org/SimpleITKDoxygen/html/classitk_1_1simple_1_1STAPLEImageFilter.html>`_
  is about 16 times faster for the
  `test images <https://github.com/fepegar/staple/blob/master/tests/itk_urls.txt>`_.
  The implementation in this repository is mostly for educational purposes.
- Markov random field (MRF) preprocessing is not implemented (nor is it in the
  `ITK version <https://github.com/InsightSoftwareConsortium/ITK/blob/master/Modules/Filtering/ImageCompare/include/itkSTAPLEImageFilter.hxx>`_).
  If you need STAPLE with MRF, check out
  `NiftySeg <https://github.com/KCL-BMEIS/NiftySeg/blob/master/seg-lib/_seg_LabFusion.cpp>`_.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
