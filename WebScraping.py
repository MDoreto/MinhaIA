from urllib.request import Request, urlopen  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

req = Request("https://www.google.com/search?sxsrf=ALeKk0296_I1keP5FzujE8gfpon7ZVOW6w%3A1606516401184&ei=sX7BX5zVCsyy5OUP57WnuAc&q=qual+o+pre%C3%A7o+das+a%C3%A7%C3%B5es+da+petrobras&oq=qual+o+pre%C3%A7o+das+a%C3%A7%C3%B5es+da+petrobras&gs_lcp=CgZwc3ktYWIQAzIMCCMQJxCdAhBGEPoBMgIIADIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46BAgAEEdQtpUBWOmkAWDFpQFoAHACeACAAYAFiAH-E5IBCTAuNC41LjUtMZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjc8av746PtAhVMGbkGHefaCXcQ4dUDCA0&uact=5", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'})
response = urlopen(req).read()
soup = BeautifulSoup(response, "html.parser")
resp = soup.find_all('span', class_="IsqQVc NprOob XcVN5d")
temp = resp[0].get_text()
resp = soup.find_all('span', class_="WlRRw IsqQVc fw-price-dn")
#resp = soup.find_all('span', jsname="rfaVEf")
print( resp.find("div"["aria-label"] ))

