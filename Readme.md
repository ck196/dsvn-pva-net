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


## TRAINING