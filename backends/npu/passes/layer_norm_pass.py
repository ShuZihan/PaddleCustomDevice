# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
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


from __future__ import print_function, division
import paddle


@paddle.incubate.passes.ir.RegisterPass
def generate_layer_norm():
    def pattern(x, scale, bias):
        return paddle.incubate.passes.ir.PassDesc.OP.layer_norm(
            X=x, Scale=scale, Bias=bias
        ).Output("Y")

    def replace(x, weight, bias):
        layer_norm = paddle.incubate.passes.ir.PassDesc.OP.custom_layer_norm(
            X=x, Scale=weight, Bias=bias
        )
        layer_norm.Attr("begin_norm_axis").MappedPattern(
            op="layer_norm", name="begin_norm_axis"
        )
        layer_norm.Attr("epsilon").MappedPattern(op="layer_norm", name="epsilon")
        return layer_norm

    return pattern, replace