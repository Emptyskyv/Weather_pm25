"""树莓派PM2.5显示文件"""

from sakshat import SAKSHAT
import time
import requests
import json

weather_url = "https://free-api.heweather.net/s6/air/now?location=CN101200101&key=434e281cb7da4b7588f0aee8fe476fd0"
SAKS = SAKSHAT()


def get_weather():
    """获得和风天气API接口数据"""

    req = requests.get(weather_url)
    contents = json.loads(req.text)

    if contents:
        pm2_5 = contents['HeWeather6'][0]['air_now_city']['pm25']
        aqi_ = contents['HeWeather6'][0]['air_now_city']['aqi']
        # print(pm25)
        # print(aqi)
        weather = [pm2_5, aqi_]
        return weather

    else:
        return -1


if __name__ == "__main__":
    while True:
        Weather = get_weather()
        pm25 = Weather[0]
        aqi = Weather[1]

        if pm25 == -1:
            time.sleep(30)
            continue

        # 严重污染，红灯亮蜂鸣器Beep
        if pm25 >= 250:
            SAKS.ledrow.off()
            SAKS.ledrow.items[7].on()
            SAKS.buzzer.beepAction(0.05,0.05,3)
        # 重度污染，红灯亮
        if pm25 < 250:
            SAKS.ledrow.off()
            SAKS.ledrow.items[7].on()
        # 中度污染，红灯亮
        if pm25 < 150:
            SAKS.ledrow.off()
            SAKS.ledrow.items[7].on()
        # 轻度污染，黄灯亮
        if pm25 < 115:
            SAKS.ledrow.off()
            SAKS.ledrow.items[6].on()
        # 良，1绿灯亮
        if pm25 < 75:
            SAKS.ledrow.off()
            SAKS.ledrow.items[4].on()
        # 优，2绿灯亮
        if pm25 < 35:
            SAKS.ledrow.off()
            SAKS.ledrow.items[4].on()
            SAKS.ledrow.items[5].on()

        # print (("%4d" % pm25).replace(' ','#'))
        # 数码管显示aqi-空气质量指数数值
        SAKS.digital_display.show(("%4d" % aqi).replace(' ','#'))
        time.sleep(1800)
    input("Enter any keys to exit...")

