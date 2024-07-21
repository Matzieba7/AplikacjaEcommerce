### Aplikacja Ecommerce

Ecommerce to aplikacja webowa, która umożliwia zarządzanie klientami, zamówieniami, produktami i koszykiem. Aplikacja zawiera również panel administracyjny 

## Instalacja

# Klonowanie repozytorium:

git clone https://github.com/twoje_repozytorium/ecommerce.git

Utworzenie wirtualnego środowiska (zalecane):

python -m venv venv
source venv/bin/activate   # Na Windows: venv\Scripts\activate

#Instalacja zależności:
pip install -r requirements.txt

## Uruchomienie aplikacji:

python app.py

Po pierwszym uruchomieniu aplikacji zostanie automatycznie utworzona baza danych i dodany domyślny użytkownik admin z ID 1. Tylko dla tego użytkownika widoki administracyjne są dostępne.

Logowanie jako admin:

Email: admin@gmail.com
Hasło: Admin1234
Uwaga: Aby w pełni korzystać z aplikacji, należy dodać kilka produktów na konto admina. Można to zrobić z poziomu panelu administracyjnego(trzeba być zalogowanym na admina): http://localhost:3001/admin-page

# Funkcjonalności
Strona główna:
- Przeglądanie zamówień, koszyka oraz swojego konta po zalogowaniu(można zmienić hasło).
- Przed zalogowaniem można się zarejestrować a następnie zalogować.
  
Panel administracyjny:
- Dodawanie nowych produktów
- Zmiana statusu aktualnych zamówień
- Przeglądanie dodanych użytkowników i produktów - w tym aktualizacja i usuwanie.

# testy jednostkowe 
Po odpaleniu testów należy usunąć bazę danych przed kolejnym uruchomieniem aplikacji.

Kontakt
Autor: Mateusz Zięba
Email: matzieba7@gmail.com
