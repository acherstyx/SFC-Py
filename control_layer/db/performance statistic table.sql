drop table if exists performance;
create table performance
(
    sf_id         int4,
    cpu_usage     float,
    mem_total     int8, -- 单位是Bytes
    mem_used      int8,
    net_pkg_in    int8, -- 进入服务的包的数量
    net_speed_in  int8, -- 进服务的网速
    net_speed_out int8, --出服务的网速
    constraint SF_ID_PK primary key,
    constraint SF_ID_FK foreign key(sf_id)
        references sf(id)
    on delete cascade
    on update cascade
);
