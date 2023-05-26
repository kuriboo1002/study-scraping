from tail_recursive import tail_recursive
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


@tail_recursive
def getlinks(url, exclude_path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # タイトルが取れない場合はHTMLじゃないと判断
    if soup.title is None:
        return
    title = soup.title.string
    print(title)
    print(url)

    # URLを辞書に追加ç
    url_dict[url] = title
    # print(url_dict)

    links = soup.find_all('a')
    for link in links:
        get_url = link.get('href')

        # リンクがなければ終了
        if get_url is None:
            continue

        # init_urlのドメインじゃなかったら無視
        if not get_url.startswith(init_url):
            if not get_url.startswith('/'):
                continue

        # exclude_pathを含んでいたら除外
        if exclude_path != '':
            if get_url.find(exclude_path) != -1:
                continue

        # 相対パスを絶対パスに修正
        # TODO: ドメインとサブディレクトリのところの/がおかしくなる部分がある。後々修正。
        if get_url.find(domain) == -1:
            get_url = domain + get_url

        # 既に一度訪れているURLは無視
        if get_url in url_dict.keys():
            continue

        # 再起処理にしているためスタックオーバーフローする可能性が高い。
        return getlinks(get_url, exclude_path)


init_url = '<URL>'
domain = url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(init_url))
exclude_path = ''
url_dict = {}
getlinks(init_url, exclude_path)
print(url_dict)
