import aiohttp
import time
import asyncio
import random
from functools import reduce
from aiohttp import FormData

TRANSLATED_OBJECT = {
    1: "나는 오늘 배고프다. 안녕? 나는 배고파. 안녕?나는 오늘 배고프다. 안녕? 나는 배고파. 안녕?나는 오늘 배고프다. 안녕? 나는 배고파. 안녕?",
    2: "오늘은 친구를 만났다. 네이콘의 하루 네이콘 이름 네오콘 네이콘 네이콘은 한국 서울 특별시 강남구에 위치한 회사이다 와이낫 와이낫",
    3: "살려줘 여기 사람 살아요. 추운 겨울이 지나야 봄이 오겠지. 그때 난 손목으로 시계를 보겠지. 난 시계를 보겠지",
    4: "그래 나도 알아. 영원한 건 없잖아. 당연하다고 믿어왔지만. 생각보다도 외로웠지. 이걸 어른이라고 부른다지만. 절대로 익숙해질 리 없지. 너와도 연락이 뜸해졌지. 서로 가는 길이 멀어져",
    5: "공정거래위원회가 삼성그룹의 사내 급식 일감 몰아주기와 관련해 섬성전자와 삼성디스플레이, 삼성전기, 삼성SDI 등 4개사와 삼성웰스토리에 과징금 2,349억원을 부과하기로 했습니다.",
    6: "삼성전자 법인과 최지성 전 미래전략실장에 대해서는 고발 조치 결정을 내렸습니다.",
    7: "공정위는 삼성전자 등 4개사가 지난 2013년부터 올해 6월까지 사내 급식 물량 전부를 삼성 웰스토리에 수의 계약 방식으로 몰아주고 높은 수준의 이익률을 보장해왔다고 밝혔습니다.",
    8: "삼성웰스토리는 2013년 12월 삼성에버랜드에서 물적분할 한 회사로, 현재 삼성물산이 100% 지분을 갖고 있는 자회사입니다.",
    9: "미래전략실이 나서 웰스토리의 마진을 보장하고 위탁수수료를 지급하는 등의 방식으로 계약 구조를 바꾼 뒤 \"전략실 결정사항으로 절대 바꾸면 안 된다\"는 방침을 내세워 9년 동안 계약을 유지했다는 겁니다.",
    10: "공정위는 2014년과 2018년, 삼성전자가 사내 급식을 경쟁입찰 방식으로 바꾸려 할때도 미래전략실이 이를 중단시켰다고 설명했습니다."
}


async def request(session, url, data, attempt):
    async with session.post(url, data=data) as request:
        print(f"query status code : {await request.text('utf8')} from attempt num {attempt}")


# 요청함수
async def request_sessions(form_data_list):
    async with aiohttp.ClientSession() as session:
        # 작업 목록
        URL = "https://papago.naver.com/apis/n2mt/translate"
        tasks = [asyncio.ensure_future(request(session=session, url=URL, data=data, attempt=form_data_list.index(data))) for data in form_data_list]

        await asyncio.gather(*tasks, return_exceptions=True)


def rand_str_gen():
    rand_str_list = [TRANSLATED_OBJECT[random.randrange(1,11)] for _ in range(5)]
    rand_str = reduce(lambda x, y : x + '\n' + y, rand_str_list)
    data = FormData()
    data.add_field(name='text', value=rand_str)
    return data



def main():
    # 검색 쿼리 (formdata)
    form_data = [rand_str_gen() for _ in range(100)]
    print(form_data)
    start = time.time()
    asyncio.run(request_sessions(form_data))

    duration = time.time() - start
    print(f'Downloaded {len(form_data)} sites in {duration} seconds')


if __name__ == "__main__":
    main()

