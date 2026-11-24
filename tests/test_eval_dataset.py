# -*- coding: utf-8 -*-
import unittest

from arbiter.eval.dataset import make_dataset


class TestDataset(unittest.TestCase):
    def test_size(self):
        ds = make_dataset()
        self.assertEqual(len(ds), 8 * 4 + 8)  # 8 intents * 4 + 8 noise

    def test_labels_consistent(self):
        ds = make_dataset()
        ds2 = make_dataset()
        self.assertEqual([l for _, l in ds], [l for _, l in ds2])


if __name__ == "__main__":
    unittest.main()
