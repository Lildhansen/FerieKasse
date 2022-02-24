# initiate
skal have alle holdene fra de 5 ligaer et eller andet sted
Der skal kunne vælges hold i menu for hver spiller / indsætte .txt-fil med holdene og spillerne i formatet:
    spiller1:
    hold1,liga1,land1
    hold2,liga2,land2
    ...
    spiller2
    ... etc
denne .txt fil så enten konverteres (eller en ny skal genereres) med spillerne, holdene, og URL i formatet:
    spiller1:
    hold1,URL1
    hold2,URL2
    ...
    spiller2:
    ... etc
et xlsx dokument skal genereres - med spillerne og holdene - i samme stil som "feriekasse 2" (evt kunne den farve med landene/ligaerne som den gør nu)
lav .txt med datoer/uger der er covered
evt. mail med holdene til alle spillerne
# update
for hver spiller
    for hvert hold
        for hver kamp der ikke er talt point for
            gem info om kamp i match objekt
                hjemmehold,udehold,mål scoret, mål imod, vinder/taber, (evt. målscorer for udehold/hjemmhold)
            beregn point
                vinder,taber,mål scoret,indbyrdes,egne hold
                evt. hvis hold har vundet - skip den
                    medmindre målscorene skal gemmes.
                    på den måde sikrer vi at indbyrdes hold ikke tælles for begge hold
    opdater datoer
    skriv til excel
        sørg for at den først skal skrive til excel når den har alt info - så den ikke skal åbne og lukke dem hele tiden.
    send mail
# remove
clear:
    excel sheet
    players and teams / players and teams and links
ikke clear:
    teams.txt

# tests:
- rigtig URL for holdene / kampene findes
- .txt format generes i rigtig format (find linjer og tjek, samt sørg for der ikke er extra \n)
- korrekt pointtælling
- korrekt excelskrivning
- mail sendes ordentligt - rigtig vedhæftning, connection til SMTP, rigtig modtagere


# hvornår / hvordan filerne skal køres
## initiate
    skal køre menuen hvis den .txt-fil med holdene og spillerne enten er tom eller ikke eksisterer 
        kan evt. også spørge om menuen skal opsættes, hvis ingen .txt-fil eksisterer/er tom
# extra shit:
    check danskerscoringer
    check specielt spillernavn scoring


# optimeringsmuligheder:
når den skal finde holdene, skal den samle dem alle i lande, så den laver minimal søgninger til chrome
sørg for at lukke **ALLE** connections samt filer

# small todo
    fix casing
    add comments - til hver funktion
    













# md guide:
~~overstreg~~
*italic*
**bold**
`code here`
```python
def thisIsCodeblock():
    return True
```
[link](www.thisisalink.com)
