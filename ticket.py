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
        return f'Ticket=[opdt={self.yumachan.opdt}, course={self.yumachan.race_course.name}, rno={self.yumachan.rno}, denomination={self.denomination}, number={self.number}, bet_price={self.bet_price}, expected_value={round(self.expected_value, 2)}, probability={round(self.probability * 100, 2)}%, odds={self.odds}]'

    def to_csv(self):
        return '{},{},{},{},{},{},{},{}'.format(
            self.yumachan.opdt,
            self.yumachan.race_course.roman,
            int(self.yumachan.rno),
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
    ticket_list.extend(make_wide_ticket(yumachan, odds_manager.wide_min_odds_list, target_refund))
    ticket_list.extend(make_umatan_ticket(yumachan, odds_manager.umatan_odds_list, target_refund))
    ticket_list.extend(make_trio_ticket(yumachan, odds_manager.trio_odds_list, target_refund))
    ticket_list.extend(make_trifecta_ticket(yumachan, odds_manager.trifecta_odds_list, target_refund))
    return ticket_list


# 単勝購入
def make_tan_ticket(yumachan, tan_odds_list, target_refund):
    tan_ticket_list = []
    for horse in yumachan.horse_list:
        odds = [tan_odds for tan_odds in tan_odds_list if tan_odds.umano == horse.umano][0].odds
        probability = get_tan_probability(horse.probability)
        expected_value = probability * odds
        if 2 <= expected_value < 2.5:
            bet = calc_bet(odds, target_refund)
        elif 2.5 <= expected_value < 3:
            bet = calc_bet(odds, target_refund * 1.3)
        elif 3 <= expected_value < 4:
            bet = calc_bet(odds, target_refund * 1.5)
        elif 4 <= expected_value < 6:
            bet = calc_bet(odds, target_refund * 1.8)
        elif 6 <= expected_value:
            bet = calc_bet(odds, target_refund * 2)
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

            odds_list = [umaren_odds for umaren_odds in umaren_odds_list if umaren_odds.umano == pair_num]
            if not odds_list:
                continue
            odds = odds_list[0].odds
            probability = get_umaren_probability(horse1.probability, horse2.probability)
            expected_value = probability * odds
            if 2 <= expected_value < 2.5:
                bet = calc_bet(odds, target_refund)
            elif 2.5 <= expected_value < 3:
                bet = calc_bet(odds, target_refund * 1.3)
            elif 3 <= expected_value < 4:
                bet = calc_bet(odds, target_refund * 1.5)
            elif 4 <= expected_value < 6:
                bet = calc_bet(odds, target_refund * 1.8)
            elif 6 <= expected_value:
                bet = calc_bet(odds, target_refund * 2)
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


# ワイド購入
def make_wide_ticket(yumachan, wide_min_odds_list, target_refund):
    wide_ticket_list = []
    for i, horse1 in enumerate(yumachan.horse_list):
        for horse2 in yumachan.horse_list[i + 1:]:
            pair_num = make_pair_num(horse1.umano, horse2.umano)

            odds_list = [wide_min_odds for wide_min_odds in wide_min_odds_list if wide_min_odds.umano == pair_num]
            if not odds_list:
                continue
            odds = odds_list[0].odds
            probability = get_wide_probability(horse1, horse2, yumachan.horse_list)
            expected_value = probability * odds
            if 2 <= expected_value < 2.5:
                bet = calc_bet(odds, target_refund)
            elif 2.5 <= expected_value < 3:
                bet = calc_bet(odds, target_refund * 1.3)
            elif 3 <= expected_value < 4:
                bet = calc_bet(odds, target_refund * 1.5)
            elif 4 <= expected_value < 6:
                bet = calc_bet(odds, target_refund * 1.8)
            elif 6 <= expected_value:
                bet = calc_bet(odds, target_refund * 2)
            else:
                continue

            ticket = Ticket(
                yumachan,
                'WIDE',
                pair_num,
                bet,
                expected_value,
                probability,
                odds)
            wide_ticket_list.append(ticket)

    sorted_umaren_ticket_list = sorted(wide_ticket_list, key=lambda t: t.number)
    return sorted_umaren_ticket_list


# 馬単購入
def make_umatan_ticket(yumachan, umatan_odds_list, target_refund):
    umatan_ticket_list = []
    for horse1 in yumachan.horse_list:
        for horse2 in yumachan.horse_list:
            if horse1.umano == horse2.umano:
                continue
            pair_num = horse1.umano + '-' + horse2.umano
            odds_list = [umatan_odds for umatan_odds in umatan_odds_list if umatan_odds.umano == pair_num]
            if not odds_list:
                continue
            odds = odds_list[0].odds
            probability = get_umatan_probability(horse1.probability, horse2.probability)
            expected_value = probability * odds
            if 2 <= expected_value < 2.5:
                bet = calc_bet(odds, target_refund)
            elif 2.5 <= expected_value < 3:
                bet = calc_bet(odds, target_refund * 1.3)
            elif 3 <= expected_value < 4:
                bet = calc_bet(odds, target_refund * 1.5)
            elif 4 <= expected_value < 6:
                bet = calc_bet(odds, target_refund * 1.8)
            elif 6 <= expected_value:
                bet = calc_bet(odds, target_refund * 2)
            else:
                continue

            ticket = Ticket(
                yumachan,
                'UMATAN',
                pair_num,
                bet,
                expected_value,
                probability,
                odds)
            umatan_ticket_list.append(ticket)

    sorted_umatan_ticket_list = sorted(umatan_ticket_list, key=lambda t: t.number)
    return sorted_umatan_ticket_list


# 3連複購入
def make_trio_ticket(yumachan, trio_odds_list, target_refund):
    trio_ticket_list = []
    for i, horse1 in enumerate(yumachan.horse_list):
        for k, horse2 in enumerate(yumachan.horse_list[i + 1:]):
            for horse3 in yumachan.horse_list[i + k + 2:]:
                trio_num = make_trio_num(horse1.umano, horse2.umano, horse3.umano)

                odds_list = [trio_odds for trio_odds in trio_odds_list if trio_odds.umano == trio_num]
                if not odds_list:
                    continue
                odds = odds_list[0].odds
                probability = get_trio_probability(horse1.probability, horse2.probability, horse3.probability)
                expected_value = probability * odds
                if 2 <= expected_value < 2.5:
                    bet = calc_bet(odds, target_refund)
                elif 2.5 <= expected_value < 3:
                    bet = calc_bet(odds, target_refund * 1.3)
                elif 3 <= expected_value < 4:
                    bet = calc_bet(odds, target_refund * 1.5)
                elif 4 <= expected_value < 6:
                    bet = calc_bet(odds, target_refund * 1.8)
                elif 6 <= expected_value:
                    bet = calc_bet(odds, target_refund * 2)
                else:
                    continue

                ticket = Ticket(
                    yumachan,
                    'SANRENPUKU',
                    trio_num,
                    bet,
                    expected_value,
                    probability,
                    odds)
                trio_ticket_list.append(ticket)

    sorted_trio_ticket_list = sorted(trio_ticket_list, key=lambda t: t.number)
    return sorted_trio_ticket_list


# 3連単購入
def make_trifecta_ticket(yumachan, trifecta_odds_list, target_refund):
    trifecta_ticket_list = []
    for i, horse1 in enumerate(yumachan.horse_list):
        for k, horse2 in enumerate(yumachan.horse_list):
            for horse3 in yumachan.horse_list:
                if horse1.umano == horse2.umano or horse1.umano == horse3.umano or horse2.umano == horse3.umano:
                    continue
                trifecta_num = horse1.umano + '-' + horse2.umano + '-' + horse3.umano

                odds_list = [trifecta_odds for trifecta_odds in trifecta_odds_list if trifecta_odds.umano == trifecta_num]
                if not odds_list:
                    continue
                odds = odds_list[0].odds
                probability = get_trifecta_probability(horse1.probability, horse2.probability, horse3.probability)
                expected_value = probability * odds
                if 2 <= expected_value < 2.5:
                    bet = calc_bet(odds, target_refund)
                elif 2.5 <= expected_value < 3:
                    bet = calc_bet(odds, target_refund * 1.3)
                elif 3 <= expected_value < 4:
                    bet = calc_bet(odds, target_refund * 1.5)
                elif 4 <= expected_value < 6:
                    bet = calc_bet(odds, target_refund * 1.8)
                elif 6 <= expected_value:
                    bet = calc_bet(odds, target_refund * 2)
                else:
                    continue

                ticket = Ticket(
                    yumachan,
                    'SANRENTAN',
                    trifecta_num,
                    bet,
                    expected_value,
                    probability,
                    odds)
                trifecta_ticket_list.append(ticket)

    sorted_trifecta_ticket_list = sorted(trifecta_ticket_list, key=lambda t: t.number)
    return sorted_trifecta_ticket_list


# 単勝の確率を計算する
def get_tan_probability(probability):
    return probability / 100


# 馬単の確率を計算する
def get_umatan_probability(probability1, probability2):
    _1_2_probability = probability1 * (probability2 / (100 - probability1))
    return _1_2_probability / 100


# 馬連の確率を計算する
def get_umaren_probability(probability1, probability2):
    _1_2_probability = get_umatan_probability(probability1, probability2)
    _2_1_probability = get_umatan_probability(probability2, probability1)
    total_probability = _1_2_probability + _2_1_probability
    return total_probability


# ワイドの確率を計算する
def get_wide_probability(horse1, horse2, horse_list):
    total_probability = 0
    for horse in horse_list:
        if horse.umano in [horse1.umano, horse2.umano]:
            continue
        total_probability += get_trio_probability(horse1.probability, horse2.probability, horse.probability)
    return total_probability


# 3連複の確率を計算する
def get_trio_probability(probability1, probability2, probability3):
    trio_probability = probability1 * probability2 / (100 - probability1) * probability3 / ((100 - probability1 - probability2)) \
        +probability1 * probability3 / (100 - probability1) * probability2 / ((100 - probability1 - probability3)) \
        +probability2 * probability1 / (100 - probability2) * probability3 / ((100 - probability2 - probability1)) \
        +probability2 * probability3 / (100 - probability2) * probability1 / ((100 - probability2 - probability3)) \
        +probability3 * probability1 / (100 - probability3) * probability2 / ((100 - probability3 - probability1)) \
        +probability3 * probability2 / (100 - probability3) * probability1 / ((100 - probability3 - probability2))
    return trio_probability / 100


# 3連単の確率を計算する
def get_trifecta_probability(probability1, probability2, probability3):
    trio_probability = probability1 * probability2 / (100 - probability1) * probability3 / (100 - probability1 - probability2)
    return trio_probability / 100


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


def make_trio_num(umano1, umano2, umano3):
    x = [int(umano1), int(umano2), int(umano3)]
    sorted_x = sorted(x)
    return str(sorted_x[0]).zfill(2) + '-' + str(sorted_x[1]).zfill(2) + '-' + str(sorted_x[2]).zfill(2)


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
