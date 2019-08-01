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


Test
----

TODO



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
