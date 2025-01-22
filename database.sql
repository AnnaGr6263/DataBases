-- Tworzenie tabeli users z ograniczeniami
CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,  -- Unikalny identyfikator użytkownika (klucz główny).
    username VARCHAR(50) NOT NULL UNIQUE,    -- Nazwa użytkownika, unikalna i wymagana.
    email VARCHAR(100) NOT NULL UNIQUE,      -- Adres e-mail, unikalny i wymagany.
    hashed_password VARCHAR(255) NOT NULL,   -- Hasło (zahashowane), wymagane.
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data utworzenia, domyślnie ustawiana na aktualny czas.

    -- Ograniczenia CHECK
    CONSTRAINT chk_username_length CHECK (CHAR_LENGTH(username) >= 3), -- Minimalna długość nazwy użytkownika to 3 znaki.
    CONSTRAINT chk_password_length CHECK (CHAR_LENGTH(hashed_password) >= 60), -- Minimalna długość zahashowanego hasła.
    CONSTRAINT chk_username_not_empty CHECK (CHAR_LENGTH(TRIM(username)) > 0), -- Nazwa użytkownika nie może być pusta.
    CONSTRAINT chk_email_not_empty CHECK (CHAR_LENGTH(TRIM(email)) > 0)        -- Adres e-mail nie może być pusty.
)ENGINE=InnoDB;


CREATE TABLE admins (
    id_admin INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator administratora, klucz główny
    username VARCHAR(50) NOT NULL UNIQUE, -- Unikalna nazwa użytkownika
    email VARCHAR(100) NOT NULL UNIQUE CHECK (email LIKE '%_@_%._%'), -- Unikalny adres e-mail z podstawową walidacją formatu
    hashed_password VARCHAR(255) NOT NULL, -- Przechowywane zahaszowane hasło użytkownika
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data utworzenia konta, domyślnie aktualny czas

    -- Ograniczenia CHECK
    CONSTRAINT chk_username_length CHECK (CHAR_LENGTH(username) >= 3), -- Minimalna długość nazwy użytkownika to 3 znaki
    CONSTRAINT chk_password_length CHECK (CHAR_LENGTH(hashed_password) >= 60), -- Minimalna długość zahashowanego hasła
    CONSTRAINT chk_username_not_empty CHECK (CHAR_LENGTH(TRIM(username)) > 0), -- Nazwa użytkownika nie może być pusta
    CONSTRAINT chk_email_not_empty CHECK (CHAR_LENGTH(TRIM(email)) > 0) -- Adres e-mail nie może być pusty
)ENGINE=InnoDB;

CREATE TABLE countries (
    id_country INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator kraju, klucz główny
    name VARCHAR(50) NOT NULL UNIQUE, -- Unikalna nazwa kraju, nie może się powtarzać

    -- Ograniczenia CHECK
    CONSTRAINT chk_country_name_length CHECK (CHAR_LENGTH(name) >= 3), -- Minimalna długość nazwy kraju to 3 znaki
    CONSTRAINT chk_country_name_not_empty CHECK (CHAR_LENGTH(TRIM(name)) > 0) -- Nazwa kraju nie może być pusta lub składać się tylko z białych znaków (spacji)
)ENGINE=InnoDB;

CREATE TABLE artists (
    id_artist INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator artysty, klucz główny
    name VARCHAR(100) NOT NULL UNIQUE, -- Unikalna nazwa artysty, nie może się powtarzać
    email VARCHAR(100) NOT NULL UNIQUE, -- Unikalny e-mail artysty do logowania
    hashed_password VARCHAR(255) NOT NULL, -- Zahashowane hasło artysty
    id_country INT NULL, -- Identyfikator kraju, do którego należy artysta (może być NULL, jeśli kraj zostanie usunięty)
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data utworzenia konta artysty

    -- Ograniczenia CHECK
    CONSTRAINT chk_artist_name_length CHECK (CHAR_LENGTH(name) >= 3), -- Minimalna długość nazwy artysty to 3 znaki
    CONSTRAINT chk_artist_name_not_empty CHECK (CHAR_LENGTH(TRIM(name)) > 0), -- Nazwa artysty nie może być pusta lub składać się tylko z białych znaków

    -- Klucz obcy z referencją do tabeli countries
    FOREIGN KEY (id_country) REFERENCES countries(id_country) ON DELETE SET NULL -- Jeśli kraj zostanie usunięty, id_country ustawia się na NULL
)ENGINE=InnoDB;

CREATE TABLE genres (
    id_genre INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator gatunku muzycznego, klucz główny
    name VARCHAR(50) NOT NULL UNIQUE, -- Unikalna nazwa gatunku muzycznego

    -- Ograniczenia CHECK
    CONSTRAINT chk_genre_name_length CHECK (CHAR_LENGTH(name) >= 3), -- Minimalna długość nazwy gatunku to 3 znaki
    CONSTRAINT chk_genre_name_not_empty CHECK (CHAR_LENGTH(TRIM(name)) > 0) -- Nazwa gatunku nie może być pusta lub składać się tylko z białych znaków
)ENGINE=InnoDB;

CREATE TABLE albums (
    id_album INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator albumu, klucz główny
    title VARCHAR(100) NOT NULL, -- Tytuł albumu, musi być podany
    id_artist INT NOT NULL, -- Identyfikator artysty, który stworzył album
    id_genre INT NULL, -- Identyfikator gatunku albumu (może być NULL, jeśli gatunek zostanie usunięty)
    release_year YEAR NOT NULL, -- Rok wydania albumu

    -- Ograniczenia CHECK
    CONSTRAINT chk_album_title_length CHECK (CHAR_LENGTH(title) >= 2), -- Minimalna długość tytułu albumu to 2 znaki
    CONSTRAINT chk_album_title_not_empty CHECK (CHAR_LENGTH(TRIM(title)) > 0), -- Tytuł albumu nie może być pusty lub składać się tylko z białych znaków
 
    -- Klucze obce
    FOREIGN KEY (id_artist) REFERENCES artists(id_artist) ON DELETE CASCADE, -- Jeśli artysta zostanie usunięty, jego albumy również zostaną usunięte
    FOREIGN KEY (id_genre) REFERENCES genres(id_genre) ON DELETE SET NULL -- Jeśli gatunek zostanie usunięty, id_genre w albumie zostanie ustawione na NULL
)ENGINE=InnoDB;


CREATE TABLE songs (
    id_song INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator utworu, klucz główny
    title VARCHAR(100) NOT NULL, -- Tytuł utworu, musi być podany
    duration TIME NOT NULL, -- Czas trwania utworu
    id_album INT NOT NULL, -- Identyfikator albumu, do którego należy utwór
    id_genre INT NULL, -- Identyfikator gatunku muzycznego (może być NULL, jeśli gatunek zostanie usunięty)

    -- Ograniczenia CHECK
    CONSTRAINT chk_song_title_length CHECK (CHAR_LENGTH(title) >= 3), -- Minimalna długość tytułu utworu to 3 znaki
    CONSTRAINT chk_song_title_not_empty CHECK (CHAR_LENGTH(TRIM(title)) > 0), -- Tytuł utworu nie może być pusty lub składać się tylko z białych znaków
    CONSTRAINT chk_duration_valid CHECK (duration >= '00:00:01' AND duration <= '23:59:59'), -- Czas trwania utworu musi być między 1 sek a 23:59:59

    -- Klucze obce
    FOREIGN KEY (id_album) REFERENCES albums(id_album) ON DELETE CASCADE, -- Jeśli album zostanie usunięty, jego utwory również zostaną usunięte
    FOREIGN KEY (id_genre) REFERENCES genres(id_genre) ON DELETE SET NULL -- Jeśli gatunek zostanie usunięty, id_genre w utworach zostanie ustawione na NULL
)ENGINE=InnoDB;


CREATE TABLE playlists (
    id_playlist INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator playlisty, klucz główny
    name VARCHAR(100) NOT NULL, -- Nazwa playlisty, musi być podana
    id_user INT NOT NULL, -- Identyfikator użytkownika, który stworzył playlistę
    is_public BOOLEAN DEFAULT TRUE, -- Określa, czy playlista jest publiczna (domyślnie TRUE)

    -- Ograniczenia CHECK
    CONSTRAINT chk_playlist_name_length CHECK (CHAR_LENGTH(name) >= 3), -- Minimalna długość nazwy playlisty to 3 znaki
    CONSTRAINT chk_playlist_name_not_empty CHECK (CHAR_LENGTH(TRIM(name)) > 0), -- Nazwa playlisty nie może być pusta lub składać się tylko z białych znaków
    CONSTRAINT chk_is_public_valid CHECK (is_public IN (0, 1)), -- `is_public` musi mieć wartość 0 (fałsz) lub 1 (prawda)

    -- Ograniczenie unikalności nazwy playlisty dla danego użytkownika
    UNIQUE (id_user, name),

    -- Klucz obcy
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE -- Jeśli użytkownik zostanie usunięty, jego playlisty również zostaną usunięte
)ENGINE=InnoDB;


CREATE TABLE playlist_songs (
    id_playlist INT NOT NULL, -- Identyfikator playlisty, do której należy utwór
    id_song INT NOT NULL, -- Identyfikator utworu dodanego do playlisty
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data i czas dodania utworu do playlisty

    -- Klucz główny (kompozytowy) zapobiegający duplikatom wpisów (ta sama piosenka w tej samej playliście)
    PRIMARY KEY (id_playlist, id_song),

    -- Klucze obce
    FOREIGN KEY (id_playlist) REFERENCES playlists(id_playlist) ON DELETE CASCADE, -- Jeśli playlista zostanie usunięta, usuwane są powiązane utwory
    FOREIGN KEY (id_song) REFERENCES songs(id_song) ON DELETE CASCADE -- Jeśli piosenka zostanie usunięta, usuwane są wszystkie jej wystąpienia w playlistach
)ENGINE=InnoDB;


CREATE TABLE subscriptions (
    id_subscription INT AUTO_INCREMENT PRIMARY KEY, -- Unikalny identyfikator subskrypcji, klucz główny
    id_user INT NOT NULL UNIQUE, -- Identyfikator użytkownika (każdy użytkownik może mieć tylko jedną aktywną subskrypcję)
    start_date DATE NOT NULL, -- Data rozpoczęcia subskrypcji
    end_date DATE NOT NULL, -- Data zakończenia subskrypcji

    -- Ograniczenia CHECK
    CONSTRAINT chk_start_date_valid CHECK (start_date >= '2000-01-01'), -- Subskrypcja nie może być wcześniejsza niż rok 2000
    CONSTRAINT chk_end_date_valid CHECK (end_date > start_date), -- Data zakończenia musi być późniejsza niż data rozpoczęcia

    -- Klucz obcy
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE -- Jeśli użytkownik zostanie usunięty, jego subskrypcja również zostanie usunięta
)ENGINE=InnoDB;


CREATE TABLE song_stats (
    id_song INT NOT NULL PRIMARY KEY, -- Identyfikator utworu (każdy utwór ma jedno statystyki)
    play_count INT DEFAULT 0 NOT NULL, -- Liczba odtworzeń utworu, domyślnie 0
    last_played TIMESTAMP NULL, -- Data i czas ostatniego odtworzenia utworu

    -- Ograniczenia CHECK
    CONSTRAINT chk_play_count_positive CHECK (play_count >= 0), -- Liczba odtworzeń nie może być ujemna

    -- Klucz obcy
    FOREIGN KEY (id_song) REFERENCES songs(id_song) ON DELETE CASCADE -- Jeśli utwór zostanie usunięty, jego statystyki również zostaną usunięte
)ENGINE=InnoDB;


CREATE TABLE song_likes (
    id_user INT NOT NULL, -- Identyfikator użytkownika, który polubił piosenkę
    id_song INT NOT NULL, -- Identyfikator piosenki, która została polubiona
    like_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data i czas polubienia utworu

    -- Klucz główny (unikalne polubienie)
    PRIMARY KEY (id_user, id_song),


  -- Klucze obce
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE, -- Jeśli użytkownik zostanie usunięty, jego polubienia również zostaną usunięte
    FOREIGN KEY (id_song) REFERENCES songs(id_song) ON DELETE CASCADE -- Jeśli utwór zostanie usunięty, wszystkie polubienia tej piosenki również zostaną usunięte
)ENGINE=InnoDB;


CREATE TABLE album_likes (
    id_user INT NOT NULL, -- Identyfikator użytkownika, który polubił album
    id_album INT NOT NULL, -- Identyfikator albumu, który został polubiony
    like_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data i czas polubienia albumu

    -- Klucz główny (unikalne polubienie)
    PRIMARY KEY (id_user, id_album),

    -- Klucze obce
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE, -- Jeśli użytkownik zostanie usunięty, jego polubienia albumów również zostaną usunięte
    FOREIGN KEY (id_album) REFERENCES albums(id_album) ON DELETE CASCADE -- Jeśli album zostanie usunięty, wszystkie jego polubienia również zostaną usunięte
)ENGINE=InnoDB;


CREATE TABLE artist_likes (
    id_user INT NOT NULL, -- Identyfikator użytkownika, który polubił artystę
    id_artist INT NOT NULL, -- Identyfikator artysty, który został polubiony
    like_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data i czas polubienia artysty

    -- Klucz główny (unikalne polubienie)
    PRIMARY KEY (id_user, id_artist),

    -- Klucze obce
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE, -- Jeśli użytkownik zostanie usunięty, jego polubienia artystów również zostaną usunięte
    FOREIGN KEY (id_artist) REFERENCES artists(id_artist) ON DELETE CASCADE -- Jeśli artysta zostanie usunięty, wszystkie jego polubienia również zostaną usunięte
)ENGINE=InnoDB;

CREATE TABLE admin_created_playlists (
    id_playlist INT PRIMARY KEY, -- Identyfikator playlisty (playlista musi istnieć)
    id_admin INT NOT NULL, -- Identyfikator administratora, który stworzył playlistę
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- Data i czas przypisania playlisty do administratora

    -- Klucze obce
    FOREIGN KEY (id_playlist) REFERENCES playlists(id_playlist) ON DELETE CASCADE, -- Jeśli playlista zostanie usunięta, usunięte zostanie też powiązanie z administratorem
    FOREIGN KEY (id_admin) REFERENCES admins(id_admin) ON DELETE CASCADE -- Jeśli administrator zostanie usunięty, usunięte zostanie też jego powiązanie z playlistą
)ENGINE=InnoDB;
