from selenium import webdriver #Selenium Webdriverをインポートして
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import random
import os

#要素を探してスクロールして購入する関数
def buy_food(driver,id,key_element):
    print(len(driver.find_elements_by_class_name(key_element)))
    target = driver.find_elements_by_class_name(key_element)[id]
    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()
    driver.find_elements_by_class_name(key_element)[id].click()

#スクロールしてクリックする関数
def scroll_and_click(driver,key_element,key_word):
    target = driver.find_elements_by_class_name(key_element)

    #取得した要素群の一覧を表示
    index = 0
    for item in target:
        print(target[index].text)
        index +=1
        
        #取得した要素群の一覧からキーワードに合致するものをクリック
        if target[index].text == key_word:
            target = driver.find_elements_by_class_name(key_element)[index]
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            driver.find_elements_by_class_name(key_element)[index].click()
            break

#複数購入する
def buy_foods(driver,num):

    #0から14でランダムで重複なしセットを購入数分生成する
    num_l = range(14)
    choice_list = random.sample(num_l,num)
    choice_list.sort()
    print(choice_list)

    #購入する
    for item in choice_list:
        sleep(1)
        buy_food(driver,item,'ipss_item_list_cart_add')

#lambda関数
def lambda_handler(event, context):
    #headlessオプション設定
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--v=99")
    options.add_argument("--single-process")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")
    options.binary_location = "./bin/headless-chromium"

    #Chromeを動かすドライバを読み込み
    driver = webdriver.Chrome(
        "./bin/chromedriver", chrome_options=options)

    #パスシステムログインページを開く
    driver.get("https://shop.pal-system.co.jp/iplg/login.htm?PROC_DIV=1") 
    #Windowを最大化してクリックしやすくする
    driver.maximize_window()

    #ログイン(lamda環境変数の利用)
    driver.find_element_by_name('S9_').send_keys(os.environ['email'])
    driver.find_element_by_name('S11_').send_keys(os.environ['password'])

    #お料理セットのページへ
    driver.find_element_by_class_name('btn-default').click()
    driver.find_element_by_class_name('navi-side').click()
    sleep(2)
    driver.find_element_by_class_name('navi-side').click()
    #sleepいれて購入のときの要素を読み込む
    sleep(2)
    #購入
    buy_foods(driver,2)


    #冷凍食品のフライのページへ
    sleep(1)
    driver.get("https://shop.pal-system.co.jp/pal/InesOrderContents.do")
    scroll_and_click(driver,'oAcordion','冷凍食品')
    scroll_and_click(driver,'oGran','フライ・ハンバーグ')
    #sleepいれて購入のときの要素を読み込む
    sleep(2)
    #購入
    buy_foods(driver,4)

    #冷凍食品の麺類のページへ
    sleep(1)
    driver.get("https://shop.pal-system.co.jp/pal/InesOrderContents.do")
    scroll_and_click(driver,'oAcordion','冷凍食品')
    scroll_and_click(driver,'oGran','麺類')
    #sleepいれて購入のときの要素を読み込む
    sleep(2)
    #購入
    buy_foods(driver,3)

    #カートのページへ
    sleep(1)
    driver.get("https://shop.pal-system.co.jp/pal/OrderConfirm.do")
    sleep(1)
    driver.get("https://shop.pal-system.co.jp/pal/OrderConfirmFix.do")
    print("end")
    driver.close()