# Task-manager


## Opis projektu
Aplikacja jest systemem zarządzania modułami, który obsługuje użytkowników, wydarzenia oraz powiadomienia. Jest zbudowana w oparciu o mikrousługi i pozwala na włączanie i wyłączanie wybranych modułów.

## Funkcjonalności
- **Zarządzanie użytkownikami**: Rejestracja, logowanie, role i uprawnienia.
- **Obsługa wydarzeń**: Tworzenie, edycja i usuwanie wydarzeń.
- **System powiadomień**: Wysyłanie notyfikacji użytkownikom.
- **Kalendarz**: Wyświetlanie wydarzeń i zarządzanie kategoriami.
- **Eksport/import danych**: Obsługa formatów JSON i CSV.

## Wymagania systemowe
- Python 3.10+
- Docker i Docker Compose
- PostgreSQL jako baza danych
- Apache Kafka do komunikacji między modułami

## Instalacja
1. Sklonuj repozytorium:
   ```bash
   git clone <URL_REPOZYTORIUM>
   cd <NAZWA_FOLDERU>
   ```
2. Uruchom Dockera:
   ```bash
   docker-compose up -d
   ```
3. Ustaw zmienne środowiskowe (plik `.env`):
   - Przykład konfiguracji:
     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/dbname
     KAFKA_BROKER=kafka:9092
     ```

## Uruchomienie
- Backend uruchomi się automatycznie w kontenerze Docker na porcie `8000`.
- Aby uruchomić frontend (jeśli dotyczy), przejdź do odpowiedniego katalogu i wykonaj:
  ```bash
  npm install
  npm start
  ```

## Struktura projektu
- `auth/`: Moduł uwierzytelniania i zarządzania użytkownikami.
- `task/`: Moduł zarządzania wydarzeniami.
- `notification/`: Moduł obsługi powiadomień.
- `core/`: Rdzeń systemu zarządzający komunikacją między modułami.

## Przykłady użycia
- **Rejestracja użytkownika**:
  ```bash
  curl -X POST http://localhost:8000/users/register -H "Content-Type: application/json" -d '{"username": "jan", "password": "haslo123"}'
  ```
- **Tworzenie wydarzenia**:
  ```bash
  curl -X POST http://localhost:8000/events -H "Content-Type: application/json" -d '{"title": "Spotkanie", "category": "Praca", "date": "2025-01-30"}'
  ```

## Autorzy
Projekt opracowany przez PC & PŁ.

## Informacje dodatkowe
- W razie problemów skontaktuj się z administratorem.
- Dokumentacja techniczna znajduje się w folderze `docs/`.
