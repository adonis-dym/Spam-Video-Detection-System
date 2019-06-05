import os
from PIL import Image
import tensorflow as tf
import random
import matplotlib.pyplot as plt

# datasetpath = '../dataset'
# datasetpath = "/project/jzhuang_03/yiming.dong/dataset"
datasetpath='./testset_pic'
# 数据集路径
datadir = datasetpath

# 每个tfrecord存放图片个数
bestnum = 1000

# 第几个图片
num = 0

# 第几个TFRecord文件
recordfilenum = 0

# tfrecord文件保存路径
# file_path = r"../dataset/tfrecords/"
# file_path = "/project/jzhuang_03/yiming.dong/tfrecords"
file_path='./'
# tfrecords格式文件名
tfrecordfilename = ("testset_pic.tfrecords-%.3d" % recordfilenum)
writer = tf.python_io.TFRecordWriter(os.path.join(file_path, tfrecordfilename))
imglist = os.listdir(datadir)
random.shuffle(imglist)
for img_name in imglist:
    label = int(img_name.split('.')[0][-1])
    aid=int(img_name.split('_')[0])
    num = num + 1
    # if num > bestnum:  # 超过1000，写入下一个tfrecord
    #     num = 1
    #     recordfilenum += 1
        # if recordfilenum >= 45:
        #     tfrecordfilename = ("testdata_63.tfrecords-%.3d" % (recordfilenum - 45))
        # elif recordfilenum >= 40:
        #     tfrecordfilename = ("validationdata_63.tfrecords-%.3d" % (recordfilenum - 40))
        # else:
        #     tfrecordfilename = ("traindata_63.tfrecords-%.3d" % recordfilenum)
        # writer = tf.python_io.TFRecordWriter(os.path.join(file_path, tfrecordfilename))
    img_path = os.path.join(datadir, img_name)
    img = Image.open(img_path, 'r')
    img_raw = img.tobytes()  # 将图片转化为二进制格式
    example = tf.train.Example(
        features=tf.train.Features(feature={
            'aid': tf.train.Feature(int64_list=tf.train.Int64List(value=[aid])),
            'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
            'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw])),
        }))
    writer.write(example.SerializeToString())  # 序列化为字符串
writer.close()

# show pictures to confirm tfrecord correctness
'''
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
    # img = tf.cast(img, tf.float32) / 255.0      #将矩阵归一化0-1之间
    return img, label


tfrecordpath = '../dataset/tfrecords'
train_list = ['traindata_63.tfrecords-000','traindata_63.tfrecords-001']
for i in range(len(train_list)):
    train_list[i]=os.path.join(tfrecordpath,train_list[i])
img, label = read_and_decode_tfrecord(train_list)
img_batch, label_batch = tf.train.batch([img, label], num_threads=2, batch_size=2, capacity=1000)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    # 创建一个协调器，管理线程
    coord = tf.train.Coordinator()
    # 启动QueueRunner,此时文件名队列已经进队
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    while True:
        b_image, b_label = sess.run([img_batch, label_batch])
        b_image = Image.fromarray(b_image[0])
        plt.imshow(b_image)
        plt.axis('off')
        plt.show()
    coord.request_stop()
    # 其他所有线程关闭之后，这一函数才能返回
    coord.join(threads)
'''
