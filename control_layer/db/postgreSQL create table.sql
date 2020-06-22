-- service function
create table sf
(
    id   serial,
    name varchar(20) not null, -- 服务名
    ip   varchar(15) not null, -- 服务部署在那个ip上（目前全127.0.0.1）
    port int         not null, -- 服务收发信息的端口
    type varchar(15) not null, -- 服务类型 firewall, dpi, qos, ...
    constraint ID_PK primary key (id)
);

-- service function chain
create table sfc
(
    id           serial primary key,
    name         varchar(20),             -- 服务链名称
    service_list varchar(15)[20] not null -- 服务链中服务列表。最多20个服务（暂定）
);

-- 测试数据
insert into sf (name, ip, port, type)
values ('SF1', '127.0.0.1', 10001, 'firewall'),
       ('SF2', '127.0.0.1', 10002, 'dpi'),
       ('SF3', '127.0.0.1', 10003, 'qos');
select * from sf;

insert into sfc(name, service_list)
values ('chain-1', array ['firewall','dpi']),
       ('chain-2', array ['qos','dpi','firewall']);

select * from sfc;