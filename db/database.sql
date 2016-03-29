


drop table if exists jianqu;
create table jianqu(
    id integer primary key autoincrement,
    jianqu text not null,
    zhibanlingdao text not null,
    baitianzaigang text not null,
    yejianzhiban text not null,
    zaice text not null,
    shiyou text not null,
    chugong text not null,
    beizhu text not null,
    createtime text not null
);


drop table if exists kanshou;
create table kanshou(
    id integer primary key autoincrement,
    zhibanlingdao text not null,
    damen text not null,
    ermen text not null,
    sanmen text not null,
    beizhu text not null,
    createtime text not null
);

