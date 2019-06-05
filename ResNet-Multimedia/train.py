import tensorflow as tf
import os
import tensorflow.contrib.slim.nets as nets
import datetime

NUM_OF_CLASSES = 2

# save_dir = r"./train_image_63.model/"  # 模型保存路径
save_dir = r"/project/jzhuang_03/yiming.dong/train_image_63.model/"
# tfrecordpath = '../dataset/tfrecords'
tfrecordpath = '/project/jzhuang_03/yiming.dong/tfrecords'


def read_and_decode_tfrecord(filename):
    filename_deque = tf.train.string_input_producer(filename)
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_deque)
    features = tf.parse_single_example(serialized_example, features={
        'label': tf.FixedLenFeature([], tf.int64),
        'img_raw': tf.FixedLenFeature([], tf.string)})
    label = tf.cast(features['label'], tf.int32)
    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [224, 224, 3])
    img = tf.cast(img, tf.float32) / 255.0  # 将矩阵归一化0-1之间
    return img, label


batch_size_ = 16
lr = tf.Variable(0.0001, dtype=tf.float32)  # 学习速率
x = tf.placeholder(tf.float32, [None, 224, 224, 3])  # 图片大小为224*224*3
y_ = tf.placeholder(tf.float32, [None])

# construct train list names
train_list = []
for i in range(40):
    train_list.append(os.path.join(tfrecordpath, 'traindata_63.tfrecords-' + str(i).zfill(3)))
img, label = read_and_decode_tfrecord(train_list)

val_list = []
for i in range(5):
    val_list.append(os.path.join(tfrecordpath, 'validationdata_63.tfrecords-' + str(i).zfill(3)))
    img_val, label_val = read_and_decode_tfrecord(val_list)

# Batch处理
img_batch, label_batch = tf.train.batch([img, label], batch_size=batch_size_,
                                        capacity=10000)
one_hot_labels = tf.one_hot(indices=tf.cast(y_, tf.int32), depth=NUM_OF_CLASSES)
pred, end_points = nets.resnet_v2.resnet_v2_101(x, num_classes=NUM_OF_CLASSES, is_training=True)
pred = tf.reshape(pred, shape=[-1, NUM_OF_CLASSES])

img_batch_val, label_batch_val = tf.train.batch([img_val, label_val], batch_size=batch_size_,
                                                capacity=10000)
one_hot_labels_val = tf.one_hot(indices=tf.cast(y_, tf.int32), depth=NUM_OF_CLASSES)
pred_val, end_points_val = nets.resnet_v2.resnet_v2_101(x, num_classes=NUM_OF_CLASSES, reuse=True)
pred_val = tf.reshape(pred_val, shape=[-1, NUM_OF_CLASSES])
# 损失函数与优化器
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=one_hot_labels))
optimizer = tf.train.AdamOptimizer(learning_rate=lr).minimize(loss)

loss_val = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(logits=pred_val, labels=one_hot_labels_val))
# 准确度
a = tf.argmax(pred, 1)
b = tf.argmax(one_hot_labels, 1)
correct_pred = tf.equal(a, b)
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

a_val = tf.argmax(pred_val, 1)
b_val = tf.argmax(one_hot_labels_val, 1)
correct_pred_val = tf.equal(a_val, b_val)
accuracy_val = tf.reduce_mean(tf.cast(correct_pred_val, tf.float32))

saver = tf.train.Saver(max_to_keep=None)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    # 创建一个协调器，管理线程
    coord = tf.train.Coordinator()
    # 启动QueueRunner,此时文件名队列已经进队
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    i = 0
    while True:
        i += 1
        b_image, b_label = sess.run([img_batch, label_batch])
        _, loss_, y_t, y_p, a_, b_ = sess.run([optimizer, loss, one_hot_labels, pred, a, b],
                                              feed_dict={x: b_image, y_: b_label})
        #
        # if i % 2000 == 0:
        #     gpuinfo = os.popen('nvidia-smi').readlines()
        #     with open('/home/jzhuang_03/yiming.dong/gpuinfo.txt', 'a') as f:
        #         for line in gpuinfo:
        #             f.write(line)

        if i % 200 == 0:
            _loss, acc_train = sess.run([loss, accuracy], feed_dict={x: b_image, y_: b_label})
            # _loss_val, acc_val = sess.run([loss_val, accuracy_val],
            #                               feed_dict={x: b_image_val, y_: b_label_val})
            # print('--------------------------------------------------------')
            with open('/home/jzhuang_03/yiming.dong/ans.txt', 'a') as f:
                f.write(datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S') + '  step: {}  train_acc: {}  train_loss: {}\n'.format(
                    i,
                    acc_train,
                    _loss))
            # print('step: {}  train_acc: {}  loss: {}'.format(i, acc_train, _loss))
            # print('--------------------------------------------------------')
        # if i % 5000 == 0:
        if i % 1000 == 0:
            j = 0
            losslist = []
            acclist = []
            while j < ((len(val_list) * 1000) / batch_size_):
                j += 1
                b_image_val, b_label_val = sess.run([img_batch_val, label_batch_val])
                _loss_val, acc_val = sess.run([loss_val, accuracy_val],
                                              feed_dict={x: b_image_val, y_: b_label_val})
                losslist.append(_loss_val)
                acclist.append(acc_val)
            with open('/home/jzhuang_03/yiming.dong/ans.txt', 'a') as f:
                f.write('--------Validation and Save Session---------\n')
                f.write(
                    'step:{}  val_loss:{}   val_acc:{}\n'.format(i, sum(losslist) / len(losslist),
                                                                 sum(acclist) / len(acclist)))
                f.write(str(acclist) + '\n')
            saver.save(sess, save_dir + 'train', global_step=i)
            if i == 40000:
                break
            # elif i == 300000:
            #     saver.save(sess, save_dir, global_step=i)
            # elif i == 100000:
            #     saver.save(sess, save_dir, global_step=i)
            #     break
    coord.request_stop()
    # # 其他所有线程关闭之后，这一函数才能返回
    coord.join(threads)
with open('/home/jzhuang_03/yiming.dong/ans.txt', 'a') as f:
    f.write("-------------Train Success------------")
