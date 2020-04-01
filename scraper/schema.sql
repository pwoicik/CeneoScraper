create table if not exists product (
    id integer primary key,
    url text unique  not null,
    name text not null,
    img_url text,
    score float
);

create table if not exists review (
    id integer primary key,
    product_id integer not null,
    author text not null,
    is_recommending boolean,
    score float,
    is_purchase_confirmed boolean not null,
    issue_date datetime not null,
    purchase_date datetime,
    yes_votes integer not null,
    no_votes integer not null,
    content text not null,
    pros text,
    const text,
    foreign key (product_id) references product (id)
);
