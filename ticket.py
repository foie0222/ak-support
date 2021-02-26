import os


class Ticket:
    def __init__(self, yumachan, denomination, number, bet_price, expected_value, probability, odds):
        self.yumachan = yumachan
        self.denomination = denomination
        self.method = 'NORMAL'
        self.multi = ''
        self.number = number
        self.bet_price = bet_price
        self.expected_value = expected_value
        self.probability = probability
        self.odds = odds

    def to_string(self):
        return f'Ticket=[opdt={self.yumachan.opdt}, course={self.yumachan.race_course.name}, denomination={self.denomination}, number={self.number}, bet_price={self.bet_price}, expected_value={round(self.expected_value, 2)}, probability={round(self.probability * 100, 2)}%, odds={self.odds}]'

    def to_csv(self):
        return '{},{},{},{},{},{},{},{}'.format(
            self.yumachan.opdt,
            self.yumachan.race_course.roman,
            self.yumachan.rno,
            self.denomination,
            self.method,
            self.multi,
            self.number,
            self.bet_price)


def make_ticket(yumachan, odds_manager, target_refund):
    print('買い目を作成中...')
    ticket_list = []
    ticket_list.extend(make_tan_ticket(yumachan, odds_manager.tan_odds_list, target_refund))
    return ticket_list


# 単勝購入
def make_tan_ticket(yumachan, tan_odds_list, target_refund):
    tan_ticket_list = []
    for horse in yumachan.horse_list:
        odds = [tan_odds for tan_odds in tan_odds_list if tan_odds.umano == horse.umano][0].odds
        probability = get_tan_probability(horse.probability)
        expected_value = probability * odds
        if expected_value >= 2:
            bet = calc_bet(odds, target_refund)
        else:
            continue

        ticket = Ticket(
            yumachan,
            'TANSYO',
            horse.umano,
            bet,
            expected_value,
            probability,
            odds)
        tan_ticket_list.append(ticket)

    sorted_tan_ticket_list = sorted(tan_ticket_list, key=lambda t: t.number)
    return sorted_tan_ticket_list


# ex)3%の期待値を0.03と返す
def get_tan_probability(probability):
    return probability / 100


# 指定した払い戻し額に届くように購入金額を計算する
def calc_bet(odds, target_refund):
    bet = 100
    while target_refund > odds * bet:
        bet += 100
    return bet


# 投票用のcsv出力
def make_csv(ticket_list, timestamp):
    make_tickets_dir()
    with open('./tickets/ticket_' + timestamp + '.csv', 'w') as f:
        for ticket in ticket_list:
            f.write(ticket.to_csv() + '\n')


# ticketsフォルダがなかったら作成する
def make_tickets_dir():
    if not os.path.isdir('./tickets'):
        os.mkdir('./tickets')
    else:
        pass
