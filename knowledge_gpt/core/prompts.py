# flake8: noqa
from langchain.prompts import PromptTemplate

template = """Fyll ut skjemaet ved å bruke informasjonen i de vedlagte dokumentene som referanse. ALLTID inkluder en "KILDER" seksjon i svaret ditt som inkluderer bare det minimale settet med kilder som trengs for å svare på spørsmålet. Hvis du ikke kan svare på spørsmålet, angi rett og slett at du ikke vet. Vær kreativ, skriv detaljert og omfattende. Prosjektet skal være inspirert fra konteksten / kilden, og være dypt kreativ, interresant og unik. bruk markdown formattering, '## ... " og  '# ...' indikerer overskrift. Prosjektbeskrivelse skal inneholde 4000< tegn. Kunstnerisk målsetting skal inneholde 3000< tegn. erstatt [tittel] med et passende navn på prosjektet.

## SKJEMA: Fond for lyd og bilde prosjektstøtte
=========
# tittel
Sjanger:
Medvirkende:

## Kunstnerisk målsetting:


## Prosjektbeskrivelse:

## Gjennomføringsplan:
Har du tidligere søkt Fond for lyd og bilde til dette prosjektet? (Ja/Nei):

Prosjektperiode Fra dato:
Til dato:
Aktivitet Fra dato:
Til dato:
Sammendrag av prosjektet ( 750 tegn):

Budsjett:

Søknadsbeløp:
Andre tilskudd:
Offentlige tilskudd:
Andre inntekter:
Vedlegg.
=========
SLUTTSVAR:
SOURCES: 1-32

BESKRIVELSE: {question}
=========
KONTEKST: {summaries}
=========
SLUTTSVAR:
"""

STUFF_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"]
)
