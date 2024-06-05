# No Bug Action

### 操作说明

```
#### 前端依赖

请先到vue官网安装vue的开发环境

npm i

#### 重新部署前端

sudo npm i

sudo npm run build


#### 启动虚拟环境（如果包没有安装在虚拟环境可以不启动）

source /envs/nb/bin/activate

#### 后端依赖

python版本3.10.14

pip install -r requirements.txt
pip install uswgi （本地运行不需要）

在fontend/src/main.js更换地址为
 url: "http://124.70.208.148"
 self_url: "http://124.70.208.148"


### 数据库
source  [project_root]/backend/database/trianglechess.sql

或者

cd [project_root]/backend/database
mysql -uroot -p -D trianglechess --default-character-set=utf8 < trianglechess.sql

如果编码有问题
iconv -f UTF-16 -t UTF-8 trianglechess.sql > trianglechess_utf8.sql


## 本地运行下面可以不看

#### 启动`nginx`

systemctl restart nginx

#### 查看状态

systemctl status nginx

#### `nginx`配置文件位置

/etc/nginx/sites-available/default

配置方法见/frontend/nginx.cfg



#### 启动后端uwsgi

nohup uwsgi --ini uwsgi.ini >/dev/null 2>&1 &    (后台挂起)

uwsgi --ini uwsgi.ini

#### 关闭

查看后台进程
ps -ef|grep uwsgi

kill -9 xxxxx

#### `nginx`配置文件位置
..../backend/uwsgi.ini





```

