from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


class scraping():

    def __init__(self, init_url, exclude_path):
        self.exclude_path = exclude_path
        self.domain = '{uri.scheme}://{uri.netloc}'.format(
            uri=urlparse(init_url))
        self.url_dict = {}
        self.url_dict[init_url] = 'no title'

    def doScraping(self):
        index = -1
        while True:
            index += 1
            # dic -> list
            linklist = list(self.url_dict)

            # 無限ループの終了条件
            # listよりindexのほうが大きければ終了
            if len(linklist) == index:
                break

            response = requests.get(linklist[index])
            bs = BeautifulSoup(response.text, 'html.parser')

            # タイトルが取れない場合はHTMLじゃないと判断
            if bs.title is None:
                continue

            title = bs.title.string
            # print(title)
            # print(linklist[index])

            # URLしかないdicにタイトルを追加
            self.url_dict[linklist[index]] = title

            links = bs.find_all('a')

            # 以下ループで対象のページ内で取得できたaタグを解析
            for link in links:
                get_url = link.get('href')

                # リンクがなければ次へ
                if get_url is None:
                    continue

                # init_urlのドメインじゃなかったら無視して次へ
                # ただし、相対パスの場合は許可
                if not get_url.startswith(self.domain):
                    if not get_url.startswith('/'):
                        continue

                # exclude_pathを含んでいたら除外して次へ
                if self.exclude_path != '':
                    if get_url.find(self.exclude_path) != -1:
                        continue

                # 相対パスを絶対パスに修正
                # TODO: ドメインとサブディレクトリのところの/がおかしくなる部分がある。後々修正。
                if not get_url.startswith(self.domain):
                    get_url = self.domain + get_url

                # 既に一度チェックしているURLは無視して次へ
                if get_url in self.url_dict.keys():
                    continue

                # 上記の複数除外条件をすり抜けたものを辞書に追加する
                self.url_dict[get_url] = 'no title'

    # url_dictのgetter
    def getUrlDict(self):
        return self.url_dict


init_url = '<URL>'
exclude_path = ''
instance = scraping(init_url, exclude_path)
instance.doScraping()
print(instance.getUrlDict())
