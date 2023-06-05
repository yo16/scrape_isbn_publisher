from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# ISBNの出版者検索ページ
URL_TARGET = "https://isbn.jpo.or.jp/index.php/fix__ref_pub/"


def get_one_publisher(pub_code):
    print(f"pub_code: {pub_code}")

    # Chrome のオプションを設定する
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_experimental_option('prefs', {
        'safebrowsing.enabled': True,
    })

    driver = None
    try:
        # Seleniumに接続
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=options.to_capabilities(),
            options=options,
        )

        driver.get(URL_TARGET)
        
        # 出版者記号
        driver.find_element(
            By.XPATH,
            "/html/body/section[2]/div/div/div/div/form[1]/p/input[4]"
        ).send_keys(pub_code)
        # 検索ボタン
        driver.find_element(
            By.XPATH,
            "/html/body/section[2]/div/div/div/div/form[1]/p/input[5]"
        ).click()
        WebDriverWait(
            driver, 30
        ).until(
            EC.presence_of_element_located(
                (By.ID, "tblp1")
            )
        )

        # 結果テーブルから"pub_code"を探す
        found = False
        page_no = 0
        found_publisher = ""
        while not found:
            page_no += 1

            td = None
            try:
                td = driver.find_element(
                    By.CSS_SELECTOR,
                    f'#tblp1 tr.sheet[id="{pub_code}"] td:first-child'
                )
            except NoSuchElementException:
                print("not found...")
                pass

            if td:
                found = True
                found_publisher = td.text
                continue
            
            # 見つからなかったので、次へボタンを押す

            # 次へボタンを探す
            next_button = driver.find_element(
                By.XPATH,
                '//*[@id="pubListform"]/table[1]/tbody/tr/td/input[2]'
            )
            if (next_button.get_attribute("class") == "next_disabled"):
                # 使用不可になっていたら次はない
                # まだ見つかっていないのでエラー
                found = True
                found_publisher = f"ERROR: Not Found(until page:{page_no})"
            
            # 押して、次のページになるまで待つ
            next_button.click()
            WebDriverWait(
                driver, 30
            ).until(
                EC.text_to_be_present_in_element(
                    (
                        By.XPATH,
                        '//*[@id="pubListform"]/table[1]/tbody/tr/td'
                    ),
                    f"{page_no + 1}／"
                )
            )

            # 無限ループ回避（念のため）
            if page_no > 10:
                found = True
                found_publisher = "ERROR: Loop 10 count"
            
            print(f"ループ page:{page_no}")

    finally:
        # ブラウザを終了
        if (driver):
            driver.quit()

    print(f"pub_code: {pub_code} -> {found_publisher}")
    return found_publisher

