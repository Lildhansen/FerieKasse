# initiate
- mangler clean-up af denne fil
skal kun kunne initiate hvis excel-sheetet med feriekassen er tom - eller slettet
skal have alle holdene fra de 5 ligaer et eller andet sted - til indsætning i menuen
Der skal kunne vælges hold i menu for hver spiller / indsætte .txt-fil med holdene og spillerne i formatet:
**note: spillere må ikke indeholde ,** 
    spiller1:
    hold1,liga1,land1
    hold2,liga2,land2
    ...
    spiller2
    ... etc
denne .txt fil skal så genereres med spillerne, holdene, og URL i formatet:
    spiller1:
    hold1,URL1
    hold2,URL2
    ...
    spiller2:
    ... etc
~~et xlsx dokument skal genereres - med spillerne og holdene - i samme stil som "feriekasse 2"~~ (evt kunne den farve med landene/ligaerne som den gør nu)
~~lav .txt med datoer/uger der er covered~~
evt. mail med holdene til alle spillerne
# update
~~for hver liga~~
    ~~for hver kamp der ikke er talt point for~~
       ~~ gem info om kamp i match objekt~~
            ~~hjemmehold,udehold,mål scoret, mål imod, vinder/taber, (evt. målscorer for udehold/hjemmhold)~~
        ~~beregn point~~
            ~~vinder,taber,mål scoret,indbyrdes,egne hold~~
            ~~evt. hvis hold har vundet - skip den~~
                ~~medmindre målscorene skal gemmes.~~
            ~~hvis 2 spillerhold mod hinanden:~~
                ~~hvis begge hold i samme spille, point = 0~~
                ~~ellers, point *= 2~~
        ~~opdater .json - for hver liga~~
        indsæt point i spiller objekter (evt i lister så alle udregninger kan ses)
opdater datoer
skriv til excel
    sørg for at den først skal skrive til excel når den har alt info - så den ikke skal åbne og lukke dem hele tiden.
send mail
    hver uge/anden uge / måned
# remove
skal have en "are you sure you want to remove"
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
    - ~~indsættes i rigtig kolonne~~
- mail sendes ordentligt - rigtig vedhæftning, connection til SMTP, rigtig modtagere
- **Kan ikke teste for webdriver**

# hvornår / hvordan filerne skal køres
## initiate
    skal køre menuen hvis den .txt-fil med holdene og spillerne enten er tom eller ikke eksisterer 
        kan evt. også spørge om menuen skal opsættes, hvis ingen .txt-fil eksisterer/er tom
# extra shit:
    check danskerscoringer
    check specielt spillernavn scoring
    LeagueNationsDict fra constants kunne måske optimere/prettify noget stuff
    kunne laves så man kunne lave en sorteringfunktion - fx kun klubber med danskere - og så vil værdierne ændres
    makefil?
# optimeringsmuligheder:
når den skal finde holdene, skal den samle dem alle i lande, så den laver minimal søgninger til chrome
sørg for at lukke **ALLE** connections samt filer

# small todo
    fix casing
    add comments - til hver funktion
    måske en selvstændig class med forbindelse til webdriver
    lav folder til tests
    fix menu - både comments og mere 
        og hvordan kan de importere ud af filen

# comments needed
~~Util~~
~~WebdriverHelper~~ 
~~Team~~
~~player~~
~~Match~~
~~Main_update~~
~~Main_remove_feriekasse~~
~~Main_initiate~~
    


# naming conventions:
## general naming conventions:
    variables = camelCase
    functions = camelCase
    constants (defined globally) = MACRO_CASE
## class stuff:
    ClassName
    classAttributes
    classMethods

## file names
    main files = Main_snake_case
    ClassFiles = PascalCase
    other files = camelCase


# nice to haves:
- send mail (both when initiation and each week(or month or some defined timeframe))
- menu initiation



# md guide:
~~overstreg~~
*italic*
**bold**
`code here`
```python
def isCodeblock():
    return True
```
[link](www.thisisalink.com)