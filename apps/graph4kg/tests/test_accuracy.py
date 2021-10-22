# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse
import paddle
import numpy as np
import unittest

from models.score_funcs import TransEScore, RotatEScore
from models.loss_func import LossFunction
from models.ke_model import KGEModel
from dataset.trigraph import TriGraph


class AccuracyTest(unittest.TestCase):
    """Test Model Accuracy
    """

    def test_transe_pos_score(self):
        """test forward of transe
        """
        score_func = TransEScore(gamma=19.9)
        np.random.seed(0)
        h = paddle.to_tensor(np.random.random((1000, 400)))
        t = paddle.to_tensor(np.random.random((1000, 400)))
        r = paddle.to_tensor(np.random.random((1000, 400)))
        pos_score = score_func(h, r, t).sum().numpy()
        trg_pos_score = 5781.9024776
        self.assertAlmostEqual(pos_score, trg_pos_score, None,
                               'pos_score not aligned!', 5e-3)

    def test_transe_neg_score(self):
        """test get_neg_score of transe
        """
        score_func = TransEScore(gamma=19.9)
        np.random.seed(0)
        h = paddle.to_tensor(np.random.random((1000, 400))).unsqueeze(0)
        t = paddle.to_tensor(np.random.random((1000, 400))).unsqueeze(0)
        r = paddle.to_tensor(np.random.random((1000, 400))).unsqueeze(0)
        neg_e = paddle.to_tensor(np.random.random((1000, 400))).unsqueeze(0)
        neg_score = score_func.get_neg_score(h, r, neg_e, False).sum().numpy()
        trg_neg_score = 5760053.6210946
        self.assertAlmostEqual(neg_score, trg_neg_score, None,
                               'neg_score not aligned!', 0.5)

    def test_rotate_pos_score(self):
        """test forward of rotate
        """
        score_func = RotatEScore(gamma=12.0, emb_init=14.0 / 200)
        np.random.seed(0)
        h = paddle.to_tensor(np.random.random((10, 400)))
        t = paddle.to_tensor(np.random.random((10, 400)))
        r = paddle.to_tensor(np.random.random((10, 200)))
        score = score_func(h, r, t).sum().numpy()
        trg_score = -1957.4883
        self.assertAlmostEqual(score, trg_score, None,
                               'pos_score not aligned!', 1e-4)

    def test_rotate_neg_score(self):
        """test get_neg_score of rotate
        """
        score_func = RotatEScore(gamma=12.0, emb_init=14.0 / 200)
        np.random.seed(0)
        h = paddle.to_tensor(np.random.random((10, 400)))
        t = paddle.to_tensor(np.random.random((10, 400)))
        r = paddle.to_tensor(np.random.random((10, 200)))
        h = paddle.reshape(h, [2, 5, 400])
        t = paddle.reshape(t, [2, 5, 400])
        r = paddle.reshape(r, [2, 5, 200])
        score = score_func.get_neg_score(h, r, t, False).sum().numpy()
        trg_score = -9693.6280
        self.assertAlmostEqual(score, trg_score, None,
                               'pos_score not aligned!', 1e-4)

    def test_logsigmoid_loss(self):
        """test logsigmoid
        """
        loss_func = LossFunction(
            name='Logsigmoid',
            pairwise=False,
            margin=1.0,
            neg_adv_spl=True,
            neg_adv_temp=1.0)
        np.random.seed(0)
        pos_score = paddle.to_tensor(np.random.random((1000, 1)))
        neg_score = paddle.to_tensor(np.random.random((1000, 1)))
        loss = loss_func(pos_score, neg_score).numpy()
        trg_loss = 0.7385364
        self.assertAlmostEqual(loss, trg_loss, None,
                               'logsigmoid loss not aligned!', 1e-6)


if __name__ == '__main__':
    unittest.main()
