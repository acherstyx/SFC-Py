import requests
from time import sleep
import json


class SFC:
    def __init__(self, odl_addr, odl_port):
        self.odl_addr = odl_addr
        self.odl_port = odl_port

        self.sf_json = {"service-functions": {"service-function": []}}
        self.service_node_json = {"service-nodes": {"service-node": []}}
        self.sff_json = {"service-function-forwarders": {"service-function-forwarder": []}}
        self.sfc_json = {"service-function-chains": {"service-function-chain": []}}

        self.sfp_json = {}

    def __create_sf(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function:service-functions/"

        payload = json.dumps(self.sf_json)
        headers = {
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SF]", response.status_code, response.text.encode('utf8'))

    def __create_node(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-node:service-nodes"

        payload = json.dumps(self.service_node_json)
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create Node]", response.status_code, response.text.encode('utf8'))

    def __create_sff(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-forwarder:service-function-forwarders/"

        payload = json.dumps(self.sff_json)
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SFF]", response.status_code, response.text.encode('utf8'))

    def __create_sfc(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-chain:service-function-chains/"

        payload = json.dumps(self.sfc_json)
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SFC]", response.status_code, response.text.encode('utf8'))

    def __create_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-path:service-function-paths/"

        payload = "{\r\n  \"service-function-paths\": {\r\n    \"service-function-path\": [\r\n      {\r\n        \"name\": \"sfc-path1\",\r\n        \"service-chain-name\": \"chain-1\",\r\n        \"transport-type\": \"service-locator:vxlan-gpe\",\r\n        \"symmetric\": true\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SFP]", response.status_code, response.text.encode('utf8'))

    def __delete_sf(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function:service-functions/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=15e0wlxsbftton2uplxb2cgiv'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def __delete_node(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-node:service-nodes"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=15e0wlxsbftton2uplxb2cgiv'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def __delete_sff(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-forwarder:service-function-forwarders/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=15e0wlxsbftton2uplxb2cgiv'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def __delete_sfc(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-chain:service-function-chains/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=1007xgm240jjertim4053v8mi'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def __delete_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-path:service-function-paths/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=1007xgm240jjertim4053v8mi'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def get_rendered_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/operational/rendered-service-path:rendered-service-paths/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=9dbvuhluh4rh13pqa1rusz3av'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))

        json_format = json.loads(response.text.encode('utf8'))
        for path in json_format["rendered-service-paths"]["rendered-service-path"]:
            print("[Get SFP Rendered]", path["path-id"])

        return json_format

    def add_sf(self, sf_name, ip, port, service_type, sff_name):
        self.sf_json["service-functions"]["service-function"].append({})
        new_sf = self.sf_json["service-functions"]["service-function"][-1]
        new_sf["name"] = sf_name
        new_sf["rest-uri"] = "http://" + ip + ":5000"
        new_sf["type"] = service_type
        new_sf["ip-mgmt-address"] = ip

        new_sf["sf-data-plane-locator"] = []
        new_sf["sf-data-plane-locator"].append({})
        new_sf["sf-data-plane-locator"][-1]["name"] = "vxlan"
        new_sf["sf-data-plane-locator"][-1]["port"] = port
        new_sf["sf-data-plane-locator"][-1]["ip"] = ip
        new_sf["sf-data-plane-locator"][-1]["service-function-forwarder"] = sff_name
        new_sf["sf-data-plane-locator"][-1]["transport"] = "service-locator:vxlan-gpe"

        print(json.dumps(self.sf_json))

    def add_service_node(self, node_name, sf_name, sff_name, ip):
        self.service_node_json["service-nodes"]["service-node"].append({})
        self.service_node_json["service-nodes"]["service-node"][-1]["name"] = node_name
        self.service_node_json["service-nodes"]["service-node"][-1]["ip-mgmt-address"] = ip
        self.service_node_json["service-nodes"]["service-node"][-1]["service-function"] = [sf_name]
        self.service_node_json["service-nodes"]["service-node"][-1]["service-function-forwarder"] = [sff_name]

        print(json.dumps(self.service_node_json))

    def add_sff(self, sff_name, node_name, ip, sff_port, sf_dict):
        self.sff_json["service-function-forwarders"]["service-function-forwarder"].append({})
        new_sff = self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]

        new_sff["name"] = sff_name
        new_sff["service-node"] = node_name
        new_sff["rest-uri"] = "http://" + ip + ":5000"
        new_sff["ip-mgmt-address"] = ip
        new_sff["sff-data-plane-locator"] = []
        new_sff["sff-data-plane-locator"].append({})
        new_sff["sff-data-plane-locator"][-1]["name"] = "dp1"
        new_sff["sff-data-plane-locator"][-1]["data-plane-locator"] = {}
        new_sff["sff-data-plane-locator"][-1]["data-plane-locator"]["port"] = sff_port
        new_sff["sff-data-plane-locator"][-1]["data-plane-locator"]["ip"] = ip
        new_sff["sff-data-plane-locator"][-1]["data-plane-locator"]["transport"] = "service-locator:vxlan-gpe"

        # dictionary
        new_sff[
            "service-function-dictionary"] = []
        for sf in sf_dict:
            new_sff["service-function-dictionary"].append({})
            new_sff["service-function-dictionary"][-1]["name"] = sf
            new_sff["service-function-dictionary"][-1]["sff-sf-data-plane-locator"] = {"sf-dpl-name": "vxlan",
                                                                                       "sff-dpl-name": "dp1"}
            new_sff["service-function-dictionary"][-1]["failmode"] = "service-function-forwarder:open"

        print(json.dumps(self.sff_json))

    def add_sfc(self, sfc_name, service_type_list):
        # 添加单个类别的服务到服务链
        self.sfc_json["service-function-chains"]["service-function-chain"].append({})
        new_sfc = self.sfc_json["service-function-chains"]["service-function-chain"][-1]
        new_sfc["name"] = sfc_name
        new_sfc["sfc-service-function"] = []

        for index, service_type in enumerate(service_type_list):
            new_sfc["sfc-service-function"].append({})
            new_sfc["sfc-service-function"][-1]["name"] = "chain-node-" + str(index + 1)
            new_sfc["sfc-service-function"][-1]["type"] = service_type

        print(json.dumps(self.sfc_json))

    def apply_config(self):
        print("[SFC] Deleting old config.")
        self.__delete_sfp()
        self.__delete_sfc()
        self.__delete_sff()
        self.__delete_node()
        self.__delete_sf()
        print("[SFC] Applying new config.")
        self.__create_sf()
        sleep(1)
        self.__create_node()
        sleep(1)
        self.__create_sff()
        sleep(1)
        self.__create_sfc()
        sleep(1)
        self.__create_sfp()
        sleep(5)
        self.get_rendered_sfp()


if __name__ == "__main__":
    sfc_connection = SFC("localhost", "8181")

    sfc_connection.add_sf("SF1", "127.0.0.1", "10001", "firewall", "SFF1")
    sfc_connection.add_sf("SF2", "127.0.0.1", "10002", "dpi", "SFF1")
    sfc_connection.add_sf("SF3", "127.0.0.1", "10003", "histogram", "SFF1")
    sfc_connection.add_service_node("Node1", "SF1", "SFF1", "127.0.0.1")
    sfc_connection.add_service_node("Node2", "SF2", "SFF1", "127.0.0.1")
    sfc_connection.add_service_node("Node3", "SF3", "SFF1", "127.0.0.1")
    sfc_connection.add_sff("SFF1", "Node1", "127.0.0.1", 4789, ["SF1", "SF2", "SF3"])
    sfc_connection.add_sfc("chain-1", ["dpi", "firewall", "histogram"])
    sfc_connection.apply_config()
