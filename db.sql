create database touristy_db;

use touristy_db;

--history on is a boolean
create table user(
    user_id int primary key auto_increment,
    user_name varchar(50) unique not null,
    user_password varchar(200) not null,
    status varchar(15) default 'active',
    constraint check_status check(status = 'active' or status = 'banned' or status = 'suspended')
);

create table admin(
    admin_id int primary key auto_increment,
    admin_name varchar(50) unique not null,
    admin_password varchar(200) not null
);

create table service(
    service_id int primary key auto_increment,
    user_id int not null,
    latitude double(20, 17) not null,
    longitude double(20, 17) not null,
    service_title varchar(40) not null,
    service_type varchar(20) not null,
    adress varchar(60) not null,
    constraint service_fk foreign key (user_id) references user(user_id),
    unique service_composite_unique(latitude, longitude, service_title)
);

create table image(
    image_id int primary key auto_increment,
    image_url varchar(300) not null,
    service_id int not null,
    constraint image_fk foreign key (service_id) references service(service_id) on delete cascade,
    unique image_unique(image_url, service_id)
);

create table rating(
    rating_id int primary key auto_increment
    user_id int,
    service_id int,
    stars int not null,
    comment_str varchar(200),
    unique rating_unique (user_id, service_id),
    constraint rating_user_fk foreign key (user_id) references user(user_id) on delete cascade,
    constraint rating_service_fk foreign key (service_id) references service(service_id) on delete cascade,
    constraint rating_stars_check check(stars >= 0 and stars <= 5)
);

create table favorite(
    favorite_id int primary key auto_increment,
    user_id int,
    service_id int,
    add_date date not null,
    unique favourite_unique (user_id, service_id),
    constraint favorite_user_fk foreign key (user_id) references user(user_id) on delete cascade,
    constraint favorite_service_fk foreign key (service_id) references service(service_id) on delete cascade
);

create table plan(
    plan_id int primary key auto_increment,
    user_id int not null,
    plan_title varchar(30) not null,
    plan_description varchar(100),
    plan_start date not null,
    plan_end date not null,
    constraint plan_user_fk foreign key (user_id) references user(user_id) on delete cascade,
    unique plan_unique (plan_title, user_id)
);

create table stop(
    stop_id int primary key auto_increment,
    plan_id int not null,
    service_id int not null,
    stop_datetime datetime,
    constraint stop_fk foreign key (plan_id) references plan(plan_id) on delete cascade,
    constraint plan_service_fk foreign key (service_id) references service(service_id) on delete cascade,
    unique plan_service_time(plan_id, service_id, stop_datetime)
);

CREATE DATABASE touristy_db CHARACTER SET UTF8;
CREATE USER touristy_test_user@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON touristy_db.* TO touristy_test_user@localhost;
FLUSH PRIVILEGES;

