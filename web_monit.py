import requests
from smtplib import SMTP


class WebMonitor:
    def __init__(self, domain_name: str, search_string: str):
        self.domain_name = domain_name
        self.search_string = search_string
        self.link = requests.get(f'{self.domain_name}')

    @staticmethod
    def email_alert(msg: str):
        fromaddr = '<from address>'  # edit here
        toaddrs = '<to address>'  # edit here
        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login('<your email>', '<your password>')  # edit here
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()

    @staticmethod
    def get_status(req):
        return req.status_code

    def check_internet_access(self):
        if self.get_status(requests.get('https://google.com')) == 200:
            return True
        self.email_alert('no internet access')

    def get_content(self):
        return self.link.text

    def main_check(self):
        if self.check_internet_access():
            if self.get_status(self.link) == 200:
                if self.search_string in self.get_content():
                    return True
                self.email_alert(f'{self.domain_name} content changed!')
            else:
                self.email_alert(f'{self.domain_name} website is down!')


web_monit = WebMonitor('https://domain_name.com', 'search_string')

