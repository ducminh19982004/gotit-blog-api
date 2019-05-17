# gotit-blog-api
Blog GotIt Api

# Hướng dẫn cài đặt 
## I. Server: ```CentOS 7```, IP example: ```10.0.0.1```
## II. Môi trường: ```Docker```
### 1. Cài Docker
#### Xem hướng dẫn tại ```https://docs.docker.com/install/linux/docker-ce/centos/```
### 2. Cài Docker Compose:
#### Xem hướng dẫn tại ```https://docs.docker.com/compose/install/```
## III. Cài đặt theo các bước sau
- B1: Tạo thư mục 
```
mkdir -p /opt/docker/gotit-blog-api/code/v1
```
- B2: Copy các file ```Dockerfile```, ```env.list```, ```requirements.txt``` của project vào thư mục ```/opt/docker/gotit-blog-api```
- B3: Copy thư mục thư mục ```api```, file ```logging.conf```, file ```config.py``` của project vào thư mục ```/opt/docker/gotit-blog-api/code/v1```
- B4: Chạy lệnh 
```
cd /opt/docker/gotit-blog-api/
```
- B5: Chạy lệnh
```
docker build -t gotit-blog-api:v1 .
```
- B6: Tạo các thư mục 
```
mkdir -p /opt/docker/mysql-master
mkdir -p /opt/data/master1/data
mkdir -p /opt/data/master1/dumps
```
- B7: Copy toàn bộ file, thư mục trong thư mục ```mysql-master``` của project vào thư mục ```/opt/docker/mysql-master```
## IV. Chạy
- B1: Chạy mysql
```
cd /opt/docker/mysql-master
docker-compose up -d
```
- B2: Import dữ liệu vào database (pass root xem trong file ```docker-compose.yml```)
```
docker exec database mysql -uroot -p  < gotit-blog.sql.sql
```
- B3: Sửa lại cấu hình kết nối db
```
cd /opt/docker/gotit-blog-api
vim env.list
```
- B4: Chạy api
```
docker run -d -p 6789:6789 -v /opt/docker/gotit-blog-api/code/v1:/usr/src/app -e "TZ=Asia/Ho_Chi_Minh" --env-file env.list --name gotit-blog-api gotit-blog-api:v1
```
- B5: Truy cập vào địa chỉ ```http://10.0.0.1:6789``` để xem mô tả các api
