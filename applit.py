from flask import Flask
import json
app = Flask(__name__)

def seconds_to_dhms(seconds):
    def _days(day):
        return "{}天".format(day)
    def _hours(hour):
        return "{}时".format(hour)
    def _minutes(minute):
        return "{}分".format(minute)
    def _seconds(second):
        return "{}秒".format(second)
    days = seconds // (3600 * 24)
    hours = (seconds // 3600) % 24
    minutes = (seconds // 60) % 60
    seconds = seconds % 60
    if days > 0 :
        return _days(days)+_hours(hours)+_minutes(minutes)+_seconds(seconds)
    if hours > 0 :
        return _hours(hours)+_minutes(minutes)+_seconds(seconds)
    if minutes > 0 :
        return _minutes(minutes)+_seconds(seconds)
    return _seconds(seconds)

def gen_bot_str(bot):
    with open((bot.get('symbol') + '.json'), 'r') as f:
        info = json.load(f)
    if bot.get('type') == 'grid':
        outstr = '分姬类型: 网格 '
        outstr += '交易对: {}<br>'.format(info['symbol'])
        outstr += '运行时间: {}<br>'.format(seconds_to_dhms(info['run_time']))
        outstr += '套利次数: {}<br>'.format(info['txn'])
        outstr += '累计收益: {}<br><br>'.format(round(info['earned'], 4))
    elif bot.get('type') == 'balancer':
        outstr = '分姬类型: 自动平衡 '.format()
        outstr += '交易对: {}<br>'.format(info['symbol'])
        outstr += '运行时间: {}<br>'.format(seconds_to_dhms(info['run_time']))
        outstr += '平衡次数: 多: {}'.format(info['buy_cnt'])
        outstr += ' 空: {}<br><br>'.format(info['sell_cnt'])

    return outstr


@app.route("/bot")
def status():
    bots = [{
             'type':'grid',
             'symbol':'BNBBUSD'
            },
            {
             'type':'grid',
             'symbol':'AVAXBUSD'
            }]
    '''bots = [
        {
            'type': 'balancer',
            'asset': 'AVAX',
            'symbol': 'AVAXBUSD'
        }]'''
    with open('BotManager.json', 'r') as f0:
        info0 = json.load(f0)
    #outstr = '<link rel = "shortcut icon" href = "#" / >'
    if info0['status'] == 'error':
        outstr = '呜呜哇！狗修金大人！！<br>云交易姬倒惹！！（哭腔）<br>'
        outstr += '<meta charset="UTF-8"><title>御鸦鸦的云交易姬</title>'
        outstr += '<img src="https://ubi-img-bed.oss-cn-shanghai.aliyuncs.com/bot_app_err.png" height="75" width="75"/><br>'
        outstr += '发生时间: {}<br>'.format(info0['time'])
        outstr += '错误原因: {}<br>'.format(info0['error'])
        outstr += '请检查运行日志！<br>'
        return outstr
    outstr = '给狗修金大人请安~<br>云交易姬正常工作中唷！！<br>'
    outstr += '<meta charset="UTF-8"><title>御鸦鸦的云交易姬</title>'
    outstr += '<img src="https://ubi-img-bed.oss-cn-shanghai.aliyuncs.com/bot_app_running.png" height="75" width="75"/><br>'
    outstr += '数据更新时间: {}<br>'.format(info0['time'])
    outstr += '当前分姬数: {}<br><br>'.format(len(bots))
    for bot in bots:
        outstr += gen_bot_str(bot)

    return outstr


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
