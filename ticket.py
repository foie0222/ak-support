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
    ticket_list.extend(make_umaren_ticket(yumachan, odds_manager.umaren_odds_list, target_refund))
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


# 馬連購入
def make_umaren_ticket(yumachan, umaren_odds_list, target_refund):
    umaren_ticket_list = []
    for i, horse1 in enumerate(yumachan.horse_list):
        for horse2 in yumachan.horse_list[i + 1:]:
            pair_num = make_pair_num(horse1.umano, horse2.umano)

            odds = [umaren_odds for umaren_odds in umaren_odds_list if umaren_odds.umano == pair_num][0].odds
            probability = get_umaren_probability(horse1.probability, horse2.probability)
            expected_value = probability * odds
            if expected_value >= 2:
                bet = calc_bet(odds, target_refund)
            else:
                continue

            ticket = Ticket(
                yumachan,
                'UMAREN',
                pair_num,
                bet,
                expected_value,
                probability,
                odds)
            umaren_ticket_list.append(ticket)

    sorted_umaren_ticket_list = sorted(umaren_ticket_list, key=lambda t: t.number)
    return sorted_umaren_ticket_list


# 単勝の期待値を計算する
def get_tan_probability(probability):
    return probability / 100


# 馬連の期待値を計算する
def get_umaren_probability(probability1, probability2):
    _1_2_probability = probability1 * (probability2 / (100 - probability1))
    _2_1_probability = probability2 * (probability1 / (100 - probability2))
    total_probability = _1_2_probability + _2_1_probability
    return total_probability / 100


# 指定した払い戻し額に届くように購入金額を計算する
def calc_bet(odds, target_refund):
    bet = 100
    while target_refund > odds * bet:
        bet += 100
    return bet


def make_pair_num(umano1, umano2):
    uma1 = int(umano1)
    uma2 = int(umano2)
    if uma1 < uma2:
        return umano1 + '-' + umano2
    return umano2 + '-' + umano1


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
