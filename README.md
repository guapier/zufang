<h1>这里有房</h1>


## About

听说最近你想租房，但是却没时间去相应网站查看，我想我做的这个东东可以满足你的需求，功能比较简单，通过web方式添加关键字定时任务，然后爬虫定时爬取关键字房源，然后进行微信推送，你只需要在微信里面就可以查看你想要了解的房源信息

--- 
## skills
主要用到了flask，sqlalchemy，apscheduler这些技术，其中flask提供web页面和api，sqlalchey主要负责处理数据库方面问题，apscheduler主要处理定时任务，以及定时任务持久化

--- 
## run
1.安装包
```bash
pip install flask
pip install flask-login
pip install flask-sqlalchey
pip install flask-apscheduler
```
2.运行
```python
python group-search-city.py
python app_schedule.py
```
3.说明
房源数据主要来源于豆瓣，后期可能会添加其他源，group-search-city.py主要用来爬虫都放城市所对应的group，python app_schedule.py用来启动应用，每次最多推送10条，数据通过title去重，关键字用英文逗号隔开，不可以使用中文，代码没有做太多的异常处理，风格也还有待完善，没有用到flask中的蓝图，后期会进行优化
4.感谢
灵感来自[tomxin7](http://house.jiandan.live/)
ui也是参考的他的UI，感谢，核心逻辑是自己实现的

![task_list.png](https://i.loli.net/2019/03/13/5c88be4a2c3e5.png)
![task.png](https://i.loli.net/2019/03/13/5c88be4915dde.png)
![detail.jpg](https://i.loli.net/2019/03/13/5c88c29188233.jpg)
![list.jpg](https://i.loli.net/2019/03/13/5c88c2c73cc02.jpg)
