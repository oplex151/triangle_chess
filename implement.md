# No Bug Action-Implement Guide

## 第一次启动

### １.　安装nginx

```shell
建议在开始安装之前配置好清华源。
参考：https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu
```

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt install -y curl gnupg2 ca-certificates lsb-release
sudo apt-get install nginx

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

### 2. 安装python和uWSGI

如果你喜欢，可以使用虚拟环境。

```shell
sudo apt-get install python=3.10.14
pip install ./backend/requirements.txt -r


# 创建虚拟环境
python -m venv /envs/虚拟环境名
source /envs/虚拟环境名/bin/activate

# 以后启动后端先要

source /envs/虚拟环境名/bin/activate
```

### 3.    安装npm

```shell
sudo apt-get install nodejs npm

npm -v
nodejs -v
```
建议的版本为npm>10.7,nodejs>20.13

如果版本明显异常，你应该重新配置Ubuntu软件源。

### 4.    安装依赖，生成项目

```shell
cd backend
sudo npm i
sudo npm run build  # 每次修改前端代码后都需要运行此命令
cd ..
```

### 5.    配置Nginx

在/etc/nginx/sites-available/default 下

```nginx

server {
	listen 80 default_server;
	listen [::]:80 default_server;


	server_name _;


    location /api {
        include uwsgi_params;
        uwsgi_pass  localhost:8888;
        proxy_set_header   	Host             $host;
        proxy_set_header   	X-Real-IP        $remote_addr;						
        proxy_set_header   	X-Forwarded-For  $proxy_add_x_forwarded_for;
    }
    location /socket.io/ {
        include uwsgi_params;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        uwsgi_pass localhost:8888;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }   
    
    location /static {
        root /var/www/html/triangle_chess/backend;
    }

	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
        # uwsgi_pass 127.0.0.1:8888;
		# try_files $uri $uri/ =404;


        root /var/www/html/triangle_chess/frontend/dist;
	    index index.html index.htm index.nginx-debian.html;
        try_files $uri $uri/ @router;
	}

    location @router {
        rewrite ^.*$ /index.html last;
    }

}

```

### 6.    下载并启动mysql

本部分命令中，password请替换为自己的mysql密码。
建议的mysql版本为8.0-8.3.

```shell
sudo apt install mysql-server
sudo systemctl start mysql.service
sudo systemctl enable mysql.service
sudo mysql
```

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```

请将下一行粘贴到/etc/profile:(your_password需要替换)

```shell
export MYSQL_PASSWORD = your_password
```

### 7.    配置数据库

project_root请替换为项目地址。

```sql
mysql -uroot -p
//登录
source  [project_root]/backend/database/trianglechess.sql
{//或者进入/bakckedn/database/目录，执行
    mysql -uroot -p -D trianglechess --default-character-set=utf8 < trianglechess.sql
}
//如果编码有问题，执行下面的语句
iconv -f UTF-16 -t UTF-8 trianglechess.sql > trianglechess_utf8.sql
```

### 8.    配置redis

```shell
# 安装redis
sudo apt install lsb-release curl gpg

curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update

sudo apt-get install redis

# pip install redis

# pip install aliyunsdkcore

# pip install aliyun-python-sdk-core-v3

# 启动redis

systemctl start redis-server

# 重启redis

service redis-server restart

# 查看redis状态

service redis-server status
```


**至此，第一次启动配置完成，接下来请按照“启动”启动。**

## 启动

```shell
cd frontend
systemctl restart nginx  #重启nginx
systemctl status nginx  #查看nginx

cd backend
nohup uwsgi --ini ./backend/uwsgi.ini >/dev/null 2>&1 &  #挂起后端
{
    #也可以 
    uwsgi --ini uwsgi.ini >/dev/null 2>&1 & #直接运行
}
```

## 关闭

```shell
ps -ef|grep uwsgi
kill -9 xxxxx
```