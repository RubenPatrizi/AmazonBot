import time
from datetime import datetime
import re
from sys import exit
import selenium.webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from text import *

class Offer:
    def __init__(self, text: str, cart_id: int, seller: str):
        self.full_text: str = text
        self.price: int = get_price_from_text(text)
        self.cart_id: int = cart_id
        self.seller: str = seller
        

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

    #log_pipe.put(f"&&&Starting {COUNTRY.upper()}...\n")      #STARTING

    offers = list()

    options = Options()
    options.add_argument("--disable-cache")

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

    b = wd.Chrome(options=options)
    
    try:
        b.get(ITEM_URL)
        # if captcha screen try to skip by loading another image (for some reason this works)
        b.find_element(By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/div/div[2]/a').click()
        log_pipe.put(f'&&&{Captcha[LAN]}')
    except:
        pass

    try:
        error_code = 1  # MAIN PAGE ERROR
        title = b.find_element('id', 'productTitle').text
        title = '#@$' + title
        log_pipe.put(title)
        time.sleep(1)
    except:
        pass

    while True:
        try:
            b.find_element('id', 'sp-cc-accept').click()
        except:
            pass
        error_code = 1
        success = 0
        price_single = 0
        price_multi = 0
        is_pinned_offer: bool = False

        pinned_seller = ''
        if len(SELLERS) > 0:
            try:
                b.find_element('id','aod-pinned-offer-show-more-link').click()
                pinned_seller = b.find_element('id', 'aod-pinned-offer-additional-content').text
            except:
                pass
        try:
            b.find_element(By.ID, "aod-pinned-offer-show-more-link").click()
            pinned_seller = b.find_element(By.ID, "aod-pinned-offer-additional-content")
            pinned_offer = b.find_elements(By.ID,'pinned-de-id')
            if pinned_offer[0].text:
                pinned_offer_text = pinned_offer[0].text
            else:
                pinned_offer_text = pinned_offer[1].text
            pinned_offer_text += '\n'+pinned_seller.text
            seller_match: str = find_seller_match(pinned_offer_text,SELLERS,COUNTRY)
            condition_match: bool = filter_conditions(pinned_offer_text,CONDITIONS,COUNTRY)
            if not seller_match or not condition_match:
                continue
            is_pinned_offer = True
            pinned_offer = Offer(pinned_offer_text, 0, seller_match)
            offers.append(pinned_offer)
        except:
            pass

        all_offers = b.find_elements(By.ID, 'aod-offer')
        cart_index = 0

        for offer in all_offers:
            if len(offers) > 0:
                cart_index += 1
            seller_match: str = find_seller_match(offer.text,SELLERS,COUNTRY)
            condition_match: bool = filter_conditions(offer.text,CONDITIONS,COUNTRY)
            if not seller_match or not condition_match:
                continue
            offer = Offer(offer.text, cart_index, seller_match)
            offers.append(offer)
        try:

            best_offer: Offer = get_best_offer(offers)
            price = best_offer.price
            
            if 0 < price <= LIMIT_VALUE:
                log_pipe.put(f"&&&{COUNTRY.upper()}:  {datetime.now().strftime('%d/%m - %H:%M:%S')} - {price}{coin} ({percentage_diff(LIMIT_VALUE,price)}%) ✔\n")
                if NOTIF:
                    b.get(send_notif(title, price, TELEGRAM, ITEM_URL_FOR_TG))
                    time.sleep(5)
                    log_pipe.put("@@@✔✔ TELEGRAM ALERT ✔✔\n")
                    b.stop_client()
                    exit()
                atc = b.find_elements('class name','a-button-inner')
                for cart in atc.copy():
                    if cart.text != ADD_TO_CART[COUNTRY]:
                        atc.remove(cart)
                try:
                    atc[get_best_offer_index(best_offer, is_pinned_offer)].click()
                    time.sleep(1)
                    if price_multi > 0 >= price_single:
                        cart_id += 1
                    log_pipe.put("@@@Adding to cart...\n")
                except:
                    pass
                time.sleep(1)
                b.get(f"https://www.amazon.{uk_link + COUNTRY}/gp/cart/view.html?ref_=nav_cart")
                time.sleep(1)
                b.find_element('id','sc-buy-box-ptc-button').click()
                error_code = 2  # LOGIN ERROR
                log_pipe.put("@@@Login...\n")

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
                log_pipe.put("@@@Checkout...\n")
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
                for t in range(0,REFRESH-7):
                    if not bot_pipe.empty():
                        exit()
                    time.sleep(1)
                b.delete_all_cookies()
                b.get(ITEM_URL)
                bot(LAN, LIMIT_VALUE, LOGIN_MAIL, LOGIN_PASSWORD, COUNTRY, TELEGRAM, PATH, ITEM_URL, ITEM_URL_FOR_TG,
                    REFRESH, NOTIF, HEADLESS, CONDITIONS, SELLERS, log_pipe, bot_pipe)
        except:
            match error_code:
                case 0:
                    log_pipe.put("❌❌ BROWSER ERROR ❌❌\n")
                case 1:
                    log_pipe.put("❌❌ MAIN PAGE ERROR ❌❌\n")
                case 2:
                    log_pipe.put("❌❌ MAIL ERROR ❌❌\n")
                case 3:
                    log_pipe.put("❌❌ CHECKOUT ERROR ❌❌\n")
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

def percentage_diff(base,actual) -> str:
    diff = abs(actual-base)
    perc = diff*100/base
    if actual-base > 0:
        return "+%.1f" % perc
    return "-%.1f" % perc

def get_price_from_text(price: str) -> int:
    try:
        matches = re.findall(pattern="\n[0-9]*.?[0-9]*\n",string=price)
        res = matches[0][1:-1]
        res = res.replace('€','')
        res = res.replace('£', '')
        res = res.replace(',', '')
        return int(res.replace('.', ''))
    except:
        return -1

def filter_conditions(string: str, cond: int, country: str) -> bool:
    if (cond == 1 and string.find(USED[country]) != -1) or \
       (cond == 2 and not string.find(USED[country]) != -1):
        return False
    return True

def find_seller_match(seller: str, sellers: str, country: str) -> str:
    if sellers == '':
        return re.findall(pattern=f"\n(?:{SOLD_BY[country]})\n(?:[a-zA-Z0-9_]+)", string=seller)[0].split("\n")[2]
    match: str
    for seller in sellers.split(','):
        seller = str(seller).replace('\n','')
        matches = re.findall(pattern=f"\n(?:{SOLD_BY[country]})\n(?:{seller})", string=seller)
        if len(matches) > 0:
            match = matches[0]
            break
    return match

def get_best_offer(offers: list[Offer]) -> Offer:
    if len(offers) == 0:
        return None
    offers.sort(key=sort_by_price)
    return offers[0]

def sort_by_price(offer: Offer):
    return offer.price

def get_best_offer_index(best_offer: Offer, is_pinned_offer: bool) -> int:
    if is_pinned_offer:
        return best_offer.cart_id
    else:
        return best_offer.cart_id - 1
