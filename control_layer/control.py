from control_layer.db.get_config import SFCDatabase
from control_layer.config.send_config import SFC


def load_config(db_conn: SFCDatabase, sfc):
    sf_raw_data = db_conn.get_sf()
    sfc_raw_data = db_conn.get_sfc()

    sf_name_list = []

    # add sf and node
    for sf in sf_raw_data:
        sfc.add_sf(sf_name=sf[1],
                   ip=sf[2],
                   port=sf[3],
                   service_type=sf[4],
                   sff_name="SFF1")  # TODO: 使用不同的SFF，探究SFF差异
        sfc.add_service_node(node_name="Node" + sf[1],
                             sf_name=sf[1],
                             ip=sf[2],
                             sff_name="SFF1")  # TODO: 和上面同样的，指定SFF
        sf_name_list.append(sf[1])

    sfc.add_sff(sff_name="SFF1",
                node_name="Node1" + sf_name_list[0],
                ip='127.0.0.1',  # TODO: 指定不同的SFF的IP和PORT
                sff_port=4789,
                sf_dict=sf_name_list)

    # add sfc
    for sfc in sfc_raw_data:
        sfc_instance.add_sfc(sfc_name=sfc[1],
                             service_type_list=sfc[2])


if __name__ == "__main__":
    db_connection = SFCDatabase(host="localhost",
                                port="5432",
                                database="sfc",
                                user="postgres",
                                password="123456")

    sfc_instance = SFC(odl_addr="localhost",
                       odl_port="8181")

    load_config(db_connection, sfc_instance)

    sfc_instance.apply_config()
