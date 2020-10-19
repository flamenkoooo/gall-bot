import tweepy
from tweepy import OAuthHandler
import json
import time
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.alert import Alert


consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET_KEY"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
account = 'realfromis_9'
#account = '테스트용 계정'
# 테스트 내 계정
BASE_DIR = "D:"
#파일 저장, 로그 불러올 폴더

dc_id = "DC_ID"
dc_pw = "DC_PW"
Gallery = 'https://gall.dcinside.com/mgallery/board/write/?id=fromis'
#Gallery = 'https://gall.dcinside.com/mgallery/board/write/?id=savedragon'
#테스트용 갤러리 https://gall.dcinside.com/mgallery/board/write/?id=savedragon


#크롬 driver 위치

chromedriver = "D:\PTN\chromedriver.exe"
#headless 모드 넣긴했는데 dc에서 오류나서 못씀
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
#headless mode 그대로 하면 dc접속 아예 안돼서 user-agent 변경
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")


driver = webdriver.Chrome (chromedriver)
youtube = Alert(driver)
driver.implicitly_wait(2)
driver.get ('https://www.dcinside.com')
driver.find_element_by_name('user_id').send_keys(dc_id)
driver.find_element_by_name('pw').send_keys(dc_pw)
driver.find_element_by_id('login_ok').click()

def upload_text (text, account, id, link):
    driver.get (Gallery)
    driver.find_element_by_name ('subject').send_keys (date, "공트 업데이트")
    driver.find_element_by_id('chk_html').click()
    url = "https://twitter.com/{0}/status/{1}".format(account, id)
    driver.find_element_by_id('tx_canvas_source').send_keys(now, "<br>  @", account, " <br><br>",
                                                            text, "<br>", link, "<br><br>",
                                                            convert (url)
                                                            )
    driver.find_element_by_id('chk_html').click()

def upload_gam_sun_list (text, account, id, link):
    driver.get (Gallery)
    driver.find_element_by_name ('subject').send_keys (date, "감선리스트")
    driver.find_element_by_id('chk_html').click()
    url = "https://twitter.com/{0}/status/{1}".format(account, id)
    driver.find_element_by_id('tx_canvas_source').send_keys(now, "<br>  @", account, " <br><br>",
                                                            text, "<br>", link, "<br><br>",
                                                            convert (url)
                                                            )
    driver.find_element_by_id('chk_html').click()

def upload_content (BASE_DIR, media_id_str):
    media_id_str_jpg = "\{0}.jpg".format (media_id_str)
    driver.find_element_by_xpath('//*[@id="fileupload"]/div[1]/input').send_keys (BASE_DIR+media_id_str_jpg)
    time.sleep (5)


#이모지 지우기
def delEmoji (inputData):
    return inputData.encode ('cp949', 'ignore').decode ('cp949')

#불필요 텍스트/금칙어 정리하기
def clean_text (orig):
    result = orig.replace ("\n", "<br>")
    result2 = result.replace ("네이버", "네/이/버")
    return result2


# 파일 다운로드 함수. :orig로 원본 저장
def download (media_url, media_id_str):
    urllib.request.urlretrieve (media_url+":orig", BASE_DIR+media_id_str+".jpg")

#url 태그 삽입
def convert (url):
    result = '<a href = "{0}" target="_blank" class="tx-link">{0}</a>'.format(url)
    return result

## 트윗 파싱
@classmethod
def parse(cls, api, raw):
    Status = cls.first_parse(api, raw)
    setattr(Status, 'json', json.dumps(raw))
    return Status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#media files 정의
media_files = list()
media_files_id = list()
link = list()
url = ''


while True:
##여기서 부터 반복문으로 넣으면 됨
    tweets = api.user_timeline(screen_name=account,count=1, include_rts=True, exclude_replies=False, tweet_mode='extended')
    for Status in tweets:
        id_str=Status.id_str
        ##과거 id_str와 비교. id.TXT에 id 저장
        with open (os.path.join(BASE_DIR, 'id.TXT'), 'r') as id_str_read:
            before = id_str_read.read()
            if before != id_str:
                #업데이트 되었으면 시작
                contents = 0
                print ('새 소식이 있습니다')
                #RT인 경우 불러오는 entity 다르므로
                if hasattr (Status, 'retweeted_status'):
                    content = Status.retweeted_status
                    print ('RT입니다')
                else:
                    content = Status
                    print ('트윗입니다')
                text_orig = content.full_text
                text = clean_text (delEmoji(text_orig))
                #본문은 text에 저장
                print (text)
                # 브이앱이나 컨텐츠 알람 굳이 올릴 필요 없으니까
                if '지금 바로!' not in text and 'FM_1.24' not in text:
                    if 'urls' in content.entities:
                        for links in content.entities['urls']:
                            link.append (convert(links['expanded_url']))
                            url = "<br>".join(link)
                    #글 부터 쓰자
                    now = time.strftime('[%H:%M]')
                    date = time.strftime ('[%y%m%d]')
                    if '#gam_sun_list' in text:
                        print('감선리스트')
                        upload_gam_sun_list (text, account, id_str, url)
                    else:
                        upload_text(text, account, id_str, url)
                    if hasattr (content, 'extended_entities'):
                        #그냥 entities보다 extended_entities가 파일 단수/복수일 경우 대응 가능.
                        media = content.extended_entities.get ('media', [])
                        # url,id를  media_files set에 추가함
                        v = len(media)
                        for media_element in media:
                            if "video_info" in media_element:
                                print ('video 입니다')
                                v = 99
                            download (media_element['media_url'], media_element['id_str'])
                            media_files.append (media_element['media_url'])
                            media_files_id.append (media_element['id_str'])
                        time.sleep (1)
                        driver.find_element_by_xpath('//*[@id="tx_image"]/a').click()
                        driver.switch_to.window(driver.window_handles[1])
                        for media_file_id in media_files_id:
                            upload_content (BASE_DIR, media_file_id)

                        driver.find_element_by_xpath('/html/body/div/div/div[2]/button').click()
                        driver.switch_to.window(driver.window_handles[0])
                        del media[:]
                        time.sleep (1)
                    time.sleep (2)
                    driver.find_element_by_xpath('//*[@id="write"]/div[5]/button[2]').click()
                    if 'youtube' in url or 'youtu.be' in url:
                        youtube.accept ()
                    time.sleep (4)
                    print ('업로드 성공')




            #아니면 그냥 그대로입니다 하고 끝
            else:
                 print ('그대로 입니다')
            id_str_read.close()

    ##id.txt 업데이트 하기
    with open (os.path.join (BASE_DIR, 'id.TXT'), 'w+') as id_str_write:
        id_str_write.write (id_str)
        id_str_write.close()
    #media 청소
    media_files_id.clear ()
    media_files.clear ()
    link.clear ()
    url = ''
    time.sleep (10)
    #dc 오랫동안 페이지 이동 안 하다가 동작하면 오류남
    driver.refresh()

