create table users
(
    id_user         int auto_increment
        primary key,
    username        varchar(50)                           not null,
    email           varchar(100)                          not null,
    hashed_password varchar(255)                          not null,
    date_created    timestamp default current_timestamp() not null,
    constraint email
        unique (email),
    constraint username
        unique (username),
    constraint chk_email_not_empty
        check (),
    constraint chk_password_length
        check (),
    constraint chk_username_length
        check (),
    constraint chk_username_not_empty
        check ()
);

create table admins
(
    id_admin        int auto_increment
        primary key,
    username        varchar(50)                           not null,
    email           varchar(100)                          not null,
    hashed_password varchar(255)                          not null,
    date_created    timestamp default current_timestamp() not null,
    constraint email
        unique (email),
    constraint username
        unique (username),
    constraint chk_email_not_empty
        check (),
    constraint chk_password_length
        check (),
    constraint chk_username_length
        check (),
    constraint chk_username_not_empty
        check (),
    constraint email
        check ()
);

create table albums
(
    id_album     int auto_increment
        primary key,
    title        varchar(100) not null,
    id_artist    int          not null,
    id_genre     int          null,
    release_year year         not null,
    constraint albums_ibfk_1
        foreign key (id_artist) references spotifydb.artists (id_artist),
    constraint albums_ibfk_2
        foreign key (id_genre) references spotifydb.genres (id_genre),
    constraint chk_album_title_length
        check (),
    constraint chk_album_title_not_empty
        check ()
);

create index id_artist
    on albums (id_artist);

create index id_genre
    on albums (id_genre);

create table songs
(
    id_song  int auto_increment
        primary key,
    title    varchar(100) not null,
    duration time         not null,
    id_album int          not null,
    id_genre int          null,
    constraint songs_ibfk_1
        foreign key (id_album) references spotifydb.albums (id_album),
    constraint songs_ibfk_2
        foreign key (id_genre) references spotifydb.genres (id_genre),
    constraint chk_duration_valid
        check (),
    constraint chk_song_title_length
        check (),
    constraint chk_song_title_not_empty
        check ()
);

create index id_album
    on songs (id_album);

create index id_genre
    on songs (id_genre);

create table artists
(
    id_artist       int auto_increment
        primary key,
    name            varchar(100)                          not null,
    email           varchar(100)                          not null,
    hashed_password varchar(255)                          not null,
    id_country      int                                   null,
    date_created    timestamp default current_timestamp() not null,
    constraint email
        unique (email),
    constraint name
        unique (name),
    constraint artists_ibfk_1
        foreign key (id_country) references spotifydb.countries (id_country),
    constraint chk_artist_name_length
        check (),
    constraint chk_artist_name_not_empty
        check (),
    constraint chk_id_country_positive
        check ()
);

create index id_country
    on artists (id_country);

create table countries
(
    id_country int auto_increment
        primary key,
    name       varchar(50) not null,
    constraint name
        unique (name),
    constraint chk_country_name_length
        check (),
    constraint chk_country_name_not_empty
        check ()
);

create table genres
(
    id_genre int auto_increment
        primary key,
    name     varchar(50) not null,
    constraint name
        unique (name),
    constraint chk_genre_name_length
        check (),
    constraint chk_genre_name_not_empty
        check ()
);

create table playlists
(
    id_playlist int auto_increment
        primary key,
    name        varchar(100)         not null,
    id_user     int                  not null,
    is_public   tinyint(1) default 1 null,
    constraint id_user
        unique (id_user, name),
    constraint playlists_ibfk_1
        foreign key (id_user) references spotifydb.users (id_user),
    constraint chk_is_public_valid
        check (),
    constraint chk_playlist_name_length
        check (),
    constraint chk_playlist_name_not_empty
        check ()
);

create table playlist_songs
(
    id_playlist int                                   not null,
    id_song     int                                   not null,
    added_at    timestamp default current_timestamp() not null,
    primary key (id_playlist, id_song),
    constraint playlist_songs_ibfk_1
        foreign key (id_playlist) references spotifydb.playlists (id_playlist),
    constraint playlist_songs_ibfk_2
        foreign key (id_song) references spotifydb.songs (id_song)
);

create index id_song
    on playlist_songs (id_song);

create table song_stats
(
    id_song     int           not null
        primary key,
    play_count  int default 0 not null,
    last_played timestamp     null,
    constraint song_stats_ibfk_1
        foreign key (id_song) references spotifydb.songs (id_song),
    constraint chk_play_count_positive
        check ()
);

create table subscriptions
(
    id_subscription int auto_increment
        primary key,
    id_user         int  not null,
    start_date      date not null,
    end_date        date not null,
    constraint id_user
        unique (id_user),
    constraint subscriptions_ibfk_1
        foreign key (id_user) references spotifydb.users (id_user),
    constraint chk_end_date_valid
        check (),
    constraint chk_start_date_valid
        check ()
);

create table admin_created_playlists
(
    id_playlist int                                   not null
        primary key,
    id_admin    int                                   not null,
    created_at  timestamp default current_timestamp() not null,
    constraint admin_created_playlists_ibfk_1
        foreign key (id_playlist) references spotifydb.playlists (id_playlist),
    constraint admin_created_playlists_ibfk_2
        foreign key (id_admin) references spotifydb.admins (id_admin)
);

create index id_admin
    on admin_created_playlists (id_admin);

create table album_likes
(
    id_user       int                                   not null,
    id_album      int                                   not null,
    like_datetime timestamp default current_timestamp() not null,
    primary key (id_user, id_album),
    constraint album_likes_ibfk_1
        foreign key (id_user) references spotifydb.users (id_user),
    constraint album_likes_ibfk_2
        foreign key (id_album) references spotifydb.albums (id_album)
);

create index id_album
    on album_likes (id_album);

create table artist_likes
(
    id_user       int                                   not null,
    id_artist     int                                   not null,
    like_datetime timestamp default current_timestamp() not null,
    primary key (id_user, id_artist),
    constraint artist_likes_ibfk_1
        foreign key (id_user) references spotifydb.users (id_user),
    constraint artist_likes_ibfk_2
        foreign key (id_artist) references spotifydb.artists (id_artist)
);

create index id_artist
    on artist_likes (id_artist);

create table song_likes
(
    id_user       int                                   not null,
    id_song       int                                   not null,
    like_datetime timestamp default current_timestamp() not null,
    primary key (id_user, id_song),
    constraint song_likes_ibfk_1
        foreign key (id_user) references spotifydb.users (id_user),
    constraint song_likes_ibfk_2
        foreign key (id_song) references spotifydb.songs (id_song)
);

create index id_song
    on song_likes (id_song);
