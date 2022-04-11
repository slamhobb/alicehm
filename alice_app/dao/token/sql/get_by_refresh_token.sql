select
    id,
    login,
    access_token,
    refresh_token
    from token
    where refresh_token = :refresh_token;
