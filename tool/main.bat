chcp 65001

@ECHO OFF

SETLOCAL EnableDelayedExpansion

ECHO ======================================================================
ECHO ◇ak-support - 実行モード選択 -
ECHO ======================================================================
ECHO [0] 自動投票モード

ECHO [1] オッズデータのみ
ECHO [2] ゆまちゃんデータのみ（先にオッズデータを取得しておく必要があります）
ECHO:

SET /P MODE="実行モードを選択してください＞"
ECHO:

IF %MODE% == 0 (
    SET /P REFUND="最低払い戻し額を入力してください＞"
    cd ..
    python main.py main !REFUND!
)
IF %MODE% == 1 (
    SET /P OPDT="日付を選択してください（例：20210214）＞"
    ECHO:
    ECHO 会場コードを選択してください
    ECHO [1]札幌
    ECHO [2]函館
    ECHO [3]福島
    ECHO [4]新潟
    ECHO [5]東京
    ECHO [6]中山
    ECHO [7]中京
    ECHO [8]京都
    ECHO [9]阪神
    ECHO [10]小倉
    ECHO:

    SET /P COURSE="会場コード＞"
    SET /P RNO="レースNOを入力してください（例：11）＞"

    cd ..
    python main.py odds_only !OPDT! !COURSE! !RNO!
)
IF %MODE% == 2 (
    cd ..
    python main.py yuma_only
)

PAUSE