# venvの利用
source ../bin/activate.fish

# pip3の更新とパッケージのインストール
python3.9 -m pip install --upgrade pip

pip3 install beautifulsoup4 requests

# requirements.txtの作成
pip3 freeze > requirements.txt

# requirements.txtからのインストール
pip3 install -r requirements.txt