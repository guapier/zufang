# coding:utf-8
# from datetime import datetime
# from urllib import request
import json
import random
import time
import requests
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask, request
from flask import render_template, redirect, flash
from flask_apscheduler import APScheduler  # 主要插件
from flask_login import login_user, login_required, LoginManager, current_user, logout_user
from sqlalchemy import and_, or_
from models.Model import db, User, Job, House, HouseSource
from spiders.douban import Douban
from spiders.joke import get_joke
from utils.LogHandler import log


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/house?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = '123456'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def crawl_data_woyaozufang(city, keyword, frequency):
    """
    发送开发者服务微信
    data里面的值，看需求决定参数
    user_id 微信推送id
    info_url 点击微信需要跳转的地址
    当需要传输的数据是json格式的时候使用
    """

    url = "https://woyaozufang.live/v2/houses"

    data = {"city": city, "source": "", "keyword": keyword}

    headers = {
        'accept': "application/json, text/plain, */*",
        'origin': "https://house-map.cn",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/72.0.3626.96 Safari/537.36",
        'dnt': "1",
        'content-type': "application/json;charset=UTF-8",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=json.dumps(data), headers=headers)
    log.info(response.text)

    houses = response.json().get('data')
    log.info('共发现{}个房源'.format(len(houses)))

    for house in houses:
        house = House(title=house.get('title'), pubTime=house.get('pubTime'), displaySource=house.get('displaySource'),
                      location=house.get('location'), onlineURL=house.get('onlineURL'),
                      longitude=house.get('longitude'),
                      latitude=house.get('latitude'), tags=house.get('tags'), price=house.get('price'),
                      detail_id=house.get('detail_id'))
        try:
            db.session.add(house)
            db.session.commit()

        except Exception as e:
            # print(e)
            pass


def crawl_data(city, keyword, frequency):
    douban = Douban()
    hs = HouseSource.query.filter_by(city=city).all()
    group_id = hs[random.randint(0, len(hs))].group
    log.info('当前抓取豆瓣房源的group_id 为：{}'.format(group_id))
    douban.crawl(group_id, keyword, city)


def post_json(url, value):
    try:
        new_value = json.dumps(value).encode(encoding='utf-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
        req = requests.post(url=url, data=new_value, headers=headers)
        # print(req.text)

    except Exception as e:
        raise e  # 抛出这个异常


def send_dev_wx(user_id, info_url, subject, task):
    url = "http://wxmsg.dingliqc.com/send"
    values = {
        "userIds": [user_id],
        "template_id": "4YscLc2uaCnsdrEdUJ9HGAGAkdBcEQM9bUBy0gs69Hw",
        "url": info_url,
        "data": {
            "first": {
                "value": "【" + subject + "】",
                "color": "#d0021b"
            },
            "keyword1": {
                "value": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                "color": "#173177"
            },
            "keyword2": {
                "value": "来自：这里有房",
                "color": "#173177"
            },
            "remark": {
                "value": "房源地址：" + task,
                "color": "#173177"
            }
        }
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
               "Content-Type": "application/json"}
    response = post_json(url, values)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        email_user = User.query.filter_by(email=email).first()

        if user or email_user:
            flash('用户名或者邮箱重复')
            return redirect('/register')
        model = User(email=email, username=username, password=password)
        db.session.add(model)
        db.session.commit()
        flash('注册成功,现在可以进行登录了')
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect('index')
        else:
            flash('错误的用户名或者密码')
            return render_template('login.html')


@login_required
@app.route('/index')
def index():
    try:
        user_id = current_user.id
    except Exception as e:
        user_id = None

    if user_id:
        task_list = Job.query.filter_by(user_id=int(current_user.id)).all()
        return render_template('task_list.html', task_list=task_list)
    else:
        flash('你还未登录，请登录后进行操作')
        return redirect('login')


@login_required
@app.route('/index/add_task', methods=['GET', 'POST'])
def task_add():
    if request.method == 'GET':
        return render_template('task_add.html')
    else:
        try:
            desc = request.form['desc']
            keyword = request.form['keywords']
            frequency = request.form['frequency']
            city = request.form['city']
            wx_user_id = request.form['wx_user_id']
            job_id = str(int(time.time() * 1000))
            status = 1
            job = Job(desc=desc, keywords=keyword, frequency=frequency, city=city, wx_user_id=wx_user_id, status=status,
                      user_id=int(current_user.id), job_id=job_id)
            db.session.add(job)
            db.session.commit()

            # 添加微信推送定时任务
            log.info('微信推送定时任务用户id:{}'.format(str(current_user.id)))
            scheduler.add_job(func=send_dev_wx, id=job_id,
                              args=(
                                  wx_user_id,
                                  'http://zufang.ngrok.xiaomiqiu.cn/index/house?keyword={}&city={}&user_id={}&from=wx'.format(keyword,
                                                                                                           city,str(current_user.id)),
                                  '这里有房为你监控到了合适的房源，请及时查看', city + '(' + keyword + ')'),
                              trigger='cron', hour='8-22', minute='*/{}'.format(int(frequency)),
                              replace_existing=True, coalesce=True)

            # 添加房源数据抓取定时任务
            minute_cron = round(int(frequency) / 3 + 1)
            scheduler.add_job(func=crawl_data, id=job_id + '_spider',
                              args=(city, keyword, frequency
                                    ),
                              trigger='cron', hour='6-23', minute='*/{}'.format(minute_cron),
                              replace_existing=True, coalesce=True)
            flash('任务提交成功')
            return redirect('/index')
        except Exception as e:
            log.error(e)
            db.session.rollback()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已安全登出')
    return redirect('login')


@app.route('/index/house', methods=['GET', 'POST'])
def house_list():
    city = request.args.get('city', '深圳')
    keyword = request.args.get('keyword', '坪洲,西乡,宝体,桂庙')
    user_id = request.args.get('user_id')
    # houses = House.query.filter_by(is_sended=0).order_by('pubTime').limit(10).all()
    words = ['%' + k + '%' for k in keyword.split(',')]
    log.info('关键词：{}'.format(words))
    rule = or_(*[House.title.like(w) for w in words])
    houses = House.query.filter(rule).order_by('pubTime').all()
    unique_houses = []
    for house in houses:
        if user_id in house.user_ids.split(','):
            continue
        else:
            house.user_ids += user_id+','
            db.session.commit()
            unique_houses.append(house)
            if len(unique_houses) >= 10:
                break
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    houses = unique_houses
    if houses:
        # 推送房源
        return render_template('info.html', houses=houses, city=city, keyword=keyword, current_time=current_time)

    else:
        # 推送段子
        response = get_joke()
        result = json.loads(response.text)
        jokes = result.get('data').get('list')
        return render_template('info_joke.html', jokes=jokes, city=city, keyword=keyword, current_time=current_time)


@app.route('/index/task_stop')
def task_stop():
    job_id = request.args.get('job_id')
    scheduler.pause_job(job_id)
    scheduler.pause_job(job_id + '_spider')

    job = Job.query.filter_by(job_id=job_id).first()

    job.status = 0
    db.session.commit()
    flash('任务暂停成功')
    return redirect('/index')


@app.route('/index/task_resume')
def task_resume():
    job_id = request.args.get('job_id')
    scheduler.resume_job(job_id)
    scheduler.resume_job(job_id + '_spider')

    job = Job.query.filter_by(job_id=job_id).first()

    job.status = 1
    db.session.commit()
    flash('任务启动成功')
    return redirect('/index')


@app.route('/')
def idx_page():
    return render_template('index.html')


def jobfromparm(**jobargs):
    id = jobargs['id']
    func = jobargs['func']
    args = eval(jobargs['args'])
    trigger = jobargs['trigger']
    seconds = jobargs['seconds']
    print('add job: ', id)
    job = scheduler.add_job(func=func, id=id, args=args, trigger=trigger, seconds=seconds, replace_existing=True)
    return 'sucess'


class Config(object):
    JOBS = []
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='mysql+pymysql://root:root@localhost:3306/house?charset=utf8mb4')
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


if __name__ == '__main__':
    db.init_app(app)
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host='0.0.0.0', port=3000, debug=False)
