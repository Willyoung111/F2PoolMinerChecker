# -*- coding: UTF-8 -*-
import pymysql
import  datetime

user = input("mysql username:")
passwd = input("mysql passwd:")
conn = pymysql.connect(user=user, passwd=passwd, db="MinerLog")
cursor = conn.cursor()


begin = datetime.date(2021, 5, 14)
end = datetime.date.today()

payout_filename = "ETH-" + str(begin) + "-" + str(end) + ".txt"
print(payout_filename)

payout = {}
payoutsum = 0
with open(payout_filename, 'rb') as fp:
    while True:
        lines = fp.readline()
        if not lines:
            break
        lines = str(lines)
        info = lines.split("\\t")
        td = info[0][2:]
        income = float(info[3])
        payout[td] = income
        print(td, "\t", income)
        payoutsum += income

print(begin, "至", end, "总收益：", payoutsum)
print("###############")


minerIncome = {}
for i in range((end - begin).days + 1):
    day = str(begin + datetime.timedelta(days=i))
    cursor.execute("SELECT * FROM powerlog WHERE date = %s", day)

    minerDayPower = {}
    minerDayPowerPecent = {}
    power_day_sum = 0
    while 1:
        res = cursor.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        minerName = res[2]
        power = float(res[3])
        # if minerName in minerList:
        #     minerList[minerName] = minerList[minerName] + float(power)
        # else:
        #     minerList[minerName] = power
        minerDayPower[minerName] = power
        power_day_sum += power
        # print("date ", day, " mineName:", minerName, " Power:", power)
    
    for minerName, power in minerDayPower.items():
        minerDayPowerPecent[minerName] = power / power_day_sum

        if minerName in minerIncome:
            minerIncome[minerName] = minerIncome[minerName] + minerDayPowerPecent[minerName] * payout[day] 
        else:
            minerIncome[minerName] = minerDayPowerPecent[minerName] * payout[day] 

    print(day, "收益:", payout[day] , "占比： ")
    for name, percent in minerDayPowerPecent.items():
        print(name[:3], "\t", percent)

    print()

for name, income in minerIncome.items():
    print(name[:3], "\t\t", str(income)[:7], "ETH")
# print(minerList)

# minerPercent = {}
# sumPower = 0
# for name, power in minerList.items():
#     sumPower += power
# print(sumPower)
# for name, power in minerList.items():
#     percent = power / sumPower
#     minerPercent[name] = percent
#     print(name, "\t", percent)
cursor.close()
conn.close()
