import datetime
import math


def args_periods(args_period):
    # periods = [args_period]
    periods = []
    if len(args_period) == 8:
        end = datetime.datetime.strptime(args_period, "%Y%m%d")
        start = datetime.datetime.strptime('20210701', "%Y%m%d")
        # print((end - start).days)

        # for i in range((end - start).days):
        for i in range((end - start).days):
            aa = (start + datetime.timedelta(days=i)).strftime("%Y%m%d")
            # print(aa)
            periods.append(aa)
        print(periods)
        return periods
    else:
        num = (int(args_period[:4]) - 2021) * 12 + (int(args_period[-2:]) - 2)
        for i in range(num):
            periods.append(add_month('202103', i))
        return periods


def add_month(datamonth, num):
    """
    月份加减函数,返回字符串类型
    :param datamonth: 时间(201501)
    :param num: 要加(减)的月份数量
    :return: 时间(str)
    """
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    datamonth = int(datamonth)
    num = int(num)
    year = datamonth // 100
    new_list = []
    s = math.ceil(abs(num) / 12)
    for i in range(int(-s), int(s + 1)):
        new_list += [str(year + i) + x for x in months]
    new_list = [int(x) for x in new_list]
    return str(new_list[new_list.index(datamonth) + num])


if __name__ == '__main__':
    args_periods('20210704')
