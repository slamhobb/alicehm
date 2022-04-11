update token
    set access_token = :access_token,
        refresh_token = :refresh_token
    where id = :id;
