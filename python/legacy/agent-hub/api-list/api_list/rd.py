import json

import pandas as pd
df = pd.read_csv('new_api.csv')
# print(df)

file = 'crawl_results_20250411_142417.json'
with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)
idx = 0
for i in data:
    if len(str(i.get('markdown'))) > 500:
        idx +=1
    else:
        print(i.get('url'))
print(idx)



# 不能用的
# https://dog-api.kinduff.com/api/facts #

# https://en.wikipedia.org/api/rest_v1 # 已经是api了
# https://docs.microlink.io/api/overview # 访问不了
# https://breakingbadapi.com # 不能用
# https://yesno.wtf/api 不是api 平台
# https://imsea.herokuapp.com 不是api 平台
# https://biriyani.anoram.com/ 暂停服务
# https://ghibliapi.herokuapp.com/ 服务迁移
# https://api.simsimi.vn 访问不了
# https://official-joke-api.appspot.com/jokes 不是api 平台
# http://shibe.online/api # 不是api 平台 网页没有返回
# https://www.tronalddump.io 网页没办法访问
# https://randomfox.ca/ 不是api平台
# https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api 访问不了
# https://api.nasa.gov 需要登陆