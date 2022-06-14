# initiate
- mangler clean-up af denne fil
skal kun kunne initiate hvis excel-sheetet med feriekassen er tom - eller slettet
skal have alle holdene fra de 5 ligaer et eller andet sted - til indsætning i menuen
Der skal kunne vælges hold i menu for hver spiller / indsætte .txt-fil med holdene og spillerne i formatet:
evt. mail med holdene til alle spillerne
# update
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
- korrekt pointtælling
- korrekt excelskrivning
- mail sendes ordentligt - rigtig vedhæftning, connection til SMTP, rigtig modtagere
- **Kan ikke teste for webdriver**

# hvornår / hvordan filerne skal køres
## initiate
    skal køre menuen hvis den .txt-fil med holdene og spillerne enten er tom eller ikke eksisterer 
        kan evt. også spørge om menuen skal opsættes, hvis ingen .txt-fil eksisterer/er tom
# extra shit:
    LeagueNationsDict fra constants kunne måske optimere/prettify noget stuff
    kunne laves så man kunne lave en sorteringfunktion - fx kun klubber med danskere - og så vil værdierne ændres
# optimeringsmuligheder:
sørg for at lukke **ALLE** connections samt filer

# small todo
    fix casing
    add comments - til hver funktion
    fix menu - både comments og mere 
        og hvordan kan de importere ud af filen

# comments needed

    


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



Thor                             Nielsen              Pølle                   Thuge                Kim
Chelsea                          Tottenham          United               Leicester           Newcastle
Leverkusen                  Frankfurt               Wolfsburg           Freiburg                Leipzig
Sociedad                        Villareal            Atletico             Betis                  Sevilla
Napoli                              Fiorentina        Roma                 Juventus             Lazio
Viborg                             Randers            AaB                     Brøndby            Silkeborg