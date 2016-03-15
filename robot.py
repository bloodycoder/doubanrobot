import requests
import re
import webbrowser
import requests.utils, pickle
import pdb

class doubanrobot(object):
    def __init__(self, username, password, cookie_path):
        self.cookie_path = cookie_path
        self.headers = {
            "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/48.0.2564.116 Safari/537.36"
            }
        self.data = {
            "form_email" : username,
            "form_password" : password,
            "source" : "index_nav",
            "rememberme": "on"        
            }
        self.url = "https://accounts.douban.com/login"
        # pdb.set_trace()
        try:
            self.cookies = self.loadcookies(self.cookie_path)
        except Exception, e:
            self.cookies = {}

        self.session = requests.session()


    def login(self):
        pdb.set_trace()
        res = self.session.get("https://www.douban.com/", headers = self.headers, cookies = self.cookies)
        pdb.set_trace()
        if res.url == "https://www.douban.com/":
            print "login sucessfully"
        else:
            while True:
                res = self.login_withoutcookies()
                if(res.url.encode('utf8') == "https://www.douban.com/"):
                    break
                else:
                    print "wrong var code"
            with open(self.cookie_path, 'w') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
        return res

    def login_withoutcookies(self):
        res = self.session.post(self.url, data = self.data, headers = self.headers)
        html = res.text
        var_code_url = re.compile(r'<img id="captcha_image" src="(.+?)" alt="captcha"').findall(html)
        if var_code_url:
            webbrowser.open(var_code_url[0])
            var_code = raw_input("var_code:")

            var_id = re.compile(r'type="hidden" name="captcha-id" value="(.+?)"/>').findall(html)
            self.data["captcha-solution"] = var_code
            self.data["captcha-id"] = var_id[0]

            res = self.session.post(self.url, data = self.data, headers = self.headers)
            with open('test.html','w') as f:
                f.write(res.text.encode("utf8"))
        
        return res


    def loadcookies(self, cookie_path):
        with open(cookie_path, 'r') as f:
            cookie = pickle.load(f)
            cookies = requests.utils.cookiejar_from_dict(cookie)

        return cookies

if __name__ == '__main__':
    robot = doubanrobot("bucktoothsir@gmail.com", "woshizhu7", "liuruishan.cookie")
    res = robot.login()
    with open("test.html", 'w') as f:
        f.write(res.text.encode('utf8'))
