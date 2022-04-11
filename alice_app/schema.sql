drop table if exists token;
create table token(
    id integer primary key autoincrement,
    login text not null,
    access_token text not null,
    refresh_token text not null
);

create unique index uq__token__login on token(login);
create unique index uq__token__access_token on token(access_token);
create unique index uq__token__refresh_token on token(refresh_token);
