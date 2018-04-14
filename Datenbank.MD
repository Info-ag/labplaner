# Theoretischer Aufbau
Das Datenverwaltungsystem ist auf vier Tabellen aufgeteilt.
## Userdaten
Die Userdaten Tabelle enthält
- UserID
- Vorname
- Nachname
- Email
- Passworthash (gesaltet)
- Geburtstag
- AgID's des Users
- Wahrheitswert Admin
- Wahrheitswert Mentor
- Wahrheitswert Teilnehmer

und ermöglicht die Ausgabe von einzelnen Elementen, als auch von ganzen Spalten, nach UserID, AgID, Klarnamen und Email. Zum Abgleich von Hash mit Passwort wird die Library bcrypt benutzt, das Abspeichern des Saltes ist daher nicht nötig. Mittels der Wahrheitswerte werden die Berechtigungen angepasst.

## Userkalender
Die Userkalender Tabelle enthält
- UserID

Der Userkalender kann erst nach Absprache mit dem Algorithmus konzipiert werden.

## AG (project group)
Die AG Tabelle entält
- Name der AG
- AgID
- UserID's der Mitglieder
- UserID's der Mentoren der jeweiligen AG

und ermöglicht die Ausgabe von einzelnen Daten, als auch ganzer Spalten und die Ausgabe von den AgID's einer jeweiligen UserID.

## Event
Die Event Tabelle enthält
- EventID

Die Eventtabelle kann erst nach Absprache mit dem Algorithmus konzipiert werden.
