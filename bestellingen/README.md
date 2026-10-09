# 📋 Bestellingen — de portal van De Koekenbakker

De werkkant van de webshop: hier komen alle bestellingen live binnen, staat het bakbriefje
voor de week, en zet je het baklimiet. Alleen Zara komt erin.

**🔗 Live op:**
👉 https://dekoekenbakkerzara.nl/bestellingen/

De webshop zelf staat in de hoofdmap van deze repo. Ze praten met hetzelfde
Firebase-project.

---

## Wat je ziet

### Deze week
- **Baklimiet** — hoeveel koekjes er deze week besteld zijn, tegen het limiet dat je zelf
  zet. De webshop kijkt naar ditzelfde getal en zet de bestelknop op slot als de week vol is.
- **Bakbriefje** — het belangrijkste scherm: per smaak opgeteld wat er de oven in moet,
  over alle bestellingen van de week heen. Verrassingsboxen en gratis koekjes staan apart
  als "zelf uitkiezen", want daar bepaal jij de smaak.
- **Afhalen en bezorgen** — wie wanneer langskomt, gegroepeerd per tijdslot, en de
  bezorgadressen bij elkaar.

### Bestellingen
Alle bestellingen van de week, nieuwste eerst, met een filter per status. Tik een
bestelling open en je ziet de regels, het contactgegeven (met knoppen om te bellen, te
appen of te mailen), het afhaalmoment of adres en de opmerking.

Komt er een hele reeks tegelijk binnen — een groepsapp, een lijstje uit je hoofd — dan is
**Lijst invoeren** sneller. Je plakt de tekst er in de vorm die je toch al gebruikt in:

```
Merel Dank:
2x chocolate chip 3x stroopwafel 1x oreo

Joze Keus:
2x stroopwafel 1x lotus 1x chocolate chip
```

Een naam met een dubbele punt begint een nieuwe bestelling; de koekjes mogen erachter of
eronder staan. De namen van de smaken mag je schrijven zoals je ze zegt (*kinder chocolade*,
*biscoff*, *choco chip*), en regels als "4 verschillende" slaat hij gewoon over. Met
**Nakijken** zie je eerst per persoon wat hij ervan maakt, wat het kost en wat hij niet
begreep; pas daarna maak je ze aan. Kanaal en status kies je één keer voor de hele lijst, en
de weekteller gaat in één keer omhoog.

Bovenaan staat **+ Bestelling toevoegen**, voor alles wat buiten de webshop om binnenkomt:
mondeling, via Instagram, een appje. Je vult een naam in, tikt de koekjes bij elkaar met de
plusknoppen, en het bedrag rekent zichzelf uit — inclusief de combideal van de webshop
(vier losse koekjes voor € 12, bij elke volgende vier opnieuw). De verrassingsboxen hebben
hun eigen prijs: € 12, € 15 of € 18 voor 4, 5 of 6 koekjes. Aanpassen mag, bijvoorbeeld als je een
andere prijs hebt afgesproken. Elke bestelling heeft ook een **kanaal** (Website,
Mondeling, WhatsApp, Instagram, …), zodat je ziet waar je klanten vandaan komen; op het
overzicht staat dat per week bij elkaar geteld. Wat via de webshop binnenkomt heet
vanzelf "Website".

Bestaande bestellingen pas je aan met **Bewerken** — handig als iemand er nog twee bij wil,
of als een adres verandert. Daarnaast staat er **Verwijderen**. Daar schuift een
eigen schermpje in beeld — geen browserpopup — waarin nog even staat om wie het gaat,
hoeveel koekjes het zijn en wat de status is; pas na *Ja, verwijderen* gebeurt er iets. Verwijderen is definitief;
wil je een bestelling alleen afzeggen maar wel kunnen terugvinden, zet hem dan op
*Geannuleerd* in het stappenlijstje.
Het baklimiet rekent in alle gevallen mee: hoog je een bestelling op, zeg je 'm af of
verwijder je 'm, dan verschuift de weekteller vanzelf — ook als die bestelling in een andere
week stond.

Een bestelling loopt langs vijf stappen. De knop zet hem telkens één stap verder; met het
keuzelijstje ernaast spring je naar elke stap, ook terug — handig als je te vroeg op
*Gebakken* hebt getikt. Ook *Geannuleerd* zit in dat lijstje.

**Nieuw → Nog bakken → Gebakken → Ingepakt → Opgehaald**

*Nieuw* betekent: net binnengekomen en nog niet door jou bekeken — die staan met een
oranje rand bovenaan. Zodra je 'm bevestigt staat hij op *Nog bakken* en weet je dat hij
op de lijst voor vrijdag staat. Bij een bezorgbestelling heet de laatste stap vanzelf
*Bezorgd* in plaats van *Opgehaald*. Een stap terug kan ook, en annuleren kan altijd — het
aantal koekjes gaat dan automatisch weer van de weekteller af.

### Zoeken en filteren
Boven de lijst staat een zoekveld en een keuzelijst met kanalen. Zoeken kijkt naar naam,
bestelnummer, telefoonnummer, adres, afhaalmoment, opmerking, kanaal én de smaken in de
bestelling, en doet dat **over alle weken** — anders vind je die bestelling van vorige
maand nooit meer terug. Bij een treffer uit een andere week staat het weeknummer erbij.
Maak je het zoekveld leeg, dan zie je weer gewoon de week die je bekijkt. De statusknoppen
eronder en het kanaalfilter werken op allebei.

### Instellingen
Drie dingen:

- **Meldingen** aanzetten, met een proefmelding om het te testen.
- **Deze week**: hoeveel koekjes je aankunt, en een knop om bestellingen te sluiten — dan
  zegt de webshop dat de week vol zit. Nam je een bestelling buiten de site om aan, dan kun
  je de teller met de hand bijstellen.
- **Bakdag en bestellen**: op welke dag en hoe laat de oven aangaat, en tot wanneer klanten
  kunnen bestellen. De webshop neemt dat meteen over in de aftelklok en de teksten, en
  schuift bestellingen na het sluitmoment door naar de week erna. Met het vinkje zet je
  dezelfde tijden ook voor de komende vier weken; laat je het uit, dan geldt het alleen
  voor de week die je bekijkt.

Hoeveel er nog vrij is zie je alleen hier. Bezoekers van de webshop krijgen dat getal pas
te zien als er nog tien of minder over zijn én hun mandje groter is.

De weken staan los van elkaar: met de pijltjes bovenin blader je naar de vorige of
volgende week, inclusief de bestellingen en het limiet van die week.

---

## Zo zet je het aan

Je hebt één Firebase-project nodig voor de webshop én de portal. Gratis, en ruim binnen de
gratis grens bij dit soort aantallen.

1. **Project maken** — ga naar [console.firebase.google.com](https://console.firebase.google.com),
   maak een project (bijvoorbeeld `de-koekenbakker`). Google Analytics mag je uitzetten.
2. **Web-app toevoegen** — klik op het `</>`-icoontje, geef de app een naam en kopieer het
   `firebaseConfig`-blok dat je krijgt.
3. **Config invullen** — plak dat blok in **twee** bestanden, op de plek waar nu `null`
   staat: [`../firebase-config.js`](../firebase-config.js) en
   [`firebase-config.js`](firebase-config.js) hiernaast. Zorg dat `ruimte` in beide
   hetzelfde woord is.
4. **Inloggen aanzetten** — Console → Build → Authentication → Get started →
   *E-mail/wachtwoord* aanzetten. Voeg daarna onder *Users* je eigen account toe met een
   e-mailadres en wachtwoord. Daarmee log je in de portal in.
5. **Database maken** — Console → Build → Firestore Database → Create database →
   productiemodus, regio `europe-west` (bijvoorbeeld België of Frankfurt).
6. **Regels plakken** — open [`firestore.rules`](firestore.rules), zet je eigen e-mailadres
   in `bakkerMails()`, en plak het hele bestand in Console → Firestore → Rules → Publish.

Klaar. Vanaf dan wordt elke bestelling opgeslagen, telt het weeklimiet vanzelf mee over
alle klanten heen, en zie je alles hier binnenkomen.

> De sleutel in `firebase-config.js` hoort openbaar te zijn bij een web-app — dat is geen
> wachtwoord. Wat je gegevens beschermt zijn de regels uit `firestore.rules`: die zorgen
> dat een klant wél een bestelling kan plaatsen, maar die van een ander nooit kan lezen.

---

## Hoe het onder water werkt

Twee laatjes in Firestore, allebei onder `koekenbakker/<ruimte>/`:

| Waar | Wat erin staat | Wie mag wat |
|---|---|---|
| `bestellingen/{id}` | naam, contact, regels, aantal, bedrag, levering, moment of adres, opmerking, status | iedereen mag er één **aanmaken**; alleen jij mag lezen en wijzigen |
| `weken/{2026-W39}` | `besteld`, `limiet`, `open` | iedereen mag **lezen** (alleen aantallen, geen klantgegevens) en de teller ophogen; alleen jij mag de rest zetten |

De webshop hoogt bij een bestelling de weekteller op met het aantal koekjes. De regels
staan toe dat die teller alleen omhoog gaat, met maximaal 40 tegelijk — zo kan niemand hem
leegtrekken of het limiet veranderen.

---

## Wat je moet weten

- **Spam is mogelijk.** Iedereen kan een bestelling aanmaken; dat hoort ook zo, anders kan
  een klant niets bestellen. Komt er onzin binnen, dan gooi je die hier weg en corrigeer je
  de teller. Wordt het een probleem, dan is Firebase App Check de volgende stap.
- **Meldingen** krijg je zodra je ze in de portal aanzet (Instellingen → *Meldingen
  aanzetten*): bij elke nieuwe bestelling een melding met naam, aantal en bedrag, plus een
  kort belletje. Dat werkt zolang de portal openstaat of op de achtergrond draait — ook als
  app op je beginscherm. Is je telefoon helemaal afgesloten, dan komt de melding zodra je
  de portal weer opent.
- **Zet de portal op je beginscherm.** Android: menu → *App installeren*. iPhone: Deel →
  *Zet op beginscherm* — daar is het zelfs verplicht, want zonder installatie laat iOS
  geen meldingen toe.
- **Bellen, WhatsApp en Mailen** bij een bestelling zetten meteen een bevestiging klaar:
  hoi met de voornaam, het bestelnummer, wat erin zit, wanneer het opgehaald kan worden en
  de link waarmee diegene zelf kan volgen hoe ver zijn koekjes zijn. Zo heeft een klant zijn
  bestelnummer in zijn eigen gesprek staan en raakt hij het niet kwijt.
- **Het getal op het tabblad Bestellingen** is hoeveel bestellingen er deze week zijn,
  zonder de afgezegde. Zit er iets nieuws bij dat je nog niet hebt bekeken, dan kleurt dat
  getal op.
- **Het weekbericht** komt elke donderdag om 20:00 per mail, met het bakbriefje en alle
  bestellingen van die week. Dat is de betrouwbare vangnet-melding: die komt binnen ook
  als de portal dicht is. Zie `.github/workflows/weekbericht.yml`.
- **Bakoverzicht mailen** doet hetzelfde op een moment dat jou uitkomt. De knop staat boven
  de bestellingen en zet het hele overzicht — wat er gebakken moet worden, en daarna per
  klant wat hij besteld heeft — klaar in je eigen mailprogramma, met jouw adres er al in.
  Versturen doe je zelf met één tik; een website mag niet ongevraagd mail de deur uit doen,
  dus dat laatste zetje moet van jou komen. De tekst staat meteen ook op je klembord, handig
  als je hem liever in een appje plakt.
- **Betalen gaat buiten de site om**, bij het ophalen.
