import tensorflow as tf
import tensorflow.contrib.slim.nets as nets
import os
import sys
import pandas as pd

NUM_OF_CLASSES = 2
batch_size_ = 20  # 必须能被测试集样本数整除


def read_and_decode_tfrecord(filename):
    filename_deque = tf.train.string_input_producer(filename)
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_deque)
    features = tf.parse_single_example(serialized_example, features={
        'aid': tf.FixedLenFeature([], tf.int64),
        'label': tf.FixedLenFeature([], tf.int64),
        'img_raw': tf.FixedLenFeature([], tf.string)})
    aid = tf.cast(features['aid'], tf.int32)
    label = tf.cast(features['label'], tf.int32)
    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [224, 224, 3])
    img = tf.cast(img, tf.float32) / 255.0  # 将矩阵归一化0-1之间
    return aid, img, label


model_dir = r'./train_image_63.model/train-4000'  # 模型地址
# model_dir = r'/project/jzhuang_03/yiming.dong/train_image_63.model/train-' + str(sys.argv[1]).split('-')[1]


tfrecordpath = './tfrecords'
# tfrecordpath = '/project/jzhuang_03/yiming.dong/tfrecords'

# construct test list names
test_list = []
# for i in range(5):
for i in range(1):
    #     test_list.append(os.path.join(tfrecordpath, 'testdata_63.tfrecords-' + str(i).zfill(3)))
    test_list.append(os.path.join(tfrecordpath, 'testset_pic.tfrecords-000'))
x = tf.placeholder(tf.float32, [None, 224, 224, 3])
y_ = tf.placeholder(tf.float32, [None])

aid, img, label = read_and_decode_tfrecord(test_list)
# img, label = read_and_decode_tfrecord(test_list)
aid_batch, img_batch, label_batch = tf.train.batch([aid, img, label], batch_size=batch_size_,
                                                   capacity=10000)

one_hot_labels = tf.one_hot(indices=tf.cast(y_, tf.int32), depth=NUM_OF_CLASSES)
# pred, end_points = nets.resnet_v2.resnet_v2_50(x, num_classes=NUM_OF_CLASSES, is_training=True)
pred, end_points = nets.resnet_v2.resnet_v2_101(x, num_classes=NUM_OF_CLASSES, is_training=True)
pred = tf.reshape(pred, shape=[-1, 2])

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=one_hot_labels))

a = tf.argmax(pred, 1)
b = tf.argmax(one_hot_labels, 1)
correct_pred = tf.equal(a, b)
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# for model_dir in model_dir_list:
loss_list = []
acc_list = []
a_list = []
b_list = []
aid_list = []

saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, model_dir)
    coord = tf.train.Coordinator()
    # 启动QueueRunner,此时文件名队列已经进队
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    i = 0
    # if (len(test_list) * 1000) % batch_size_ != 0:
    #     raise ValueError("Batch size must be divisible by test set size")
    while i < ((len(test_list) * 1000) / batch_size_):
        # while i < 5:
        i += 1
        b_aid, b_image, b_label = sess.run([aid_batch, img_batch, label_batch])
        loss_, test_acc, a_, b_ = sess.run([loss, accuracy, a, b],
                                           feed_dict={x: b_image, y_: b_label})
        aid_list += list(b_aid)
        a_list += list(a_)
        b_list += list(b_)
        loss_list.append(loss_)
        acc_list.append(test_acc)
    coord.request_stop()
    # 其他所有线程关闭之后，这一函数才能返回
    coord.join(threads)

    # col1 = pd.Series(aid_list)
    # col2 = pd.Series(a_list)
    # df = pd.DataFrame()
    # df.insert(0, 'aid', col1)
    # df.insert(1, 'pred_label', col2)
    # df.to_csv('./pred_result.csv',index=None)

    tp = tn = fp = fn = 0
    for x in zip(a_list, b_list):
        if x[0] == 1 and x[1] == 1:
            tp += 1
        elif x[0] == 0 and x[1] == 1:
            fn += 1
        elif x[0] == 1 and x[1] == 0:
            fp += 1
        elif x[0] == 0 and x[1] == 0:
            tn += 1
    #
    # with open('/home/jzhuang_03/yiming.dong/test result.txt', 'a') as f:
    with open('test_result.txt', 'a') as f:
        f.write(
            model_dir.split('-')[1] + ',' + str(
                round((tn + tp) / (fn + tn + tp + fp), 4)) + ',' + str(
                round(tp / (tp + fp), 4)) + ',' + str(round(tp / (tp + fn), 4)) + '\n')
