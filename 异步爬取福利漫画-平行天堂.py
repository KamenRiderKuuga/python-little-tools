import requests
import os
import re
from bs4 import BeautifulSoup
import urllib.request
import aiohttp
import asyncio
from contextlib import closing
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 创建保存目录
save_dir = '平行天堂'
if save_dir not in os.listdir('./'):
    os.mkdir(save_dir)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Safari/537.36'}

cookies = {'ASPSESSIONIDSGDBSTRR': 'PHLNAIMDNOGLNLPACIJJAJHJ', '__utma': '5717153.264278397.1590149613.1590151451.1590174073.3',
           '__utmc': '5717153', '__utmz': '5717153.1590174073.3.3.utmcsr=cartoonmad.com|utmccn=(referral)|utmcmd=referral|utmcct=/comic/5564.html',
           '__gads': 'ID=238bcefd261cd6c4:T=1590149616:S=ALNI_MYHuhTspcgZeZPoJE00qvcpflJXcg', '__utmt': '1', '__utmb': '5717153.1.10.1590174073'}


async def fetch(session, url):
    try:
        headers['Referer'] = url
        async with session.get(url, headers=headers, cookies=cookies) as response:
            return await response.text(encoding='big5')
            # ,aiohttp.ClientConnectorError,aiohttp.ClientPayloadError
    except (aiohttp.ServerDisconnectedError):
        # 由于异步的关系，有时候seesion会被提前关闭，这里捕捉异常，用标准库请求
        resp = requests.get(url, headers=headers)
        resp.encoding = 'big5'
        content = resp.text
        return content


async def main():
    target_url = "https://www.cartoonmad.com/comic/5564.html"
    headers['Referer'] = target_url
    resp = requests.get(target_url, headers=headers)
    resp.encoding = 'big5'
    content = resp.text
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find(name='table', width='800', align='center')
    index = 'https://www.cartoonmad.com'
    tags_a = table.find_all('a')
    chapterNum = 0
    tasks = []
    count = 0
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    r_session = requests.session()
    r_session.mount('http://', adapter)
    r_session.mount('https://', adapter)
    for tag_a in tags_a:
        chapterNum += 1
        herf = tag_a.get('href')
        firsturl = index+herf
        headers['Referer'] = firsturl
        resp = requests.get(firsturl, headers=headers, timeout=60)
        resp.encoding = 'big5'
        content = resp.text
        soup = BeautifulSoup(content, 'lxml')
        pages = soup.find_all(name='a', attrs={"class": "pages"})
        lastPage = int(pages[-2].text)

        for pageNum in range(1, lastPage+1):
            count += 1
            url = "https://www.cartoonmad.cc" + \
                herf[:-8] + str(pageNum).zfill(3)+".html"
            if count == 500:
                await asyncio.gather(*tasks)
                tasks = []
                count = 0
        
            tasks.append(asyncio.create_task(
                         download(r_session,url, chapterNum, pageNum)))

        print(f"正在收集第{chapterNum}卷信息")

    if len(tasks) > 0:
            await asyncio.gather(*tasks)

# 处理网页


async def download(r_session,url, chapterNum, pageNum):
    async with aiohttp.ClientSession() as session:
        page = await fetch(session, url)
        await getImage(r_session,url, page, session, chapterNum, pageNum)


async def getImage(r_session,mainurl, page, session, chapterNum, pageNum):
    soup1 = BeautifulSoup(page, "lxml")
    pics1 = soup1.find_all('img')
    name = f"第{str(chapterNum).zfill(3)}卷"
    chapter_save_dir = os.path.join(save_dir, name)
    if name not in os.listdir(save_dir):
        os.mkdir(chapter_save_dir)
    for pic in pics1:
        url = pic.get('src')
        if('.' in url[-4:]):
            continue
        if url != "":
            pic_save_path = os.path.join(
                chapter_save_dir, str(pageNum).zfill(3))+".jpg"
            headers['Referer'] = mainurl
        try:
            async with session.get(url, headers=headers) as img:
                imgcode = await img.read()
                try:
                    with open(pic_save_path, 'wb') as file:
                        file.write(imgcode)
                        file.close()
                        img.close()
                except:
                    print('文件创建失败')
        except:
            with closing(r_session.get(url, headers=headers, stream=True)) as response:
                print('正在下载'+url)
                chunk_size = 1024
                if response.status_code == 200:
                    with open(pic_save_path, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                        file.close()
                        response.close()
                else:
                    print('链接异常')
asyncio.run(main())
