import datetime
import time
Date = datetime.date.today() + datetime.timedelta(days=0)
TDate = Date.strftime("%Y_%m_%d")
import requests
from threading import  Thread
import os
from scrapy.http import HtmlResponse
import sys
sys.path.insert(0, r'E:\Tracetunnel\request_engine-0.0.0-cp311-cp311-win_amd64\Xbyte_Common_Scrape')
import request_engine
import pymongo
con = pymongo.MongoClient("mongodb://adarshs:YdaJ(4sw@192.168.0.50:27017/?authSource=admin")
db = con['amit_kup_a_k_il_3433_1']
# coll = db[f'mapping_pl_2025_07_23__']
coll = db[f'mapping_pl_{TDate}']

pdp_collection = db[f'English_PDP_{TDate}']
def pdp_data(a,b):
    search =coll.find({'status':'pending'}).skip(a).limit(b)
    for ii in search:
        object_id=ii['_id']
        url = ii['url']
        asin1 = ii['asin']
        main_category1 = ii['category']
        pagesave = ii['pagesave']
        url1 = url
        url2 = f'{url1}&tag=smitdeals-20'

        url = f'{url1}&th=1&language=en_US'

        payload = {}
        headers = {
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'cookie': 'session-id=137-9193413-9419338; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=130-8646178-3954249; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20246%7CMCMID%7C77599018055442555492050136625834459643%7CMCAAMLH-1749816482%7C12%7CMCAAMB-1749816482%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1749218882s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; regStatus=pre-register; s_nr=1751446968579-New; s_vnum=2183446968579%26vn%3D1; s_dslv=1751446968579; sp-cdn="L5Z9:IL"; session-token=Se0ibc4bVFDLbvyy8W6SmZjGtEtQ2ylzWbJlybQP6CfO+eSHEZMEKJSxnMdxW2Y33QVRXDNCHSDlO4JhumLNDNBHANBF+6AigDHlI5uADs1UoxFIlcai3AQoeXucTx9oHf1vHQecBB6LLzXibSIxszzeJ0ZnKArRQF4ozTYRgqrzyBGxHQhZIkTL3pcTO+RMWbF6IAMzof/8+/bPsoGhvJgCsB9YBtTyJLo1iarHLci9yTtLjneOfL46nFrJe5FPkJoDgbe3jpntrZuAo2BV0MEXCmPwA520QmSAGVOWLhTJjxs+xpLzhQVhdO3UfjdQbMVG4aBaQoJwCRxscynq4iF/rhpGQrLN; lc-main=en_US; csm-hit=tb:H5KBV9QP9B54EB6ZJFY7+s-H5KBV9QP9B54EB6ZJFY7|1755229943640&t:1755229943640&adb:adblk_no; rxc=ANdxzMNU3kzsEPaJiRg',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
        }

        # response = requests.request("GET", URL, headers=headers, data=payload)

        args = {
            "url": url,
            "headers":headers,  # Provide yours if any
            "request_type": "GET",  # Method should be define get and post
            "proxy": 'scraper-api',  # Provide yours if any
            "proxy_region":'IL',  # Provide yours while using country code if not then Keep it None
            "projectid": "3433",  # from glacier
            "feedid": "15635"
        }

        response = request_engine.make_xbt_request(**args)

        if response.status_code==200:

            try:
                path = f'e:\\amazon_israel\\{TDate}\\EN_pdp\\'
                if not os.path.exists(path):
                    os.makedirs(path)
                full_path1 = os.path.join(path, f'{object_id}.html')
                with open(full_path1, 'w', encoding='utf-8') as file:
                    file.write(response.text)
            except Exception as e:
                print(f"Error saving HTML: {e}")
            # print(response.text)
            content = HtmlResponse(url=url,body=response.content)
            try:
                product_title = content.xpath('//span[@id="productTitle"]//text()').get()
                product_title = product_title.strip()
            except:
                product_title = ''

            try:
                total_rating = content.xpath('//span[@id="acrCustomerReviewText"]//text()').get()
                total_rating = total_rating.replace('ratings', '')
                total_rating =total_rating.strip()
            except:
                total_rating = ''

            try:
                brand = content.xpath('//a[@id="bylineInfo"]/text()').get().replace('Visit', '').replace('the',
                                                                                                          '').replace(
                    'Store', '').replace('Brand:', '')
                brand = brand.strip()
            except:
                brand = ''
            if brand == '':
                try:
                    brand = content.xpath('//span[contains(text(),"Brand")]/../following-sibling::td/span/text()').get()
                except:
                    brand = ''

            try:
                avg_rating = content.xpath('''//div[@id="averageCustomerReviews"]//span//a[@role="button"]//span//text()''').get()
                avg_rating = avg_rating.strip()
            except:
                avg_rating = ''

            amazon_choice = content.xpath(
                '//span[@class="aok-float-left mvt-ac-badge-rectangle"]/span[@class="a-size-small" and contains(normalize-space(text()), "Amazon")]').get()
            if amazon_choice is not None and 'Amazon' in amazon_choice:
                amazon_choice = 'Yes'
            else:
                amazon_choice = ''

            description = []
            try:
                product_description_loop = content.xpath('//div[@id="feature-bullets"]//ul//li')
                if product_description_loop:
                    for dec in product_description_loop:
                        product_description = dec.xpath('''.//span[@class="a-list-item"]//text()''').get()
                        product_description = product_description
                        description.append(product_description)
            except:
                description = ''

            if description:
                product_description = '|'.join(description)
            else:
                product_description = ''
            primary_image = ''
            # secondary_image = []
            try:
                image = content.xpath('''//div[@class="imgTagWrapper"]//img/@src''')
                if image:
                    i = 0
                    for im in image:
                        iamges = im.get()
                        if i == 0:
                            primary_image = iamges
                            i = 1
                        # else:
                        #     secondary_image.append(secondary_image)
            except:
                primary_image = ''
            try:
                second_image = content.xpath('''//div[@id="altImages"]//ul//li//img/@src''').getall()
                if second_image:
                    secondary_image = '|'.join(second_image)
                else:
                    secondary_image = ''
            except:
                secondary_image = ''


            if primary_image is not None or primary_image!='':
                extracted = primary_image.split("images/I/")[1].split('.')[0]
                new_primary_image = f"https://m.media-amazon.com/images/I/{extracted}.jpg" if ".jpg" in primary_image else f"https://m.media-amazon.com/images/I/{extracted}.png" if ".png" in primary_image else ''
            else:
                new_primary_image=''

            if secondary_image is not None or secondary_image!='':
                cleaned_secondary_image = '|'.join([
                    f"https://m.media-amazon.com/images/I/{i.split('images/I/')[1].split('.')[0]}.jpg"
                    if ".jpg" in i else
                    f"https://m.media-amazon.com/images/I/{i.split('images/I/')[1].split('.')[0]}.png"
                    if ".png" in i else ''
                    for i in secondary_image.split('|')
                    if "images/I/" in i and (".jpg" in i or ".png" in i)
                ])
            else:
                cleaned_secondary_image=''
            asin = ''
            try:
                details = content.xpath('''//table[@id="productDetails_detailBullets_sections1"]//tr''')
                if details:
                    for de in details:
                        asin_check = de.xpath('.//th//text()').get()
                        if 'ASIN' in asin_check:
                            asin = de.xpath('''.//td//text()''').get()

            except:
                asin = ''
            # try:
            #     product_price = content.xpath(
            #         '''//div[@class="a-box-group"]//span[contains(@class,'a-price')]//span[@class="a-offscreen"]//text()''').get()
            #     product_price = product_price
            # except:
            #     product_price = ''
            #
            # if product_price:
            #     product_price = product_price.replace('$', '')
            # else:
            #     try:
            #         product_price = content.xpath(
            #             '//div[@id="primeSavingsUpsellAccordionRow"]//h5//div[@id="corePrice_feature_div"]//span//span[@class="a-offscreen"]//span//following-sibling::text()').get()
            #         product_price = product_price
            #     except:
            #         product_price = ''
            # try:
            #     product_price_original = content.xpath(
            #         '''//div[@data-feature-name="corePriceDisplay_desktop"]//div//span//span[@class="aok-relative"]//span[contains(text(),'$')]/text()''').get()
            #     product_price_original = product_price_original.replace('List Price:', '').replace('$', '').replace('Typical price:','')
            #     product_price_original = product_price_original.strip()
            # except:
            #     product_price_original = product_price
            #     product_price = ''

            try:
                list_price = content.xpath(
                    '//td[contains(text(),"List Price:")]//following-sibling::td//span[@class="a-offscreen"]//text()').get(
                    '')

                if not list_price:
                    list_price = content.xpath(
                        '//td[contains(text(),"Typical price:")]//following-sibling::td//span[@class="a-offscreen"]//text()').get(
                        '')

                if not list_price:
                    list_price = content.xpath(
                        '//span[contains(text(),"List Price:")]//following-sibling::span[contains(@class,"text-price")]//span[@class="a-offscreen"]//text()').get(
                        '')
                    if not list_price:
                        list_price = content.xpath(
                            '//td[contains(text(),"Was:")]//following-sibling::td//span[@class="a-offscreen"]//text()').get(
                            '')
                        if not list_price:
                            list_price = content.xpath(
                                '//span[contains(@class,"basisPrice")]//span[@class="a-price a-text-price"]//text()').get(
                                '')
                            if not list_price:
                                list_price = content.xpath(
                                    '//td[contains(text(),"Typical price:")]//following-sibling::td//span//span//text()').get(
                                    '')
                                if not list_price:
                                    list_price = content.xpath(
                                        '//td[contains(text(),"List Price:")]//following-sibling::td//span//span//text()').get(
                                        '')
                                    if not list_price:
                                        list_price = content.xpath(
                                            '//div[@class="a-box-group"]//div[@id="booksAdditionalPriceInfoContainer"]//span[@id="listPrice"]//text()').get(
                                            '')
            except:
                list_price = ''
            if list_price:
                list_price = list_price.replace('$', '').replace(',', '').strip()
            else:
                list_price = ''

            sellprice = content.xpath(
                '//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="aok-offscreen"]//text()').get('')

            if not sellprice:
                sellprice = content.xpath(
                    '//span[contains(text(),"One-time purchase:")]//ancestor::div[@data-a-accordion-row-name="newAccordionRow"]//div[@data-csa-c-content-id="corePrice"]//span[@class="a-price a-text-price header-price a-size-base a-text-normal a-color-price"]//span//text()').get(
                    '')
            if not sellprice:
                sellprice = content.xpath(
                    """//span[contains(text(),"One-time purchase:")]//ancestor::div[@data-a-accordion-row-name="newAccordionRow"]//div[@data-csa-c-content-id="corePrice"]//span[@class='a-price a-text-price header-price a-size-base a-text-normal']//span//text()""").get(
                    '')
            if not sellprice:
                sellprice = content.xpath(
                    '//td[contains(text(),"Bundle Price:")]//following-sibling::td//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]//text()').get(
                    '')
            if not sellprice:
                sellprice = content.xpath(
                    '//span[contains(@class,"apexPriceToPay")]//span[@class="a-offscreen"]//text()').get(
                    '')
            if not sellprice:
                sellprice = content.xpath(
                    '//span[contains(@class,"priceToPay")]//span[@class="a-offscreen"]//text()').get('')
            if not sellprice:
                sellprice = content.xpath(
                    '//td[contains(text(),"Deal Price:")]//following-sibling::td//span[@class="a-price a-text-price a-size-medium apexPriceToPay"]//text()').get(
                    '')
            if not sellprice:
                sellprice = content.xpath(
                    '//div[@class="a-box-group"]//div[@id="booksHeaderSection"]//span[@id="price"]//text()').get('')
            if not sellprice:
                sellprice = content.xpath(
                    '//div[@data-csa-c-content-id="offer_display_desktop_accordion_header"]//div[@id="corePrice_feature_div"]//span[@class="a-price a-text-price header-price a-size-base a-text-normal"]//span[@class="a-offscreen"]//text()').get(
                    '')
            if sellprice:
                sellprice = sellprice.replace('$', '').replace(',', '').strip()
                import re
                match = re.search(r'([\d.,]+)\s+with', sellprice)
                if match:
                    sellprice = match.group(1)
                else:
                    sellprice = sellprice

            if list_price != '' and sellprice != '':
                list_price = list_price
                sellprice = sellprice

            elif list_price == '' and sellprice != '':
                list_price = sellprice
                sellprice = ''

            elif list_price != '' and sellprice == '':
                list_price = list_price
                sellprice = ''

            try:
                sub_category_loop = content.xpath(
                    '''//div[contains(@id,'breadcrumbs')]//ul//li//span[@class="a-list-item"]//a''')
                text = ''
                main_category = ''
                i = 0
                if sub_category_loop:
                    for sub in sub_category_loop:
                        text = sub.xpath('''.//text()''').get()
                        if i == 0:
                            main_category = text
                            i = 1

                sub_category = text
            except:
                sub_category = ''
                main_category = ''

            try:
                off = content.xpath(
                    '''//div[@data-feature-name="corePriceDisplay_desktop"]//div//span[contains(@class,'savingsPercentage')]//text()''').get()
                if off:
                    off = off.replace('-', '')
            except:
                off = ''

            if off is None:
                off=''


            try:
                best_seller_tag = content.xpath('''//div[@class="zg-bf-badge-wrapper"]//a//span//text()''').get()
                if '#1' in best_seller_tag:
                    best_seller = 'Yes'
                else:
                    best_seller = ''
            except:
                best_seller = ''

            try:
                last_month = content.xpath(
                    '''//div[@id="socialProofingAsinFaceout_feature_div"]//span[contains(@class,'social-proofing-faceout-title')]//span//text()''').get()
            except:
                last_month = ''

            try:
                coupon = content.xpath('''//span[contains(@id,'couponText')]//text()''').get()
                coupon = coupon.replace('Apply', '').replace('coupon', '').strip()
            except:
                coupon = ''

            try:
                limited_deal = content.xpath(
                    '''//div[@id="apex_desktop"]//span[@id="dealBadgeSupportingText"]//span//text()''').get()
                if 'Limited time deal' in limited_deal:
                    limited_time = 'yes'
                else:
                    limited_time = ''
            except:
                limited_time = ''

            try:
                lowest_price = content.xpath('''//div[@class=" delightPricingBadge"]//span//text()''').get()
                if 'Lowest price' in lowest_price:
                    lowest_price = 'Yes'
                else:
                    lowest_price = ''
            except:
                lowest_price = ''

            video = content.xpath('//a[@data-elementid="vse-cards-vw-dp-widget-ingress-carousel-element"]/@href').getall()
            video_tumbnail = content.xpath('//img[@alt="Video Widget Video Title Section"]/@src').getall()

            if video:
                viddd = []
                for vid in video:
                    vi = 'https://www.amazon.com' + str(vid)
                    viddd.append(vi)
                vids = '|'.join(viddd)
            else:
                vids = ''

            if video_tumbnail:
                vts = []
                for vt in video_tumbnail:
                    if "._C" in vt and ".jpg" in vt:
                        cleaned_url = vt.split("._C")[0] + "._PKdp-play-icon-overlay__.jpg"
                        vts.append(cleaned_url)
                    elif "._CR" in vt and ".png" in vt:
                        cleaned_url = vt.split("._CR")[0] + "._PKdp-play-icon-overlay__.png"
                        vts.append(cleaned_url)

                vtss = '|'.join(vts)
            else:
                vtss = ''

            item = {'Product_Url_EN': url2,
                    'Main_Category_EN': main_category1,
                    'Main_Category_EN_Onsite':main_category,
                    'Sub_Category_EN': sub_category,
                    'Product_Name_EN': product_title,
                    'Product_Brand_EN': brand,
                    'Product_Description_EN': product_description,
                    'Amazon_Choice': amazon_choice,
                    'Best Seller': best_seller,
                    'Limited Time Deal': limited_time,
                    'Product Bought Last Month': last_month,
                    'OFF': off,
                    'Coupon': coupon,
                    'lowest price in 30 days': lowest_price,
                    'product_image': new_primary_image,
                    'secondary_image': cleaned_secondary_image,
                    'Video_Link':vids,
                    'Video_Thumbnail':vtss,
                    'asin': asin1,
                    'review_count': total_rating,
                    'avg_rating': avg_rating,
                    'discounted_product_price': sellprice,
                    'product_original_price': list_price,
                    'EN_PDP_pagesave':full_path1}

            pdp_collection.insert_one(item)
            print('inserted................')
            coll.update_one({'_id': ii['_id']}, {'$set': {'status': 'done'}})
            print('status updated..........')
        elif response.status_code==500 or response.status_code==404:
            coll.update_one({'_id': ii['_id']}, {'$set': {'status': 'not_found'}})
            print('not found.................')

if __name__ == '__main__':
    run_count = 0
    while coll.count_documents({'status': 'pending'}) != 0 and run_count < 10:
        total_count = coll.count_documents({'status': 'pending'})
        variable_count = total_count // 40
        if variable_count == 0:
            variable_count = total_count ** 2
        count = 1
        threads = [Thread(target=pdp_data, args=(i, variable_count)) for i in range(0, total_count, variable_count)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        run_count += 1