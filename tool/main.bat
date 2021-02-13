chcp 65001

@ECHO OFF

SETLOCAL EnableDelayedExpansion

ECHO ======================================================================
ECHO ◇ak-support - 実行モード選択 -
ECHO ======================================================================
ECHO [0] ゆまちゃんデータとオッズの両方
ECHO [1] オッズデータのみ
ECHO:

SET /P MODE="実行モードを選択してください＞"
ECHO:

IF %MODE% == 0 (
    cd ..
    python main.py main
)
IF %MODE% == 1 (
    SET /P OPDT="日付を選択してください（例：20210214）＞"
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

    SET /P COURSE="会場コード＞"
    SET /P RNO="レースNOを入力してください（例：11）＞"

    cd ..
    python main.py odds_only !OPDT! !COURSE! !RNO!
)

PAUSE