# No Bug Action







### 操作说明

#### 启动虚拟环境（一定要先做这个）

`source /envs/nb/bin/activate`



#### 启动`nginx`

```systemctl restart nginx```

#### 查看状态

`systemctl status nginx`

#### `nginx`配置文件位置

`/etc/nginx/sites-available/default`





#### 启动后端

`nohup uwsgi --ini uwsgi.ini >/dev/null 2>&1 &`(后台挂起)

`uwsgi --ini uwsgi.ini`

#### 关闭

`ps -ef|grep uwsgi`

`kill -9 xxxxx`

#### `nginx`配置文件位置

`..../backend/uwsgi.ini`



