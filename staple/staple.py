# -*- coding: utf-8 -*-

"""Main module."""

from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import SimpleITK as sitk


class Convergence(Enum):
    itk = 'itk'
    warfield = 'warfield'


class STAPLE:
    def __init__(
            self,
            arrays: List[np.ndarray],
            maximization_first: bool = True,
            convergence_type: Convergence = Convergence.warfield,
            sensitivity_init: float = 0.99999,
            specificity_init: float = 0.99999,
            max_num_iterations: int = 1000,
            verbose: bool = False,
            convergence_threshold: Optional[float] = None,
            ):
        if not arrays:
            raise ValueError('arrays must be a list of NumPy arrays')
        self.arrays = arrays
        self.decisions_matrix = self._get_decisions_matrix(arrays)  # D
        self.maximization_first = maximization_first
        self.convergence_type = convergence_type
        self.num_voxels, self.num_raters = self.decisions_matrix.shape  # N, R
        self.sensitivity_init = sensitivity_init
        self.specificity_init = specificity_init
        self.sensitivity = None  # p
        self.specificity = None  # q
        self.output = None  # W
        self.prior = self._get_prior(self.decisions_matrix)
        self.max_num_iterations = max_num_iterations
        self.verbose = verbose
        if convergence_threshold is None:
            convergence_threshold = 1e-7
        self.convergence_threshold = convergence_threshold
        self._init()

    @staticmethod
    def _get_decisions_matrix(arrays) -> np.ndarray:
        columns = [array.flatten() for array in arrays]
        decisions_matrix = np.column_stack(columns)
        return decisions_matrix

    @staticmethod
    def _get_prior(decisions_matrix) -> float:
        gamma = decisions_matrix.mean()
        return gamma

    @staticmethod
    def _to_column(array):
        return array.reshape(-1, 1)

    @staticmethod
    def _to_row(array):
        return array.reshape(1, -1)

    def _init(self) -> None:
        if self.maximization_first:
            self.output = np.array(self.arrays).mean(axis=0)
            self.output = self._to_column(self.output)
            self.output = self.output.astype(np.float64)
        else:
            shape = (1, self.num_raters)
            self.sensitivity = np.full(shape, self.sensitivity_init)
            self.sensitivity = self.sensitivity.astype(np.float64)
            self.specificity = np.full(shape, self.specificity_init)
            self.specificity = self.specificity.astype(np.float64)
        self.previous_sum = -1
        self.num_iterations = 1

    def _run_expectation(self) -> None:
        p = self.sensitivity
        q = self.specificity
        D = self.decisions_matrix
        N = self.num_voxels
        f_1 = self.prior
        f_0 = 1 - f_1

        # Compute a
        p_matrix = p.repeat(N, axis=0)
        p1_matrix = 1 - p_matrix
        m_1 = np.ma.masked_array(p_matrix, D == 0).prod(axis=1)  # second term
        m_2 = np.ma.masked_array(p1_matrix, D == 1).prod(axis=1)  # third term
        a = f_1 * m_1.data * m_2.data

        # Compute b
        q_matrix = q.repeat(N, axis=0)
        q1_matrix = 1 - q_matrix
        m_1 = np.ma.masked_array(q_matrix, D == 1).prod(axis=1)  # second term
        m_2 = np.ma.masked_array(q1_matrix, D == 0).prod(axis=1)  # third term
        b = f_0 * m_1.data * m_2.data

        # Compute W
        W = a / (a + b)
        W = self._to_column(W)
        self.output = W

    def _run_maximization(self) -> None:
        w_1 = self.output
        w_0 = 1 - w_1
        R = self.num_raters
        D = self.decisions_matrix

        w_1_matrix = w_1.repeat(R, axis=1)
        num = np.ma.masked_array(w_1_matrix, D == 0).sum(axis=0).data
        denom = w_1.sum()
        p = num / denom
        p = self._to_row(p)

        w_0_matrix = w_0.repeat(R, axis=1)
        num = np.ma.masked_array(w_0_matrix, D == 1).sum(axis=0).data
        denom = w_0.sum()
        q = num / denom
        q = self._to_row(q)

        self.sensitivity = p
        self.specificity = q

        if self.verbose:
            print('Sensitivities:', p.ravel())
            print('Specificities:', q.ravel())

    def _run_iteration(self) -> None:
        step_1, step_2 = self._run_expectation, self._run_maximization
        if self.maximization_first:
            step_1, step_2 = step_2, step_1
        step_1()
        step_2()
        self.num_iterations += 1

    def _check_convergence(self) -> bool:
        if self.convergence_type == Convergence.warfield:
            current_sum = self.output.sum()
            diff = abs(current_sum - self.previous_sum)
            if self.verbose:
                print('Sum difference:', diff)
            self.previous_sum = current_sum
            return diff <= self.convergence_threshold
        else:
            raise NotImplementedError

    def run(self) -> Optional[np.ndarray]:
        while True:
            if self.verbose:
                print('Running iteration', self.num_iterations)
            self._run_iteration()
            if self._check_convergence():
                success = True
                break
            elif self.num_iterations == self.max_num_iterations:
                success = False
                break
            if self.verbose:
                print()
        if success:
            if self.verbose:
                print('\n\nConvergence reached after',
                      self.num_iterations, 'iterations')
            one_shape = self.arrays[0].shape
            return self.output.reshape(one_shape)
        else:
            message = 'Maximum number of iterations reached before convergence'
            raise ValueError(message)


def get_images(filepaths: List[Union[str, Path]]) -> List[sitk.Image]:
    images = [sitk.ReadImage(str(path)) for path in filepaths]
    return images
