Anna Grelewska
Marcel Musiałek

# **Projekt bazy danych dla aplikacji muzycznej w stylu Spotify**  
## **Sprawozdanie z realizacji projektu**  

---

## **1. Wstęp**

Celem niniejszego projektu jest zaprojektowanie oraz implementacja relacyjnej bazy danych dla aplikacji muzycznej, umożliwiającej użytkownikom streamowanie utworów, tworzenie własnych playlist, polubianie utworów i artystów. 

W projekcie skupimy się na zaprojektowaniu struktury bazy danych w **MariaDB**
---

## **2. Analiza wymagań dla bazy danych aplikacji muzycznej**  

### **2.1. Główne wymagania**  
Baza danych musi przechowywać i udostępniać dane dla aplikacji klienckiej w sposób **wydajny i bezpieczny**. Powinna obsługiwać:  

- **Operacje CRUD** na encjach: `Users`, `Artists`, `Albums`, `Songs`, `Playlists`, `Playlist_Songs`, `Genres`, `Likes`.  
- **Bezpieczne przechowywanie haseł użytkowników**.  
- **Zapewnienie transakcyjności** dla operacji kluczowych (np. dodawanie utworów, tworzenie playlist).  
- **Informacja o subskrypcjach użytkowników** – przechowywanie planów płatnych.  
- **Wyszukiwanie utworów** na podstawie tytułu, albumu, artysty i gatunku.  
- **Statystyki odtwarzania utworów** – rejestrowanie liczby odsłuchań.  
- **Zarządzanie ulubionymi artystami i piosenkami.**

### **2.2. Ograniczenia projektu**  
1. **Baza danych działa w MariaDB**.  
2. **Nie przechowujemy plików audio** – baza danych zawiera tylko metadane utworów.  
3. **Aplikacja w Pythonie lub Javie** – baza musi zapewniać wygodny dostęp poprzez SQL (np. JDBC dla Javy lub SQLAlchemy dla Pythona).  

---

## **3. Model dziedziny i słowniki pojęciowe**  

| **Pojęcie dziedzinowe** | **Encja w bazie** | **Opis** |  
|----------------------|----------------|----------------|  
| **Użytkownik** | `Users` | Reprezentuje osoby korzystające z aplikacji. |  
| **Artysta** | `Artists` | Artysta publikujący utwory i albumy. |  
| **Administrator** | `Admin` | Reprezentuje pracownika platformy streamingowej. |  
| **Album** | `Albums` | Zbiór utworów wydanych przez artystę. |  
| **Utwór** | `Songs` | Pojedynczy utwór muzyczny, powiązany z albumem i gatunkiem. |  
| **Playlista** | `Playlists` | Zbiór utworów utworzony przez użytkownika. |  
| **Gatunek muzyczny** | `Genres` | Klasyfikacja muzyki według stylu. |  
| **Polubienie** | `Likes` | Polubienia użytkowników dotyczące utworów i artystów. |  
| **Subskrypcja** | `Subscriptions` | Informacje o planach subskrypcyjnych użytkowników. |  
| **Statystyki utworów** | `Song_Stats` | Rejestr liczby odtworzeń i ostatniego odtworzenia. |  
 | **Ulubieni artyści** | `Favorite_Artists` | Lista artystów polubionych przez użytkownika. |  

---

## **5. Modelowanie bazy danych**  

### **5.1. Model konceptualny**  
Model konceptualny przedstawia **główne encje i relacje** bez uwzględnienia detali technicznych.  

- **Użytkownicy (`Users`)** mogą posiadać **playlisty (`Playlists`)**, dodawać utwory do ulubionych oraz polubić różne elementy (`Likes`).  
- **Artyści (`Artists`)** publikują **albumy (`Albums`)**, które zawierają **utwory (`Songs`)** przypisane do określonego gatunku (`Genres`).  
- **Utwory (`Songs`)** mogą być dodawane do **playlist (`Playlist_Songs`)** i śledzone pod kątem statystyk (`Song_Stats`).  
- **Użytkownicy mogą ulubionych artystów** (`Favorite_Artists`).  

### **5.2. Model logiczny**   

# Funkcjonalności i uprawnienia użytkowników

| Funkcjonalność                 | Priorytet | Administrator          | Artysta                      | Użytkownik                   | Uzasadnienie                                 |
|--------------------------------|-----------|------------------------|------------------------------|------------------------------|---------------------------------------------|
| CRUD na użytkownikach          | Wysoki    | ✅ Pełen dostęp        | ❌ Brak dostępu              | ❌ Brak dostępu              | Niezbędne do zarządzania kontami            |
| CRUD na utworach               | Wysoki    | ✅ Pełen dostęp        | ✅ Dodawanie/edycja (tylko własne) | ❌ Brak dostępu          | Podstawa funkcjonowania aplikacji           |
| CRUD na albumach               | Wysoki    | ✅ Pełen dostęp        | ✅ Dodawanie/edycja (tylko własne) | ❌ Brak dostępu          | Albumy muszą być zarządzane przez artystów  |
| CRUD na playlistach            | Średni    | ✅ Pełen dostęp        | ❌ Brak dostępu              | ✅ Pełen dostęp              | Playlisty zwiększają komfort użytkowania    |
| Odtwarzanie utworów            | Wysoki    | ✅ Tak                 | ❌ Brak dostępu              | ✅ Tak                       | Kluczowa funkcjonalność aplikacji           |
| Polubienia (utwory, albumy, artyści) | Średni | ✅ Tak                 | ❌ Brak dostępu              | ✅ Tak                       | Personalizacja treści                       |
| Zarządzanie subskrypcjami      | Wysoki    | ✅ Tak                 | ❌ Brak dostępu              | ✅ Tylko własna subskrypcja  | Kluczowe dla modelu biznesowego             |
| Statystyki odtwarzania         | Średni    | ✅ Pełen dostęp        | ✅ Tylko własne utwory (SELECT)      | ❌ Brak dostępu              | Przydatne dla artystów do analizy popularności |
| Wyszukiwanie utworów           | Wysoki    | ✅ Pełen dostęp        | ❌ Brak dostępu              | ✅ Tak                       | Ułatwia dostęp do treści                    |

—

### **➢ Tabela `Users`**  
a) **Encja**: Użytkownik  
b) **Atrybuty**:  
   - `id_user`: Unikalny identyfikator użytkownika (klucz główny).  
   - `username`: Unikalna nazwa użytkownika.  
   - `email`: Unikalny adres e-mail użytkownika.  
   - `password`: Hasło użytkownika (przechowywane w formie zaszyfrowanej).  
   - `subscription_id`: Identyfikator subskrypcji użytkownika (klucz obcy).  
   - `date_created`: Data rejestracji użytkownika.  
c) **Relacje**:  
   - Użytkownik może mieć **jedną subskrypcję** (`subscription_id` → `Subscriptions.id_subscription`).  
   - Użytkownik może **tworzyć playlisty** (`id_user` → `Playlists.id_user`).  
   - Użytkownik może **polubić utwory, albumy lub artystów** (`id_user` → `Likes.id_user`).  

---

### **➢ Tabela `Artists`**  
a) **Encja**: Artysta  
b) **Atrybuty**:  
   - `id_artist`: Unikalny identyfikator artysty (klucz główny).  
   - `name`: Nazwa artysty.  
   - `genre_id`: Identyfikator gatunku artysty (klucz obcy).  
   - `country`: Kraj pochodzenia artysty.  
c) **Relacje**:  
   - Artysta może mieć **wiele albumów** (`id_artist` → `Albums.id_artist`).  
   - Artysta może mieć **wiele utworów** (`id_artist` → `Songs.id_artist`).  
   - Artysta jest przypisany do **jednego gatunku muzycznego** (`genre_id` → `Genres.id_genre`).  

---

### **➢ Tabela `Admins`**  
a) **Encja**: Administrator  
b) **Atrybuty**:  
   - `id_admin`: Unikalny identyfikator administratora (klucz główny).  
   - `username`: Unikalna nazwa administratora.  
   - `email`: Unikalny adres e-mail administratora.  
   - `password`: Hasło administratora (przechowywane w formie zaszyfrowanej).  
   - `date_created`: Data utworzenia konta administratora.  
c) **Relacje**:  
   - Administrator może **tworzyć oficjalne playlisty** (`id_admin` → `Playlists.created_by_admin`).  
   - Administrator może **zarządzać statystykami utworów** (`id_admin` → `Song_Stats.id_song`).  

---

### **➢ Tabela `Albums`**  
a) **Encja**: Album  
b) **Atrybuty**:  
   - `id_album`: Unikalny identyfikator albumu (klucz główny).  
   - `title`: Tytuł albumu.  
   - `id_artist`: Identyfikator artysty, który stworzył album (klucz obcy).  
   - `release_year`: Rok wydania albumu.  
c) **Relacje**:  
   - Album jest przypisany do **jednego artysty** (`id_artist` → `Artists.id_artist`).  
   - Album może zawierać **wiele utworów** (`id_album` → `Songs.id_album`).  

---

### **➢ Tabela `Songs`**  
a) **Encja**: Utwór  
b) **Atrybuty**:  
   - `id_song`: Unikalny identyfikator utworu (klucz główny).  
   - `title`: Tytuł utworu.  
   - `duration`: Czas trwania utworu.  
   - `id_album`: Identyfikator albumu, do którego należy utwór (klucz obcy).  
   - `id_artist`: Identyfikator artysty wykonującego utwór (klucz obcy).  
   - `id_genre`: Identyfikator gatunku utworu (klucz obcy).  
c) **Relacje**:  
   - Utwór należy do **jednego albumu** (`id_album` → `Albums.id_album`).  
   - Utwór jest przypisany do **jednego artysty** (`id_artist` → `Artists.id_artist`).  
   - Utwór ma określony **gatunek muzyczny** (`id_genre` → `Genres.id_genre`).  

---

### **➢ Tabela `Playlists`**  
a) **Encja**: Playlista  
b) **Atrybuty**:  
   - `id_playlist`: Unikalny identyfikator playlisty (klucz główny).  
   - `name`: Nazwa playlisty.  
   - `id_user`: Identyfikator użytkownika, który stworzył playlistę (klucz obcy).  
   - `is_public`: Czy playlista jest publiczna? (Boolean).  
   - `created_by_admin`: Czy playlista została stworzona przez administratora? (Boolean).  
c) **Relacje**:  
   - Playlista jest przypisana do **jednego użytkownika** (`id_user` → `Users.id_user`).  
   - Playlista może zawierać **wiele utworów** (`id_playlist` → `Playlist_Songs.id_playlist`).  

---

### **➢ Tabela `Genres`**  
a) **Encja**: Gatunek muzyczny  
b) **Atrybuty**:  
   - `id_genre`: Unikalny identyfikator gatunku (klucz główny).  
   - `name`: Nazwa gatunku muzycznego.  
c) **Relacje**:  
   - Każdy gatunek może mieć **wiele utworów** (`id_genre` → `Songs.id_genre`).  

---

### **➢ Tabela `Subscriptions`**  
a) **Encja**: Subskrypcja  
b) **Atrybuty**:  
   - `id_subscription`: Unikalny identyfikator subskrypcji (klucz główny).   
   - `price`: Cena subskrypcji.  
   - `start_date`: Data rozpoczęcia subskrypcji.  
   - `end_date`: Data zakończenia subskrypcji.  
c) **Relacje**:  
   - Subskrypcja jest przypisana do **jednego użytkownika** (`id_subscription` → `Users.subscription_id`).  

---

### **➢ Tabela `Likes`**  
a) **Encja**: Polubienie  
b) **Atrybuty**:  
   - `id_like`: Unikalny identyfikator polubienia (klucz główny).  
   - `id_user`: Identyfikator użytkownika, który polubił (klucz obcy).  
   - `item_id`: Identyfikator polubionego elementu (utwór, album, artysta).  
   - `item_type`: Typ polubionego elementu (`song`, `album`, `artist`).  
   - `like_datetime`: Data polubienia.  
c) **Relacje**:  
   - Każdy użytkownik może **polubić wiele elementów** (`id_user` → `Users.id_user`).  

Zmiana:
Usunięcie kolumny genre_id z tabeli Artists
Teraz Genres odnosi się tylko do Songs


Normalizacja:
1NF – Każda kolumna przechowuje tylko jedną wartość (atomowość).
2NF – Wszystkie kolumny zależą od całego klucza głównego.
3NF – Nie ma zależności przechodnich.

User - spełnia 3NF
1NF - Każda kolumna przechowuje tylko jedną wartość. Nie ma powtarzających się grup danych.
2NF - Klucz główny (id_user) jednoznacznie identyfikuje każdą kolumnę.
3NF - subscription_id → zależy od Users, ale jednocześnie Subscriptions przechowuje szczegóły. Nie ma zależności przechodnich.

Artists - problem
1NF - Każdy artysta ma jedną nazwę, jeden gatunek i jedno państwo.
2NF - Klucz główny id_artist jednoznacznie identyfikuje artystę i wszystkie pozostałe kolumny zależą bezpośrednio od niego.
3NF - country może być zależne od nazwy artysty (name), ponieważ każdy artysta pochodzi z jednego kraju.
Jeśli przechowujemy country w Artists, istnieje ryzyko redundancji, np. "USA" będzie powtarzane dla wielu artystów z USA.

Rozwiązanie: 
Utworzenie nowej tabeli Countries, aby usunąć zależność przechodnią i uniknąć powtarzania tych samych wartości.

Albums - spełnia 3NF
1NF - Każda kolumna przechowuje tylko jedną wartość (atomowość). Nie ma list wartości w jednej komórce. Każdy wiersz ma unikalny klucz główny (id_album).
2NF - Klucz główny id_album jednoznacznie identyfikuje album i wszystkie pozostałe kolumny zależą bezpośrednio od niego.
3NF - Nie ma zależności przechodnich.

Songs - problem
1NF - Każda kolumna przechowuje tylko jedną wartość (atomowość). Nie ma list wartości w jednej kolumnie. Każdy wiersz ma unikalny klucz główny (id_song).
2NF - title, duration → zależą tylko od id_song  (OK)
id_album → zależy od id_song (OK)
id_artist → może być uzyskane również z  id_album! 

Rozwiązanie:
Usunięcie id_artist z Songs, ponieważ id_artist można określić na podstawie id_album.

3NF - (id_genre zależy od id_song, co jest poprawne, ponieważ każdy utwór ma jeden gatunek.) Nie ma zależności przechodnich.

Genres - spełnia 3NF
1NF - Każda kolumna przechowuje tylko jedną wartość (atomowość). Nie ma list wartości w jednej kolumnie. Każdy wiersz ma unikalny klucz główny (id_genre).
2NF - Wszystkie kolumny zależą wyłącznie od id_genre, ponieważ name to nazwa gatunku i nie zależy od żadnych innych atrybutów.
3NF - Nie ma żadnych zależności przechodnich – name zależy bezpośrednio od id_genre.

Playlists - problem 
1NF - Każda kolumna przechowuje tylko jedną wartość (atomowość). Nie ma list wartości w jednej kolumnie. Każdy wiersz ma unikalny klucz główny (id_playlist).
2NF - name → zależy tylko od id_playlist (OK)
id_user → odnosi się do twórcy playlisty, ale nie zawsze jest obecne (np. gdy playlista została stworzona przez admina) 
created_by_admin → zależy od tego, czy playlista została utworzona przez admina, ale jest redundancją (można określić to na podstawie id_user lub dodatkowej tabeli) 

Rozwiązanie:
Przenosimy created_by_admin do osobnej tabeli Admin_Created_Playlists.

3NF - Po zmianach nie ma już zależności przechodnich. 

Playlist_Songs - spełnia 3NF
1NF - Każda kolumna przechowuje tylko jedną wartość (atomowość). Nie ma list wartości w jednej kolumnie. Każdy wiersz ma unikalny klucz główny ((id_playlist, id_song)).
2NF - Klucz główny (id_playlist, id_song) jednoznacznie identyfikuje wpis, a added_at zależy od obu wartości.
3NF - e ma żadnych zależności przechodnich, ponieważ added_at zależy bezpośrednio od (id_playlist, id_song).

Subscriptions - problem
1NF - Każdy wiersz ma unikalny klucz główny (id_subscription).
2NF - price, start_date, end_date zależą bezpośrednio od id_subscription
3NF - price nie ma sensu skoro zakladamy jeden rodzaj subskrypcji a cena jest stała.

Rozwiązanie:
Usunięto price, ponieważ subskrypcja zawsze kosztuje tyle samo – cena będzie przechowywana w aplikacji.
Usunięto id_type, ponieważ mamy tylko jeden rodzaj subskrypcji.
Każdy id_user może mieć tylko jedną subskrypcję (UNIQUE CONSTRAINT na id_user).

Song_Stats - spełnia 3NF
1NF - Każdy wiersz ma unikalny klucz główny (id_song).
2NF - play_count zależy tylko od id_song. last_played zależy tylko od id_song 
3NF - Nie ma żadnych zależności przechodnich, ponieważ play_count i last_played zależą bezpośrednio od id_song.


Likes - problem
1NF - Każdy wiersz ma unikalny klucz główny (id_like).
2NF -id_user zależy od id_like. 
item_id i item_type są związane z id_like, 
item_id wskazuje na różne encje (Songs, Albums, Artists).
item_type powoduje brak referencyjnej integralności (nie mamy bezpośrednich kluczy obcych do Songs, Albums, Artists).

Rozwiązane: 
Tworzymy osobne tabele dla każdego typu polubienia:
Song_Likes → dla polubionych utworów
Album_Likes → dla polubionych albumów
Artist_Likes → dla polubionych artystów

3NF - Po zmianach nie ma już zależności przechodnich!

Favorite_Artists - problem
Usunięto  Favorite_Artists, bo jej funkcję może spełniać Artist_Likes.

Admins  - spełnia 3NF
1NF - Każdy wiersz ma unikalny klucz główny (id_admin).
2NF - username, email, password, date_created zależą tylko od id_admin
3NF - Każdy email i username jest bezpośrednio związany z id_admin, więc nie ma problemu.

Po wszystkich wprowadzonych zmianach wszystkie tabele zostały do 3NF.




---

### **5.3. Model fizyczny**  
Model fizyczny przedstawia sposób **implementacji bazy w MariaDB**, uwzględniając:  

- **Indeksy na `username`, `email`, `title`** dla szybszego wyszukiwania.  
- **Optymalizację zapytań** poprzez indeksy na kluczach obcych.  
- **Transakcje dla operacji dodawania ocen i playlist**.  
- **Zabezpieczenia i mechanizmy autoryzacji** użytkowników.  



# Data-dases
