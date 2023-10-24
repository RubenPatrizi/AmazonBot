import time
from datetime import datetime
import re
from sys import exit
import selenium.webdriver as wd
import selenium.webdriver.common.by
from selenium.webdriver.chrome.options import Options
from text import *


def send_conf(title,price,usr):
    text = f"Articolo \"{title}\" acquistato a {price}€%0A{usr}"
    token = ''    # your token
    chat_id = ''   # your chat id
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    return url_req

def send_notif(title,price,usr,url):
    text = f"{usr}%0A%0A{title}%0A%0A💸 {price}€%0A%0A{url}"
    token = ''  # your token
    chat_id = ''  # your chat id
    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&disable_web_page_preview=true"
    return url_req

def bot(LAN, LIMIT_VALUE, LOGIN_MAIL, LOGIN_PASSWORD, COUNTRY, TELEGRAM, PATH, ITEM_URL, ITEM_URL_FOR_TG, REFRESH, NOTIF, HEADLESS, CONDITIONS, SELLERS, log_pipe, bot_pipe):

    log_pipe.put(f"&&&Starting {COUNTRY.upper()}...\n")      #STARTING

    options = Options()

    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--window-size=%s" % "1920,1080")

    if COUNTRY == 'co.uk':
        coin = '£'
        uk_link = 'co.'
    else:
        coin = '€'
        uk_link = ''

    if COUNTRY == 'co.uk':
        COUNTRY = 'uk'

    try:
        b = wd.Chrome(executable_path=PATH,options=options)
    except:
        log_pipe.put(f'&&&{Version_error[LAN]}')
        exit()
    try:
        b.get(ITEM_URL)
        # if captcha screen try to skip by loading another image
        b.find_element(selenium.webdriver.common.by.By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/div/div[2]/a').click()
        log_pipe.put(f'&&&{Captcha[LAN]}')
    except:
        pass

    try:
        error_code = 1  # MAIN PAGE ERROR
        b.find_element('id', 'sp-cc-accept').click()
        title = b.find_element('id', 'productTitle').text
        title = '#@$' + title
        log_pipe.put(title)
        time.sleep(1)
    except:
        pass

    while True:
        error_code = 0
        success = 0
        price_single = 0
        price_multi = 0

        try:
            seller_position = -1
            all_offers = b.find_elements('id', 'aod-offer')
            while price_multi <= 0:  # check multiple aod offers until one with right conditions
                seller_position += 1  # and allowed seller is found. It will already be the
                price = all_offers[seller_position].text  # lowest price one since they are already sorted by price
                if filter_conditions(price, CONDITIONS, COUNTRY) and filter_sellers(price, SELLERS, COUNTRY):
                    price_multi = get_price_from_text(price)
                else:
                    price_multi = -1
            b.find_element('id','aod-pinned-offer-show-more-link').click()
            offer = b.find_elements('id','pinned-de-id')
            pinned_seller = b.find_element('id', 'aod-pinned-offer-additional-content').text
            price = offer[1].text
            if filter_conditions(price,CONDITIONS,COUNTRY) and filter_sellers(pinned_seller,SELLERS,COUNTRY):
                price_single = get_price_from_text(price)
            else: price_single = -1

            if price_single == -1 and price_multi == -1:
                price = -1
            if price_single == 0 and price_multi == 0:
                price = 999999
            elif (0 < price_single <= price_multi or price_multi == 0) or (0 < price_single and price_multi == -1):
                cart_id = 3
                price = price_single
            elif (price_single > price_multi > 0 or price_single == 0) or (0 < price_multi and price_single == -1):
                cart_id = 3+(seller_position+1)*3
                price = price_multi
            if 0 < price <= LIMIT_VALUE:
                log_pipe.put(f"&&&{COUNTRY.upper()}:  {datetime.now().strftime('%d/%m - %H:%M:%S')} - {price}{coin} ({percentage_diff(LIMIT_VALUE,price)}%) ✔\n")
                if NOTIF:
                    b.get(send_notif(title, price, TELEGRAM, ITEM_URL_FOR_TG))
                    time.sleep(5)
                    log_pipe.put(-6)      #TELEGRAM ALERT
                    b.stop_client()
                    exit()
                atc = b.find_elements('class name','a-button-input')
                try:
                    loc = atc[cart_id].location
                    b.set_window_position(loc['x'],loc['y'])
                    atc[cart_id].click()
                    log_pipe.put(-2)       # ADD TO CART
                except:
                    pass
                time.sleep(1)
                b.get(f"https://www.amazon.{uk_link + COUNTRY}/gp/cart/view.html?ref_=nav_cart")
                time.sleep(1)
                b.find_element('id','sc-buy-box-ptc-button').click()
                error_code = 2  # LOGIN ERROR
                log_pipe.put(-3)  # LOGIN

                if len(b.find_elements('id','phone-tab')) > 0:
                    b.find_element('id', 'email-tab').click()
                    time.sleep(1)
                    b.find_element('id','claim-input').send_keys(LOGIN_MAIL)
                    b.find_element('id','claim-submit-button').click()
                else:
                    time.sleep(1)
                    # b.find_element('id','ap_email').click()
                    b.find_element('id','ap_email').send_keys(LOGIN_MAIL)
                    b.find_element('id','continue').click()

                b.find_element('id','ap_password').send_keys(LOGIN_PASSWORD)
                b.find_element('id','signInSubmit').click()
                time.sleep(5)
                try:
                    if b.find_element('id','prime-declineCTA').is_displayed():
                        b.find_element('id','prime-declineCTA').click()
                except:
                    pass
                error_code = 3      # CHECKOUT ERROR
                log_pipe.put(-4)     # CHECKOUT
                try:
                    b.find_element('id','shipToThisAddressButton').click()
                    time.sleep(5)
                    b.find_element('id','orderSummaryPrimaryActionBtn').click()
                    time.sleep(5)
                    b.find_element('name','placeYourOrder1').click()
                    success = 1
                    break
                except:
                    pass
                try:
                    b.find_element('id','orderSummaryPrimaryActionBtn').click()
                    time.sleep(5)
                    b.find_element('name','placeYourOrder1').click()
                    success = 1
                    break
                except:
                    pass
                try:
                    b.find_element('name','placeYourOrder1').click()
                    success = 1
                    break
                except:
                    pass
            else:
                if price in [2,999999]:
                    log_pipe.put(f"&&&{COUNTRY.upper()}:  {datetime.now().strftime('%d/%m - %H:%M:%S')} - Unable to get price\n")
                elif price == -1:
                    log_pipe.put(f"&&&{COUNTRY.upper()}:  {datetime.now().strftime('%d/%m - %H:%M:%S')} - No offer available\n")
                else:
                    log_pipe.put(f"&&&{COUNTRY.upper()}:  {datetime.now().strftime('%d/%m - %H:%M:%S')} - {price}{coin} ({percentage_diff(LIMIT_VALUE,price)}%) ❌\n")
                for seller_position in range(0,REFRESH):
                    if not bot_pipe.empty():
                        exit()
                    time.sleep(1)
                b.refresh()
        except:                                # error management
            log_pipe.put(error_code)
            if bot_pipe.empty():
                if COUNTRY == 'uk':
                    COUNTRY = 'co.uk'
                if HEADLESS:
                    log_pipe.put(f"&&&Restarting {COUNTRY.upper()} non headless...\n")  # restart in normal mode to avoid bot detection
                    b.quit()
                    bot(LAN,LIMIT_VALUE,LOGIN_MAIL,LOGIN_PASSWORD,COUNTRY,TELEGRAM,PATH,ITEM_URL,ITEM_URL_FOR_TG,REFRESH,NOTIF,False,CONDITIONS,SELLERS,log_pipe,bot_pipe)
                elif not HEADLESS and error_code >= 2:   # non-headless and problem with login
                    b.switch_to.new_window('tab')
                    b.get(url=send_notif(title[3:],price,"Login issue for this product",ITEM_URL_FOR_TG))   # notifying user
                    time.sleep(3)
                    log_pipe.put(f"&&&Login failed, Telegram alert sent...\n")
                    b.quit()
                    exit()
                else:
                    log_pipe.put(f"&&&Restarting {COUNTRY.upper()}...\n")  # restart for general error
                    b.quit()
                    bot(LAN,LIMIT_VALUE,LOGIN_MAIL,LOGIN_PASSWORD,COUNTRY,TELEGRAM,PATH,ITEM_URL,ITEM_URL_FOR_TG,REFRESH,NOTIF,HEADLESS,CONDITIONS,SELLERS,log_pipe,bot_pipe)
            exit()

    if success == 1:
        log_pipe.put(f"&&&✔✔ {Acquistato[LAN]} {price}{coin} ✔✔\n")       # confirm order
        if len(TELEGRAM) > 1:
            b.switch_to.new_window('tab')
            b.get(url=send_conf(title,price,TELEGRAM))
            time.sleep(5)
        b.close()
    exit()

def percentage_diff(base,actual):
    diff = abs(actual-base)
    perc = diff*100/base
    if actual-base > 0:
        return "+%.1f" % perc
    return "-%.1f" % perc

def get_price_from_text(price):
    matches = re.findall(pattern="\n[0-9]*.?[0-9]*\n",string=price)
    res = matches[0][1:-1]
    res = res.replace('€','')
    res = res.replace('£', '')
    res = res.replace(',', '')
    return int(res.replace('.', ''))

def filter_conditions(string, cond, country):
    if (cond == 1 and string.find(USED[country]) != -1) or \
       (cond == 2 and not string.find(USED[country]) != -1):
        return False
    return True

def filter_sellers(string, sellers, country):
    for seller in sellers.split(','):
        matches = re.findall(pattern=f"\n(?:{SOLD_BY[country]})\n(?:{seller})", string=string)
        if len(matches) > 0:
            return True
    return False
