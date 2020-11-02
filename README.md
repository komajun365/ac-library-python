# ac-library-python
仲間内で進める、ac-libraryのpython版を作ろうプロジェクトです。
https://github.com/atcoder/ac-library

まだ何も決まっていませんが、
良いものができたらだれでも使っていただいて良いんじゃないか、とは思っています。
（ライセンス的なものは要確認）

<br>

- ## pull requestまでの流れ
1. branchを切る。  
  `feature/hoge`

2. 単体テストのテストコードを作成する。  
  C++で書かれた公式のACLを参考にする。  
  書き方はpytestのお作法に準拠。  
  ディレクトリは下記の通り。  
  root/  
  &ensp;└ tests/  
  &ensp;&ensp;└ test_hoge.py  
  test_hoge.py内では手順3で作成するatcoder/hoge.pyからオブジェクトをインポートすることになるが、インポートの書き方は下記の通り。
    1. \_\_init\_\_.py内でオブジェクトをインポート。
    ```python
    from atcoder.hoge import Hoge # 追記
      
    __all__ = ['Hoge'] # リストに追加
    ```
    2. test_hoge.py内でオブジェクトをインポート。
    ```python
    from atcoder import Hoge
      
    h = Hoge(*args, **kwargs)
    ```

3. 本体を作成する。  
  こちらも公式のACLを参考に。  
  ディレクトリは下記の通り。  
  root/  
  &ensp;└ atcoder/  
  &ensp;&ensp;└ hoge.py  

4. テストを実行する。  
  pull requestを実行すると、テストが走る。  
  テストの内容はflake8によるコードレビューと、手順2で作成した単体テスト。  
  テストを実施したい場合は"WIP"と付けてpull requestを実行する。  
  テストが全て通ったのを確認した段階で"WIP"を外す。