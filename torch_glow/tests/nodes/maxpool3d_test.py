from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import torch
import torch.nn.functional as F
from tests import utils


class SimpleMaxPool3dTest(torch.nn.Module):
    def __init__(self, kernel_size, padding=0, ceil_mode=False):
        super(SimpleMaxPool3dTest, self).__init__()
        self.kernel_size = kernel_size
        self.padding = padding
        self.ceil_mode = ceil_mode

    def forward(self, inputs):
        return F.max_pool3d(
            inputs,
            kernel_size=self.kernel_size,
            padding=self.padding,
            ceil_mode=self.ceil_mode,
        )


class TestMaxpool3d(unittest.TestCase):
    def test_max_pool3d_basic(self):
        """Basic test of the PyTorch max_pool3d Node on Glow."""

        utils.compare_tracing_methods(
            SimpleMaxPool3dTest(3),
            torch.randn(1, 4, 5, 5, 5),
            fusible_ops={"aten::max_pool3d"},
        )

    def test_max_pool3d_padding(self):
        """Stronger test of the PyTorch max_pool3d Node with assymetric padding on Glow."""

        utils.compare_tracing_methods(
            SimpleMaxPool3dTest(7, padding=(1, 2, 3)),
            torch.randn(2, 3, 16, 16, 16),
            fusible_ops={"aten::max_pool3d"},
        )

    def test_max_pool3d_with_args(self):
        """Test of the PyTorch max_pool3d Node with arguments on Glow."""

        utils.compare_tracing_methods(
            SimpleMaxPool3dTest(7, 3),
            torch.randn(1, 4, 10, 10, 10),
            fusible_ops={"aten::max_pool3d"},
        )

    def test_max_pool3d_ceil_mode(self):
        """Test of the PyTorch max_pool3d Node with ceil_mode on Glow."""

        utils.compare_tracing_methods(
            SimpleMaxPool3dTest(7, 1, ceil_mode=True),
            torch.randn(1, 4, 16, 16, 16),
            fusible_ops={"aten::max_pool3d"},
        )

    def test_max_pool3d_ceil_mode_strong_1(self):
        """Stronger test of the PyTorch max_pool3d Node with ceil_mode on Glow."""

        utils.compare_tracing_methods(
            SimpleMaxPool3dTest(5, 1, ceil_mode=True),
            torch.randn(1, 5, 33, 33, 33),
            fusible_ops={"aten::max_pool3d"},
        )

    def test_max_pool3d_ceil_mode_strong_2(self):
        """Stronger test of the PyTorch max_pool3d Node with ceil_mode on Glow."""

        utils.compare_tracing_methods(
            SimpleMaxPool3dTest(8, 2, ceil_mode=True),
            torch.randn(1, 3, 41, 41, 41),
            fusible_ops={"aten::max_pool3d"},
        )
