import gc
import json
import logging
import re
import sys
import config

from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

prefec = ['岩手', '北海道', '青森', '宮城', '秋田', '山形', '福島', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川', '新潟', '富山', '石川', '福井',
          '山梨', '長野', '岐阜', '静岡', '愛知', '三重', '滋賀', '京都', '大阪', '兵庫', '奈良', '歌山', '鳥取', '島根', '岡山', '広島', '山口', '徳島',
          '香川', '愛媛', '高知', '福岡', '佐賀', '長崎', '熊本', '大分', '宮崎', '児島', '沖縄']

screen_name = 'zishin3255'
url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + screen_name

if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        logging.basicConfig(level=logging.DEBUG)
    elif sys.argv[1] == 'info':
        logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARNING)

params = {'count': 1}

file_name = 'final_twi.txt'
txt_file = open(file_name, 'w')

basic_data = open('basic_data.txt')
basic_txt = basic_data.read()
basic_data.close()

final_txt_file = open(file_name)
content = final_txt_file.read()
final_txt_file.close()
print(content)

regex_ken = re.compile(r'都道府県:(\w+)都?県?府?\n')
ken = regex_ken.search(basic_txt)
try:
    ken = ken.group(1)
except:
    ken = ''
if ken in prefec:
    logging.debug('{}は存在します'.format(ken))
else:
    ken = ''
logging.debug(ken + '=====================================')
regex_siku = re.compile(r'市区:(\w+)市?区?\n')
siku = regex_siku.search(basic_txt)
try:
    siku = siku.group(1)
except:
    siku = ''
logging.debug(siku)
regex_chouson = re.compile(r'町村:(\w?)町?村?\n')
chouson = regex_chouson.search(basic_txt)
try:
    chouson = chouson.group(1)
except:
    chouson = ''
logging.debug(chouson)
where = {'都道府県': ken, '市区': siku, '町村': chouson}

print(where)
gc.collect()

logging.debug('get yet')

try:
    req = twitter.get(url, params=params)
except:
    print('=========\nCheck Wi-Fi\n=========')
    sys.exit()

if req.status_code == 200:
    timeline = json.loads(req.text)
    logging.debug(timeline)
    for tweet in timeline:
        tw_txt = tweet['text']
        # TODO 最終ツイとの比較処理
        if content == tw_txt:
            txt_file.write(tw_txt)
            print(tw_txt)
            re_eq_where = re.compile(r'\s?(\w+)で地震')
            re_eq_level = re.compile('震度\s?(\d)')
            info_where = re_eq_where.search(tw_txt)
            info_level = re_eq_level.search(tw_txt)
            # 震度の型チェックが必要
            # 震度の型チェックが必要

            # 緊急地震速報が含まれ、info_whereとinfo_levelがnot None
            if tw_txt.find('緊急地震速報') != -1 and info_where != None and info_level != None:
                print('Earthquake happend\nwhere:{}\nlevel:{}'.format(info_where.group(1), info_level.group(1)))
                try:
                    info_level = int(info_level.group(1))
                except:
                    logging.debug('')
                for loop in prefec:
                    if loop in str(info_where.group(1)):
                        info_prefec = loop
                        print('{}県での地震を観測'.format(info_prefec))
                    else:
                        info_prefec = ''

                if info_prefec == where['都道府県']:
                    print('Here')
                    try:
                        if info_level >= 3:
                            print('DANGER')
                        elif info_level < 3 and info_level >= 0:
                            print('ALEART')
                        else:
                            print('Check Earthquake Value')
                    except:
                        print('Check Earthquake Value')
                else:
                    logging.debug('Not here')

            else:
                logging.debug('This is not EQ')
        else:
            logging.debug('This is not new tweet')

else:
    logging.debug("ERROR: %d" % req.status_code)

txt_file.close()

txt_file = open(file_name)
content = txt_file.read()
txt_file.close()
print(content)
