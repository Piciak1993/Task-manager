# Uruchomienie Aplikacji

Aby uruchomić aplikację i wszystkie zależności, wykonaj poniższe kroki.

### 1. Uruchomienie Aplikacji za pomocą Docker Compose

Przejdź do katalogu, w którym znajduje się plik `docker-compose.yml`, a następnie uruchom aplikację za pomocą komendy:

```bash
docker-compose up -d
```
# Zakładanie Topików w Kafka

W przypadku, gdy aplikacja wymaga utworzenia specyficznych topików w systemie Kafka, należy wykonać poniższe kroki. Topiki są wykorzystywane do przesyłania wiadomości między różnymi komponentami systemu (np. między mikroserwisami).

### 1. Założenie Topików na Serwerze Kafka

Po uruchomieniu aplikacji oraz serwera Kafka, topiki mogą być utworzone ręcznie za pomocą narzędzia Kafka CLI lub mogą zostać utworzone automatycznie, jeśli aplikacja ma taką funkcjonalność.

Dwa główne topiki, które muszą zostać założone:

- **`user-events`** - topik do przesyłania zdarzeń związanych z użytkownikami (np. rejestracja, logowanie, aktualizacja profilu).
- **`task-events`** - topik do przesyłania zdarzeń związanych z zadaniami (np. tworzenie, aktualizacja, usuwanie zadań).

### 2. Tworzenie Topików za pomocą `kafka-topics`

Po uruchomieniu aplikacji oraz serwera Kafka, użyj poniższych komend do stworzenia wymaganych topików:

#### Tworzenie Topiku:

```bash
docker exec -it kafka kafka-topics --create --topic user-events --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics --create --topic task-events --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1
docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --replication-factor 1 --partitions 50 --topic __consumer_offsets
```

### Inicjalizacja Bazy Danych

Aby przygotować bazę danych na potrzeby aplikacji, należy wykonać proces inicjalizacji, który wstępnie załaduje dane do systemu (np. utworzy domyślne rekordy użytkowników, zadań itp.). W tym celu należy uruchomić odpowiednie skrypty w zależności od wymagań aplikacji.

### 1. Inicjalizacja Bazy Danych dla Użytkowników

Aby zainicjować dane użytkowników w bazie danych, przejdź do katalogu, w którym znajduje się plik `init_db.py` odpowiedzialny za inicjalizację bazy danych dla użytkowników.

#### Uruchomienie Skryptu Inicjalizacji dla Użytkowników:

W terminalu uruchom poniższą komendę:

```bash
docker exec -it user python init_db.py
docker exec -it task python init_db.py
```

---

## Autoryzacja

### Login
**Endpoint:**  
`POST /auth/login`

**Opis:**  
Logowanie użytkownika oraz uzyskanie tokena JWT.

**Wymagane zmienne:**
- `grant_type`: Typ grantów (np. `password`).
- `username`: Adres e-mail użytkownika.
- `password`: Hasło użytkownika.
- `client_id`: ID klienta (przykładowa wartość `string`).
- `client_secret`: Sekret klienta (przykładowa wartość `string`).

**Przykładowe zapytanie:**
```bash
curl -s -X 'POST' \
  'http://localhost:8001/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=test@local.com&password=Test1234!&scope=&client_id=string&client_secret=string'
```


### Weryfikacja Tokena
**Endpoint:**  
`POST /auth/verify-token`

**Opis:**  
Weryfikacja poprawności tokena JWT.

**Wymagane zmienne:**
- `token` (query parameter): Token JWT do weryfikacji.
- `status_code` (query parameter): Kod statusu, który ma zostać zwrócony po weryfikacji (np. `200`).

**Przykładowe zapytanie:**
```bash
curl -X 'POST' \
  'http://localhost:8001/auth/verify-token?token=your_jwt_token&status_code=200' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "additionalProp1": "string",
  "additionalProp2": "string",
  "additionalProp3": "string"
}'
```


### Tworzenie Użytkownika
**Endpoint:**  
`POST /user/`

**Opis:**  
Tworzy nowego użytkownika w systemie.

**Wymagane zmienne (JSON w ciele zapytania):**
- `email`: Adres e-mail użytkownika (string, wymagany).
- `password`: Hasło użytkownika (string, wymagany).
- `name`: Imię użytkownika (string, opcjonalne).

**Nagłówki:**
- `Content-Type`: `application/json`
- `Authorization`: Bearer token JWT (jeśli wymagana autoryzacja).

**Przykładowe zapytanie:**
```bash
curl -X 'POST' \
  'http://localhost:8000/user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_jwt_token' \
  -d '{
  "email": "newuser@example.com",
  "password": "SecurePassword123!",
  "name": "Jan",
}'
```

### Pobierz Listę Użytkowników / Użytkownika
**Endpoint:**  
`GET /user/`
`GET /user/{user_id}`
**Opis:**  
Zwraca listę wszystkich użytkowników w systemie.

**Nagłówki:**
- `accept`: `application/json`
- `Authorization`: Bearer token JWT uzyskany podczas logowania.

**Przykładowe zapytanie:**
```bash
curl -X 'GET' \
  'http://localhost:8000/user/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token'
```

```bash
curl -X 'GET' \
  'http://localhost:8000/user/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token'
```

### Pobierz Listę Zadań
**Endpoint:**  
`GET /task/`

**Opis:**  
Zwraca listę wszystkich zadań w systemie.

**Nagłówki:**
- `accept`: `application/json`
- `Authorization`: Bearer token JWT uzyskany podczas logowania.

**Przykładowe zapytanie:**
```bash
curl -X 'GET' \
  'http://localhost:8003/task/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token'
```

### Tworzenie Zadania
**Endpoint:**  
`POST /task/`

**Opis:**  
Tworzy nowe zadanie w systemie.

**Wymagane zmienne (JSON w ciele zapytania):**
- `title`: Tytuł zadania (string, wymagany).
- `description`: Opis zadania (string, wymagany).
- `start_time`: Czas rozpoczęcia zadania w formacie ISO 8601 (string, wymagany).
- `end_time`: Czas zakończenia zadania w formacie ISO 8601 (string, wymagany).
- `hours_to_complete`: Liczba godzin potrzebna na wykonanie zadania (integer, wymagany).
- `user_id`: ID użytkownika przypisanego do zadania (integer, wymagany).

**Nagłówki:**
- `Content-Type`: `application/json`
- `Authorization`: Bearer token JWT uzyskany podczas logowania.

**Przykładowe zapytanie:**
```bash
curl -X 'POST' \
  'http://localhost:8003/task/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Nowe zadanie",
  "description": "Opis nowego zadania",
  "start_time": "2025-01-18T13:47:35.877Z",
  "end_time": "2025-01-18T15:47:35.877Z",
  "hours_to_complete": 2,
  "user_id": 1
}'
```

### Aktualizacja Zadania
**Endpoint:**  
`PUT /task/{id}`

**Opis:**  
Aktualizuje dane istniejącego zadania na podstawie jego ID.

**Wymagane zmienne (JSON w ciele zapytania):**
- `title`: Tytuł zadania (string, opcjonalny, do zaktualizowania).
- `description`: Opis zadania (string, opcjonalny, do zaktualizowania).
- `start_time`: Czas rozpoczęcia zadania w formacie ISO 8601 (string, opcjonalny, do zaktualizowania).
- `end_time`: Czas zakończenia zadania w formacie ISO 8601 (string, opcjonalny, do zaktualizowania).
- `hours_to_complete`: Liczba godzin potrzebna na wykonanie zadania (integer, opcjonalny, do zaktualizowania).
- `user_id`: ID użytkownika przypisanego do zadania (integer, opcjonalny, do zaktualizowania).

**Nagłówki:**
- `Content-Type`: `application/json`
- `Authorization`: Bearer token JWT uzyskany podczas logowania.

**Wymagana zmienna w URL:**
- `{id}`: ID zadania, które ma zostać zaktualizowane (np. `1`).

**Przykładowe zapytanie:**
```bash
curl -X 'PUT' \
  'http://localhost:8003/task/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Zaktualizowane zadanie",
  "description": "Zaktualizowany opis zadania",
  "start_time": "2025-01-18T14:00:00.000Z",
  "end_time": "2025-01-18T16:00:00.000Z",
  "hours_to_complete": 3,
  "user_id": 1
}'
```

### Pobierz Zadania Użytkownika
**Endpoint:**  
`GET /task/{user_id}`

**Opis:**  
Zwraca listę zadań przypisanych do konkretnego użytkownika na podstawie jego ID.

**Wymagane zmienne:**
- `{user_id}`: ID użytkownika, dla którego chcesz pobrać zadania (np. `1`).

**Opcjonalne zmienne query:**
- `task_id`: ID konkretnego zadania, jeżeli chcesz pobrać tylko jedno zadanie danego użytkownika (np. `1`).

**Nagłówki:**
- `accept`: `application/json`
- `Authorization`: Bearer token JWT uzyskany podczas logowania.

**Przykładowe zapytanie (wszystkie zadania użytkownika):**
```bash
curl -X 'GET' \
  'http://localhost:8003/task/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token'
```

### Pobierz Powiadomienia o Zadaniach
**Endpoint:**  
`GET /notification/task`

**Opis:**  
Zwraca listę powiadomień związanych z zadaniami w systemie.

**Nagłówki:**
- `accept`: `application/json`
- `Authorization`: Bearer token JWT uzyskany podczas logowania (jeśli wymagane jest uwierzytelnienie).

**Przykładowe zapytanie:**
```bash
curl -X 'GET' \
  'http://localhost:8004/notification/task' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer your_jwt_token'
```


