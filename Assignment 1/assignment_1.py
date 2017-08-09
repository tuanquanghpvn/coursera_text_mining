# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010


import pandas as pd
import datetime


doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)


def convert_year(year):
    if len(year) == 2:
        if int(year) < 10:
            year = "20{}".format(year)
        else:
            year = "19{}".format(year)
    return year


def convert_month(month):
    return month if len(month) == 2 else "0{}".format(month)


def convert_day(day):
    return day if len(day) == 2 else "0{}".format(day)


def convert_time(time_str):
    if len(time_str) == 4:
        day = "01"
        month = "01"
        year = time_str
    else:
        for c in ["/", "-"]:
            if c in time_str:
                parts = time_str.split(c)
                if len(parts) == 2:
                    day = "01"
                    month = convert_month(parts[0])
                    year = convert_year(parts[1])
                elif len(parts) == 3:
                    day = convert_day(parts[1])
                    month = convert_month(parts[0])
                    year = convert_year(parts[2])
    return "{}/{}/{}".format(year, day, month)


def get_time_format_by_string():
    result = []
    regex_patterns = [
        r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?:[a-z]*)?(?:[\.,\,,\-])? (?:\d{1,2}(?:st|nd|th)?(?:[\,,\-])? )?\d{4}',
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(?:\d{1,2})-\d{4}',
        r'(?:\d{1,2}[/-])?(?:\d{1,2}[/-])\d{2,4}',
        r'\d{4}'
    ]

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    idxs = []

    for pattern_index, pattern in enumerate(regex_patterns):
        for idx, match in enumerate(df.str.findall(pattern)):
            if match:
                time_str = match[0].strip()
                # print("Pattern Index: ", pattern_index)
                # print("Idx: ", idx)
                # print("Truoc: ", time_str)
                if pattern_index == 0 or pattern_index == 1:
                    time_str = time_str.replace('-', ' ')
                    time_str = ''.join([w for w in time_str if w not in ['th', 'st', 'nd', '.', ',']])
                    list_time = [w if w.isdigit() else months.index(w[0:3]) for w in time_str.split(' ')]
                    if len(list_time) > 2:
                        if isinstance(list_time[0], int):
                            month = list_time[0] + 1
                            month = month if month > 9 else "0{}".format(month)
                            time_str = '{0}/{1}/{2}'.format(list_time[2], list_time[1], month)
                        else:
                            month = list_time[1] + 1
                            month = month if month > 9 else "0{}".format(month)
                            time_str = '{0}/{1}/{2}'.format(list_time[2], list_time[0], month)
                    else:
                        month = list_time[0] + 1
                        month = month if month > 9 else "0{}".format(month)
                        time_str = '{0}/01/{1}'.format(list_time[1], month)

                    if idx not in idxs:
                        # print("Sau: ", time_str)
                        # print("\n")
                        result.append((idx, time_str))
                        idxs.append(idx)
                elif pattern_index == 2:
                    time_str = convert_time(time_str)
                    if idx not in idxs:
                        # print("Sau: ", time_str)
                        # print("\n")
                        result.append((idx, time_str))
                        idxs.append(idx)
                elif pattern_index == 3:
                    # print("Pattern Index: ", pattern_index)
                    # print("Idx: ", idx)
                    # print("Truoc: ", time_str)
                    time_int = int(time_str)
                    if idx not in idxs and time_int >= 1900 and time_int <= 2020:
                        time_str = convert_time(time_str)
                        # print("Sau: ", time_str)
                        # print("\n")
                        result.append((idx, time_str))
                        idxs.append(idx)
    return result


def date_sorter():
    sorted_date = sorted(get_time_format_by_string(), key=lambda x: datetime.datetime.strptime(x[1], '%Y/%d/%m'))
    # print("Len: ", len(sorted_date))
    # for index, dt in enumerate(sorted_date):
    #     print("Date: {} - Idx: {}".format(dt[1], index))

    idxs = [idx for idx, _ in sorted_date]
    result = pd.Series(idxs)
    return result

print(date_sorter())


