from tools import log
import config
import request
import setting

def login():
    if (config.mihoyobbs_Cookies == ''):
        log.error("请填入Cookies!")
        config.Clear_cookies()
        exit(1)
    temp_Cookies = {}
    if "login_ticket" in config.mihoyobbs_Cookies:
        temp_Cookies = config.mihoyobbs_Cookies.split(";")
        for i in temp_Cookies:
            if i.split("=")[0] == " login_ticket":
                config.mihoyobbs_Login_ticket = i.split("=")[1]
                break
        data = request.get(url=setting.bbs_Cookieurl.format(config.mihoyobbs_Login_ticket))
        if "成功" in data["data"]["msg"]:
            config.mihoyobbs_Stuid = str(data["data"]["cookie_info"]["account_id"])
            data = request.get(url=setting.bbs_Cookieurl2.format(config.mihoyobbs_Login_ticket, config.mihoyobbs_Stuid))
            config.mihoyobbs_Stoken = data["data"]["list"][0]["token"]
            log.info("登录成功！")
            log.info("正在保存Config！")
            config.Save_config()
        else:
            log.error("cookie已失效,请重新登录米游社抓取cookie")
            config.Clear_cookies()
            exit(1)
    else:
        log.error("cookie中没有'login_ticket'字段,请重新登录米游社，重新抓取cookie!")
        config.Clear_cookies()
        exit(1)