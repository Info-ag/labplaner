#Theoretischer Aufbau
Das Datenverwaltungsystem ist auf vier Tabellen aufgeteilt.
##Userdaten
Die Userdaten tabelle enthält
- UserID
- Die AgID's des Users
- Klarnamen
- Email
- Passworthash
- Salt

und ermöglicht die Ausgabe von einzelnen Elementen, als auch von ganzen Spalten, nach UserID, AgID, Klarnamen und Email.

##Userkalender
Die Userkalender Tabelle enthält
- UserID
- Verfügbarkeit an einem Bestimmten Datum

und ermöglicht die Außgabe von einzelnen Daten, Datengruppen, als auch ganzer Spalten,nach User und Datum.

##AG
Die AG Tabelle entält
- AgID
- UserID's der Mitglieder
- UserID's der Mentoren/Administratoren der jeweiligen AG

und ermöglicht die Ausgabe von einzelnen Daten, als auch ganzer Spalten und die Ausgabe von den AgID's einer jeweiligen UserID.

##Event
Die Event Tabelle enthält
- EventID
- AgID
- DateRange
- BestT
- Deadline

und ermöglicht die Ausgabe von einzelnen Daten, als auch ganzer Spalten, nach AgId und EventID.
