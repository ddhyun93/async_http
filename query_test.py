import aiohttp
import time
import asyncio
import random
import bs4
from functools import reduce

TRANSLATED_OBJECT = {
    1: "공정거래위원회가 삼성그룹의 사내 급식 일감 몰아주기와 관련해 섬성전자와 삼성디스플레이, 삼성전기, 삼성SDI 등 4개사와 삼성웰스토리에 과징금 2,349억원을 부과하기로 했습니다.",
    2: "삼성전자 법인과 최지성 전 미래전략실장에 대해서는 고발 조치 결정을 내렸습니다.",
    3: "공정위는 삼성전자 등 4개사가 지난 2013년부터 올해 6월까지 사내 급식 물량 전부를 삼성 웰스토리에 수의 계약 방식으로 몰아주고 높은 수준의 이익률을 보장해왔다고 밝혔습니다.",
    4: "삼성웰스토리는 2013년 12월 삼성에버랜드에서 물적분할 한 회사로, 현재 삼성물산이 100% 지분을 갖고 있는 자회사입니다.",
    5: "미래전략실이 나서 웰스토리의 마진을 보장하고 위탁수수료를 지급하는 등의 방식으로 계약 구조를 바꾼 뒤 \"전략실 결정사항으로 절대 바꾸면 안 된다\"는 방침을 내세워 9년 동안 계약을 유지했다는 겁니다.",
    6: "공정위는 2014년과 2018년, 삼성전자가 사내 급식을 경쟁입찰 방식으로 바꾸려 할때도 미래전략실이 이를 중단시켰다고 설명했습니다."
}


async def request(session, url, attempt):
    async with session.get(url) as request:
        # print(f"query status code : {await request.text('utf8')} from attempt num {attempt}")
        text = await request.text()
        soup = bs4.BeautifulSoup(text, features="html.parser")
        result = soup.select_one('span[id*=tw-answ-target-text]').text
        print(f"[translated result] : \n{result}\n[from attempt num: {attempt}]")


# 요청함수
async def request_sessions(data_dict):
    async with aiohttp.ClientSession() as session:
        # 작업 목록
        URL = "https://em56ce3j4m.execute-api.ap-northeast-2.amazonaws.com/dev/api/v1.4/translate"
        tasks = [asyncio.ensure_future(request(session=session, url=URL+data['query_string'],
                 attempt=data_dict.index(data))) for data in data_dict]

        await asyncio.gather(*tasks, return_exceptions=True)


def rand_str_gen():
    rand_str_list = [TRANSLATED_OBJECT[random.randrange(1,7)] for _ in range(5)]
    rand_str = reduce(lambda x, y : x + '\n' + y, rand_str_list)

    TEXT = rand_str
    SOURCE = 'ko'
    TARGET = 'en'

    # data = FormData()
    # data.add_field(name='text', value=rand_str)
    # data.add_field(name='deviceId', value=DEVICE_ID)
    # headers = {'authorization': AUTH_CODE, 'cookie': COOKIE}
    return {'query_string': f"?text={TEXT}&source={SOURCE}&target={TARGET}"}


def main():
    # 검색 쿼리 (formdata)
    data = [rand_str_gen() for _ in range(1000)]
    start = time.time()
    asyncio.run(request_sessions(data))

    duration = time.time() - start
    print(f'Downloaded {len(data)} sites in {duration} seconds')


if __name__ == "__main__":
    main()

