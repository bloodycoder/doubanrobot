# coding=utf-8
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
        self.url = "https://www.douban.com/"
        # pdb.set_trace()
        try:
            self.cookies = self.loadcookies(self.cookie_path)
        except Exception, e:
            self.cookies = {}

        self.session = requests.session()

    def login(self):
        self.session.cookies.update(self.cookies)
        res = self.session.get(self.url + "mine", headers = self.headers)
        pdb.set_trace()
        if res.url == self.url + "people/uid/":
            print "login sucessfully"
        else:
            while True:
                res = self.login_withoutcookies()
                if(res.url == self.url):
                    print "login sucessfully"
                    break
                else:
                    print "wrong var code"
            with open(self.cookie_path, 'w') as f:
                pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)
        self.ck = self.get_ck(res)
        return res

    def login_withoutcookies(self):
        res = self.session.post(self.url + "login", data = self.data, headers = self.headers)
        html = res.text
        var_code_url = re.compile(r'<img id="captcha_image" src="(.+?)" alt="captcha"').findall(html)
        if var_code_url:
            webbrowser.open(var_code_url[0])
            var_code = raw_input("var_code:")
            var_id = re.compile(r'type="hidden" name="captcha-id" value="(.+?)"/>').findall(html)

            self.data["captcha-solution"] = var_code
            self.data["captcha-id"] = var_id[0]

            res = self.session.post(self.url, data = self.data, headers = self.headers)
        
        return res


    def loadcookies(self, cookie_path):
        with open(cookie_path, 'r') as f:
            cookie = pickle.load(f)
            cookies = requests.utils.cookiejar_from_dict(cookie)
        return cookies
   
    def get_ck(self, res):
        ck = re.compile(r'source=main&amp;ck=(.+?)">').findall(res.text)
        return ck

    def report(self):
        pdb.set_trace()
        postdata = {
            'ck': self.ck,
            'comment': 'commnet'
        }
        return self.session.post(self.url, data = postdata)

    def sofa(self, group_id, comment):
        group_url = self.url + "group/" + group_id
        html = self.session.get(group_url).text()
        topics = re.findall(r'topic/(\d+?)/.*?class="">.*?<td nowrap="nowrap" class="">(.*?)</td>',
                html, re.DOTALL)
        return topics

    def add_comment(self,topic_id, comment):
        post_data = {
            'ck': self.ck,
            'rv_comment': comment,
            'start': '0',
            'submit_btn': '加上去'
        }
        pdb.set_trace()
        self.session.post(self.url + "group/topic/" + str(topic_id) + "/add_comment", 
                          data = post_data)


    def sofa(self, group_id, comment):
        group_url = self.url + "group/"  + group_id
        html = self.session.get(group_url).text
        topics = re.findall(r'topic/(\d+?)/.*?class="">.*?<td nowrap="nowrap" class="">(.*?)</td>',
                html, re.DOTALL)
        for topic in topics:
          if topic[1] == '0':
                add_commet(topic_id[0], comment)


if __name__ == '__main__':
    robot = doubanrobot("username@gmail.com", "password", "cookie_path")
    res = robot.login()
    res=robot.report()

