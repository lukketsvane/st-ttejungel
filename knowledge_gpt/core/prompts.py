# flake8: noqa
from langchain.prompts import PromptTemplate


template = """Fyll ut skjemaet ved å bruke informasjonen i de vedlagte dokumentene som referanse. ALLTID inkluder en "KILDER" seksjon i svaret ditt som inkluderer bare det minimale settet med kilder som trengs for å svare på spørsmålet. Hvis du ikke kan svare på spørsmålet, angi rett og slett at du ikke vet. Vær kreativ, skriv detaljert og omfattende. Prosjektet skal være inspirert fra konteksten / kilden, og være dypt kreativ, interessant og unik. Bruk markdown formattering, '## ... " og  '# ...' indikerer overskrift. Prosjektbeskrivelse skal inneholde 4000< tegn. Kunstnerisk målsetting skal inneholde 3000< tegn. Erstatt [tittel] med et passende navn på prosjektet.

## SKJEMA: Fond for lyd og bilde prosjektstøtte
=========
# tittel
**[Tittel på prosjektet]**
Sjanger: [Angi sjangeren]
Medvirkende: [Liste over medvirkende]

## Kunstnerisk målsetting:
[Innehold en beskrivelse av de kunstneriske målene du ønsker å oppnå med dette prosjektet. Gjør det detaljert og engasjerende.]

## Prosjektbeskrivelse:
[Her beskriver du prosjektet ditt mer grundig. Gi leseren en dypere forståelse av hva prosjektet handler om, dets formål og betydning.]

## Gjennomføringsplan:
Har du tidligere søkt Fond for lyd og bilde til dette prosjektet? (Ja/Nei):
[Angi om du har søkt støtte tidligere]

Prosjektperiode Fra dato:
Til dato:
Aktivitet Fra dato:
Til dato:

Sammendrag av prosjektet ( 750 tegn):
[Kort oppsummering av prosjektet på opptil 750 tegn]

Budsjett:
[Detaljert budsjett for prosjektet]

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
