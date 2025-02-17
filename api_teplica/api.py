import requests as rq
import json


class TeplicaApi:
    """
    This class is a class for a connection to an api of TEPLICA
    """

    head_token = dict()

    def get_temp_hum(self, num: int):
        """
        This function get information about temperature and humanity from device with ids (1-4)
        :param num: device's id
        :return: dict
            {
                "id": device_id,
                "temperature": temp_value,
                "humidity": hum_value
            }
        """
        res_json = rq.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{num}", headers=self.head_token)
        result = json.loads(res_json.text)
        return result

    def get_ground_hum(self, num: int):
        """
        This function get information about humanity of ground from device with ids (1-6)
        :param num: device's id
        :return: dict
            {
                "id": device_id,
                "humidity": hum_value
            }
        """
        res_json = rq.get(f"https://dt.miet.ru/ppo_it/api/hum/{num}", headers=self.head_token)
        result = json.loads(res_json.text)
        return result

    def patch_fork(self, status: int):
        """
        This function patch the information about fork state (open or close)
        :param status: 0 - close fork, 1 - open fork
        :return: response
        """
        data = {"state": status}
        result = rq.patch(f"https://dt.miet.ru/ppo_it/api/fork_drive", params=data, headers=self.head_token)
        return result

    def patch_watering(self, num: int, status: int):
        """
        This function patch the status of watering devices (1-6)
        :param num: watering device's id (1-6)
        :param status: 0 - close watering device, 1 - open watering device
        :return: response
        """
        data = {"id": num, "state": status}
        result = rq.patch(f"https://dt.miet.ru/ppo_it/api/watering", params=data, headers=self.head_token)
        return result

    def patch_total_hum(self, status):
        """
        This function patch the status of total humidity system
        :param status: 0 - end watering, 1 - start watering
        :return: response
        """
        data = {"state": status}
        result = rq.patch(f"https://dt.miet.ru/ppo_it/api/total_hum", params=data, headers=self.head_token)
        return result

    def __init__(self, token: str):
        """
        Initialization of api, needed token
        :param token: token
        """
        self.head_token = {"X-Auth-Token": token}
