import sqlite3 as sql

class DataBase:
    """
    This is class for working with sqlite3
    """
    conn = None  # this is variable for a connection to sqlite3
    c = None  # this is the cursor for an execution operations to sqlite3

    def __init__(self, dropping_tables):
        """
        Initialization of cursor a connection to db
        and creating all needed tables
        :param: dropping_tables - if we want drop all data (for testing)
        """
        self.conn = sql.connect('data.db')
        self.c = self.conn.cursor()

        if dropping_tables:  # if we want drop all data (for testing)
            self.c.execute("""drop table if exists `params`""")
            self.c.execute("""drop table if exists `states`""")
            self.c.execute("""drop table if exists `devices_data`""")
            self.c.execute("""drop table if exists `ground_humanity`""")

            # create a table with user parameters
            self.c.execute("""create table if not exists `params` (
                                    id integer primary key,
                                    `temperature` real,
                                    `humanity`    real,
                                    `hb_persent`  real
                    )""")

            # this table for states of forks, hum. systems and 6 HB devices
            self.c.execute("""create table if not exists `states` (
                              id integer primary key,
                              `fork_state` bool,
                              `humanity_state` bool,
                              `hb_1` bool,
                              `hb_2` bool,
                              `hb_3` bool,
                              `hb_4` bool,
                              `hb_5` bool,
                              `hb_6` bool,
                              `extreme` bool                                
                        )""")

            # this table for device's data, temperature and humanity
            self.c.execute("""create table if not exists `devices_data` (
                            id integer primary key,
                            `device_id` int,
                            `temperature` real,
                            `humanity` real
            )""")

            # this table for ground humanity
            self.c.execute("""create table if not exists `ground_humanity` (
                                id integer primary key,
                                `device_id` int,
                                `humanity` real
            )""")

            # it's to be cool, create a line with default parameters in `params` table (we don't needed to write ADD)
            self.c.execute("""insert into `params` (`temperature`, `humanity`, `hb_persent`) values (10, 10, 10)""")

            # insert data (default FALSE) for all devices
            self.c.execute("""insert into `states` (
            `fork_state`, 
            `humanity_state`,
            `hb_1`,
            `hb_2`,
            `hb_3`,
            `hb_4`,
            `hb_5`,
            `hb_6`,
            `extreme`
            ) values (
            False,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE,
            FALSE
            )""")

        self.conn.commit()

    def update_user_params(self, t=-1, h=-1, hb=-1):
        """
        This function updates user parameters from `params`
        :parameter: t - user's new temperature (default = -1, that means that we don't need to change info)
                    h - user's new humanity (default = -1, , that means that we don't need to change info)
                    hb - user's new ground_humanity % (default = -1, , that means that we don't need to change info)
        :return: bool (True - good or False - not good)
        """
        # if we have data, we'll update it
        if t != -1:
            self.c.execute("""update `params` set `temperature`=? where `id`=1""", (t,))
            self.conn.commit()
        if h != -1:
            self.c.execute("""update `params` set `humanity`=? where `id`=1""", (h,))
            self.conn.commit()
        if hb != -1:
            self.c.execute("""update `params` set `hb_persent`=? where `id`=1""", (hb,))
            self.conn.commit()
        return True

    def get_user_params(self):
        """
        this function gets all user parameters from sqlite3
        :return: tuple of data (id, temperature, humanity, hb_persent)
        """
        params_data = self.c.execute("""select * from `params` where id=1""")
        params = params_data.fetchone()
        return params

    def get_fork(self):
        """
        This function gets information about fork
        :return: tuple of data (fork_state)
        """
        fork_state = self.c.execute("""select `fork_state` from `states` where id=1""")
        return fork_state.fetchone()

    def update_fork(self, new_state: bool):
        """
        This function updates the state of fork
        :param new_state: new state of fork in boolean type (True or False)
        :return: None
        """
        self.c.execute("""update `states` set `fork_state`=? where id=1""", (new_state,))
        self.conn.commit()

    def get_humanity(self):
        """
        This funcrion gets information about humanity system state
        :return: tuple of data (humanity_state)
        """
        humanity_state = self.c.execute("""select `humanity_state` from `states` where id=1""")
        return humanity_state.fetchone()

    def update_humanity(self, new_state):
        """
        This function updates the state of humanity system
        :param new_state: new state of system in boolean type (True or False)
        :return: None
        """
        self.c.execute("""update `states` set `humanity_state`=? where id=1""", (new_state,))
        self.conn.commit()

    def get_hb_device(self, device_id):
        """
        This function gets information about state of hb_device
        :param device_id: the number of device (1-6)
        :return: tuple of data (device_state)
        """
        device_state = self.c.execute(f"""select `hb_{device_id}` from `states` where id=1""")
        return device_state.fetchone()

    def update_hb_device(self, device_id, new_state):
        """
        This function updates state of one hb_device
        :param device_id: device_id: the number of device (1-6)
        :param new_state: new state of system in boolean type (True or False)
        :return: None
        """
        self.c.execute(f"""update `states` set `hb_{device_id}`=? where id=1""", (new_state,))
        self.conn.commit()

    def insert_temp_hum(self, device_id, temperature, humanity):
        """
        this function insert data to the table `device_data`
        :param device_id: the num of the device (1-6)
        :param temperature: the temperature that we got from api
        :param humanity: the humanity that we got from api
        :return: None
        """
        self.c.execute("""insert into `devices_data` (`device_id`, `temperature`, `humanity`) values (?, ?, ?)""",
                       (device_id, temperature, humanity,))
        self.conn.commit()

    def insert_ground_hum(self, device_id, humanity):
        """
        this function insert data to the table `ground_humanity`
        :param device_id: device's num (1-6)
        :param humanity: the value of humanity given from the api
        :return: None
        """
        self.c.execute("""insert into `ground_humanity` (`device_id`, `humanity`) values (?, ?)""",
                       (device_id, humanity,))
        self.conn.commit()

    def get_all_temperature(self):
        """
        this function gets all temperature from database
        :return: list of tuples with one item - temperature
        """
        data = self.c.execute("""select `temperature` from devices_data""")
        data = data.fetchall()
        return data

    def get_all_humanity(self):
        """
        this function gets all humanity from database
        :return: list of tuples with one item - humanity
        """
        data = self.c.execute("""select `humanity` from `devices_data`""")
        data = data.fetchall()
        return data

    def get_all_hb_in_one(self, num):
        """
        This function gets all humanity (from only one device) from database
        :param num: the num of device (1-6)
        :return: list of tuples with one item - humanity
        """
        data = self.c.execute("""select `humanity` from `ground_humanity` where device_id=?""", (num,))
        data = data.fetchall()
        return data

    def update_extreme(self, state):
        """
        This function updates state of extreme work
        :param state: the boolean value that we need to see
        :return: None
        """
        self.c.execute("""update `states` set `extreme`=? where id=1""", (state,))
        self.conn.commit()

    def get_extreme(self):
        """
        This function gets information about extreme state
        :return: tuple of data: (extreme)
        """
        data = self.c.execute("""select `extreme` from `states` where id=1""")
        data = data.fetchone()
        return data
