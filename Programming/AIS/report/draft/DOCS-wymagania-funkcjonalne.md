[https://github.com/Artur-Romaniuk/ais](https://github.com/Artur-Romaniuk/ais)  
[https://www.overleaf.com/project/67e843e5c78b52b01a88211a](https://www.overleaf.com/project/67e843e5c78b52b01a88211a)

System e-Toll do zbierania danych na temat ruchu pojazdów po polskich drogach i naliczania należności za przejazdy.

Rezultatem projektu powinien być dokument PDF, zawierający następujące elementy:

1. Wymagania funkcjonalne.  
   * pogrupowana lista wymagań  
   * zidentyfikować jeden kluczowy proces biznesowy i szczegółowo ten proces zdefiniować. Definicja procesu to po prostu:  
     * cel procesu  
     * stan początkowy  
     * stan końcowy  
     * kroki procesu, z uwzględnieniem sytuacji wyjątkowych.  
2. Wymagania niefunkcjonalne.  
   * geograficzna skala działania  
   * liczba obsługiwanych klientów  
   * liczba obsługiwanych zdarzeń biznesowych w określonym czasie (na godzinę/dziennie/miesięcznie etc.)  
   * wymagania wydajnościowe  
   * wymagania niezawodnościowe  
   * wymagania bezpieczeństwa  
   * ....  
3. Projekt systemu w postaci modelu C4 (https://c4model.com/)  
   * wystarczą 3 pierwsze poziomy : context, containers, components, nie wymagam poziomu code  
   * diagram dynamiczny(dynamic diagram) realizujący opisany w wymaganiach proces biznesowy  
   * diagram wdrożenia (deploymen diagram)  
4. Dyskusja zastosowanych wzorców i/lub taktyk architektonicznych \- w celu wyboru odpowiednich rozwiązań należy się odwołać do wymagań funkcjonalnych i niefunkcjonalnych.  
5. Decyzje architektoniczne w postaci modelu MAD 2.0

# Wymagania funkcjonalne

\# Wymagania funkcjonalne dla Systemu e-Toll

\#\# Kluczowy proces biznesowy: Naliczanie i pobieranie opłat za przejazd

\#\#\# 1\. Cel procesu

1) Wykrywanie pojazdów na płatnych odcinkach dróg  
2) Naliczanie należności zgodnie z taryfami   
3) Pobieranie opłat od użytkowników

\#\#\# 2\. Stan początkowy  
Pojazd niezarejestrowany w systemie jako znajdujący się na płatnym odcinku drogi, z kontem użytkownika posiadającym określony stan środków (prepaid) lub limitem kredytowym (postpaid).

\#\#\# 3\. Stan końcowy  
Prawidłowo naliczona i pobrana opłata za przejazd, zaksięgowana w systemie finansowym, z wygenerowanym potwierdzeniem dla użytkownika oraz aktualizacją stanu konta.

\#\#\# 4\. Kroki procesu  
1\. Identyfikacja pojazdu wjeżdżającego na płatny odcinek (poprzez urządzenie OBU, aplikację mobilną lub kamery ANPR) \[Dla redundancji, im więcej systemów tym większa szansa na identyfikację)  
2\. Zebranie danych o pojeździe (kategoria, klasa emisji spalin, masa)  
3\. Rozpoczęcie śledzenia przejazdu i rejestracja czasu wjazdu  
4\. Monitorowanie trasy przejazdu przez punkty kontrolne  
5\. Identyfikacja zjazdu z płatnego odcinka  
6\. Obliczenie należności na podstawie przebytej trasy i charakterystyki pojazdu  
7\. Weryfikacja dostępności środków na koncie użytkownika  
8\. Pobranie opłaty z konta użytkownika  
9\. Wygenerowanie potwierdzenia transakcji  
10\. Aktualizacja salda konta użytkownika

\*\*Obsługa sytuacji wyjątkowych:\*\*  
\- Jeśli identyfikacja pojazdu nie jest możliwa: uruchomienie procedury rejestracji incydentu z dokumentacją wizualną (zdjęcia niezidentyfikowanego pojazdu)  
\- W przypadku niewystarczających środków na koncie:

1) Zablokowanie konta do momentu zapłacenia  
2) W przypadku braku zapłaty w określonym czasie, uruchomienie procedury windykacyjnej

\- Przy awarii urządzenia OBU: automatyczne przełączenie na identyfikację przez system kamer ANPR  
\- W razie przerwy w komunikacji: lokalne buforowanie danych i synchronizacja po przywróceniu łączności  
\- Jeśli zidentyfikowano omijanie bramek:

1. Poinformowanie użytkownika  
2. uruchomienie procedury kontrolnej   
3. naliczenie kary

\#\# Wymagania funkcjonalne

1\. \*\*System rejestracji użytkowników\*\* \- System musi umożliwiać rejestrację nowych użytkowników z weryfikacją tożsamości, zbieraniem danych o pojazdach (w tym masa, klasa emisji, kategoria) oraz wyborem metody płatności (prepaid lub postpaid).

2\. \*\*Moduł geolokalizacji pojazdów\*\* \- System musi określać pozycję pojazdów z dokładnością do 10 metrów, wykorzystując dane GPS z urządzeń OBU lub aplikacji mobilnej, aktualizowane nie rzadziej niż co 30 sekund podczas przejazdu.

3\. \*\*System rozpoznawania tablic rejestracyjnych (ANPR)\*\* \- System musi identyfikować pojazdy poprzez kamery ANPR z dokładnością co najmniej 98% w różnych warunkach pogodowych i oświetleniowych, jako dopełnienie jeśli wszystkie systemy działają poprawnie lub alternatywa dla urządzeń OBU w razie awarii..

4\. \*\*Elastyczny system taryfowy\*\* \- System musi obsługiwać zróżnicowane taryfy opłat w zależności od: typu pojazdu, masy całkowitej, klasy emisji spalin, pory dnia, dnia tygodnia oraz stopnia zatłoczenia drogi.

5\. \*\*Moduł rozliczeń i płatności\*\* \- System musi obsługiwać różne metody płatności (karty płatnicze, przelewy, płatności mobilne, blik) z możliwością automatycznego doładowania konta prepaid oraz wystawiania faktur elektronicznych zgodnych z przepisami prawa. 

6\. \*\*System powiadomień dla użytkowników\*\* \- System musi wysyłać automatyczne powiadomienia do użytkowników (aplikacja, mail \+ sms) o: niskim stanie konta, zbliżającym się terminie płatności, dokonanych transakcjach oraz zmianach w taryfach i regulaminie.

7\. \*\*Moduł raportowania i analityki\*\* \- System musi generować raporty dotyczące natężenia ruchu, generowanych przychodów, incydentów oraz efektywności egzekwowania opłat, z możliwością eksportu danych w formatach CSV i PDF.

8\. \*\*System wykrywania naruszeń\*\* \- System musi identyfikować próby obejścia opłat (np. manipulacja urządzeniem OBU, podawanie fałszywych danych o pojeździe) i automatycznie uruchamiać procedury weryfikacyjne.

9\. \*\*Portal samoobsługowy dla użytkowników\*\* \- System musi udostępniać portal internetowy oraz aplikację mobilną umożliwiającą użytkownikom zarządzanie kontem, przeglądanie historii przejazdów i opłat, generowanie raportów oraz aktualizację danych pojazdu.

10\. System musi umożliwiać ręczną korektę naliczonej opłaty przez operatora w przypadku zgłoszenia błędu przez użytkownika. Zakładając, że system źle naliczył opłatę np. Użytkownik został obciążony za trasę, której nie przejechał lub przypisano niewłaściwą kategorię pojazdu. Użytkownik zgłasza błąd do obsługi systemu. W takim przypadku operator musi mieć możliwość ręcznej korekty naliczonej opłaty np. Anulowanie opłaty, zmniejszenie jej lub ponowne przeliczenie, jeżeli zgłoszenie użytkownika okaże się zasadne. Zasadność zgłoszenia musi być weryfikowalna poprzez fizyczne zdjęcia pojazdu


---

[Wymagania niefunkcjonalne](DOCS-wymagania-niefunkcjonalne.md) zostały
wydzielone do osobnego pliku, aby zmieścić się w limicie 250 wierszy.
