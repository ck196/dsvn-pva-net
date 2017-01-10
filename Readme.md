# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG PVANET
## CÀI ĐẶT
### Yêu cầu cài đặt cơ bản
- Ubuntu 14.04 hoặc lớn hơn
- Máy tính có GPU >= 2GB cho việc chạy mô hình, GPU >= 4GB cho việc training model.
- CUDA 7.5, cudnn 5 (hoặc phiên bản lớn hớn - nhưng không khuyến khích)

### Các bước
- Tải PVAnet về (đã chỉnh sửa)

```
git clone git@github.com:ck196/dsvn-pva-net.git
cd dsvn-pva-net

```
- Cài đặt OpenCV 3.1.0

```
sudo ./scripts/opencv_3.1.0_install.sh
```
- Cài đặt các phần mềm liên quan cho Caffe

```
sudo ./scripts/caffe_requiremnts_install.sh
cd libjson
sudo python setup.py install
cd ..

```
- Cài đặt PVANET

```
cd pva-faster-rcnn/lib
make
cd ..
cd caffe-faster-rcnn
make -j8 && make pycaffe
cd ..
```

## SỬ DỤNG
- Tải model có sẵn về

```
wget https://www.dropbox.com/s/87zu4y6cvgeu8vs/test.model?dl=0 -O test.model
```
- Chạy thử

```
python pva-faster-rcnnn/tools/rcnn_detector.py
```

- Nếu có model có thể chỉnh sửa *rcnn_detector.py* cho phù hợp

## TRAINING
### Chuẩn bị dữ liệu - Ví dụ với tập dữ liệu PASCAL VOC 2007
- Dowload tập dữ liệu

```
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCdevkit_08-Jun-2007.tar

tar xvf VOCtrainval_06-Nov-2007.tar
tar xvf VOCtest_06-Nov-2007.tar
tar xvf VOCdevkit_08-Jun-2007.tar
```

- Sau khi giải nén cấu trúc thư mục như sau:

```
VOCdevkit/                           # development kit
VOCdevkit/VOCcode/                   # VOC utility code
VOCdevkit/VOC2007                    # image sets, annotations, etc.
# ... and several other directories ...
```

- Tạo liên kết

```
ln -s VOCdevkit VOCdevkit2007
```

### Chú ý khi train với dữ liệu của mình
- Nếu muốn train model với dữ liệu của mình chúng ta có thể copy dữ liệu của mình vào các thư mục sau.
-- Thư mục chứa ảnh:  *VOC2007/JPEGImages*
-- Thư mục chứa file xml: *VOC2007/Annotations*
-- Thư mục chứa các file trainval.txt, test.txt: *ImageSets/Main/*
-- Các file trainval.txt và test.txt chứa tên các file ảnh (bỏ đuôi)

- Chúng ta cần chỉnh sửa file định nghĩa mô hình và file test mô hình cho phù hợp với dữ liệu mới. (Xem phần dưới)
- Công cụ tạo ra file annotations (xml):

```
https://github.com/tzutalin/labelImg
```

### Chỉnh sửa mô hình và cấu hình
- Các file cần chú ý và chỉnh sửa khi training và test mô hình sau khi train xong mô hình.

```
pva-faster-rcnn/models/pvanet/example_train_384/train.prototxt
pva-faster-rcnn/models/pvanet/example_train_384/test.prototxt
pva-faster-rcnn/lib/datasets/pascal_voc.py
```

#### 1. train.prototxt
- Dòng 11, 6318 chỉnh sửa thành số lớp bạn có trong dữ liệu + 1, VOC hiện có 20 lớp + lớp __background__
```
param_str: "'num_classes': 21"
```

- Dòng 6498, tương tự thay bằng số lớp + 1

```
layer {
  name: "cls_score"
  type: "InnerProduct"
  bottom: "fc7"
  top: "cls_score"
  param { lr_mult: 1.0 decay_mult: 1.0 }
  param { lr_mult: 2.0 decay_mult: 0 }
  inner_product_param {
    num_output: 21
    weight_filler { type: "gaussian" std: 0.01 }
    bias_filler { type: "constant" value: 0 }
  }
}

```

- Dòng 1511, numpout_output = (class + 1) * 4

```
layer {
  name: "bbox_pred"
  type: "InnerProduct"
  bottom: "fc7"
  top: "bbox_pred"
  param { lr_mult: 1.0 decay_mult: 1.0 }
  param { lr_mult: 2.0 decay_mult: 0 }
  inner_product_param {
    num_output: 84
    weight_filler { type: "gaussian" std: 0.001 }
    bias_filler { type: "constant" value: 0 }
  }
}
```

#### 2. test.prototxt 
- Chỉnh sửa tương tự với train.txt ở các layer *cls_score* và *bbox_pred*

#### 3. lib/datasets/pascal_voc.py
- Chỉnh sửa tên các lớp cho phù hợp với dữ liệu

```
self._classes = ('__background__', # always index 0
                         'aeroplane', 'bicycle', 'bird', 'boat',
                         'bottle', 'bus', 'car', 'cat', 'chair',
                         'cow', 'diningtable', 'dog', 'horse',
                         'motorbike', 'person', 'pottedplant',
                         'sheep', 'sofa', 'train', 'tvmonitor')
```

### Training
- Tải mô hình Imagenet

```
cd pva-faster-rcnn
./models/pvanet/download_imagenet_model.sh
```

- Training (cần chỉnh sửa đường dẫn cho phù hợp)

```
mkdir output
./train.sh
```

- Các model snapshot sẽ lưu trong output/. Chỉnh sửa thông số trong lib/fast_rcnn/config.py để có các snapshot. Hiện tại các snapshot lưu lại sau 10k vòng lặp.

```
__C.TRAIN.SNAPSHOT_ITERS = 10000
```