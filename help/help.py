from database import db_sqlite as db


def average_temp():
    """
    this func solves average temperature from all devices and after tells us, can we use the fork or not
    :return: True or False (can use or not)
    """
    database = db.DataBase(False)
    if database.get_extreme()[0]:
        return True
    user_params = database.get_user_params()
    t = user_params[1]
    all_temperature = database.get_all_temperature()
    sum_of_temperatures = 0
    for i in range(0, len(all_temperature)):
        sum_of_temperatures += all_temperature[i][0]
    average_t = sum_of_temperatures / len(all_temperature)
    return average_t > t


def average_hum():
    """
    this func solves average humanity from all devices and after tells us, can we use the hum_sys or not
    :return: True of False (can we use or not)
    """
    database = db.DataBase(False)
    if database.get_extreme()[0]:
        return True
    user_params = database.get_user_params()
    h = user_params[2]
    all_humanity = database.get_all_humanity()
    sum_of_hums = 0
    for i in range(0, len(all_humanity)):
        sum_of_hums += all_humanity[i][0]
    average_t = sum_of_hums / len(all_humanity)
    return average_t > h


def average_hb(num):
    """
    this func solves average humanity from one device and after tells us, can we use the hb_sys or not
    :param num: the num of the device
    :return: can we use or not (True or False)
    """
    database = db.DataBase(False)
    if database.get_extreme()[0]:
        return True
    user_params = database.get_user_params()
    hb = user_params[3]
    all_hb = database.get_all_hb_in_one(num)
    sum_of_hums = 0
    for i in range(0, len(all_hb)):
        sum_of_hums += all_hb[i][0]
    aver_hb = sum_of_hums / len(all_hb)
    return aver_hb < hb
