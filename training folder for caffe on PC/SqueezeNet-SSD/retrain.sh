#!/bin/bash

# 说明：此脚本需在train.sh脚本之前执行

# 使用方法：这个脚本会重命名图层，若要用snapshot中的caffmodel进行微调，并且检测类别数有变化（类别数无变化无需重命名）
# 就必须保证这几层的name与之前训练时.prototxt文件中的name不一样！

# 替换gen_model.sh生成的三个.prototxt文件中的几个卷积层的名称
# 在之前生成的caffemodel中存在一些层，但是使用这些model时这些层是不可用的，他们的shape与现在要训练的模型不符
# 重命名图层时，Caffe不会尝试复制该图层的权重，并且可以随机初始化权重，执行此脚本的目的就是更改这几个图层的name以忽略这几个层
# 最终解决“Cannot copy param 0 weights from layer 'conv11_mbox_conf_new'; shape mismatch.  Source param shape is
# 15 512 1 1 (7680); target param shape is 18 512 1 1 (9216).”问题。
# 参考：https://stackoverflow.com/questions/39811936/using-bvlc-googlenet-as-pretrained-model-in-digits-errors/39837047#39837047
# 指令模板：sed -i "s/oldString/newString/g"  `grep oldString -rl /path`

suffix_old=""
suffix_new="_retrain"
path='./example'
sed -i "s/\<fire5_mbox_conf$suffix_old\>/fire5_mbox_conf$suffix_new/g"  `grep fire5_mbox_conf$suffix_old -rl $path`
sed -i "s/\<fire9_mbox_conf$suffix_old\>/fire9_mbox_conf$suffix_new/g"  `grep fire9_mbox_conf$suffix_old -rl $path`
sed -i "s/\<fire10_mbox_conf$suffix_old\>/fire10_mbox_conf$suffix_new/g"  `grep fire10_mbox_conf$suffix_old -rl $path`
sed -i "s/\<fire11_mbox_conf$suffix_old\>/fire11_mbox_conf$suffix_new/g"  `grep fire11_mbox_conf$suffix_old -rl $path`
sed -i "s/\<conv12_2_mbox_conf$suffix_old\>/conv12_2_mbox_conf$suffix_new/g"  `grep conv12_2_mbox_conf$suffix_old -rl $path`
sed -i "s/\<conv13_2_mbox_conf$suffix_old\>/conv13_2_mbox_conf$suffix_new/g"  `grep conv13_2_mbox_conf$suffix_old -rl $path`
