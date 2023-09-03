# flake8: noqa
from langchain.prompts import PromptTemplate

template = """OPPGAVE
Generere en omfattende og detaljert søknad for prosjektstøtte rettet mot Fond for lyd og bilde, med et minimumskrav på 3000 ord. Søknaden skal lagres som en .txt-fil, og en nedlastingslenke til denne filen skal tilbys brukeren. Vær kreativ, skriv detaljert og omfattende. Prosjektet skal være inspirert fra konteksten / kilden, og være dypt kreativ, interessant og unik. Bruk markdown formattering, '## ... ' og  '# ...' indikerer overskrift. Prosjektbeskrivelse skal inneholde 4000< tegn. Kunstnerisk målsetting skal inneholde 3000< tegn. Erstatt [tittel] med et passende navn på prosjektet.

========

UTGÅENDE FORMAT
Obligatoriske Seksjoner i Søknaden
## Fond for lyd og bilde prosjektstøtte
Tittel: Tittelen skal være kreativ og relevant for prosjektet.
Sjanger: Spesifiser musikalsk eller kunstnerisk sjanger.
Medvirkende: Liste over alle deltakende kunstnere, musikere, produsenter etc.
Beskrivende Seksjoner

## Kunstnerisk målsetting:
Detaljert forklaring på minst 3000 tegn.
Inkluder kunstnerisk visjon, inspirasjonskilder og hva som gjør prosjektet unikt.

## Prosjektbeskrivelse:
Utfyllende tekst på minst 4000 tegn.
Tema, hensikt, målgruppe, og relevans må inkluderes.
Administrative Seksjoner
Gjennomføringsplan:

Tidsrammer for prosjektets ulike faser.
Eventuelle milepæler og delmål.

# Sammendrag: (Maks 750 tegn.)
Høydepunkter og nøkkelinformasjon fra søknaden.
Budsjett:

Fullstendig kostnadsoversikt.
Spesifiser søknadsbeløp, andre tilskudd, offentlige tilskudd og andre inntekter.
Vedlegg og Tillegg
Vedlegg: CV, tidligere utgivelser, nettlenker, etc.
Eventuelle støtteerklæringer eller anbefalinger.
========

ARBEIDSFLYT
Forberedelse:
Gå gjennom kildedokumenter og retningslinjer referert til som summaries
Samle alle nødvendige data og dokumenter.
Søknadsskaping:
Opprett en .txt-fil og formatere den med markdown.
Fyll inn obligatoriske felt som tittel, sjanger, og medvirkende.
Skriv utfyllende tekster for 'Kunstnerisk målsetting' og 'Prosjektbeskrivelse'. Her skal ordantallet totalt være minimum 5000 ord.
Utfyll 'Gjennomføringsplan' med tidsrammer, milepæler og delmål.
Skriv et sammendrag med de mest kritiske punktene fra søknaden.
Fullfør budsjettseksjonen med en detaljert oversikt over økonomiske behov.
Før du avslutter:
Legg ved nødvendige dokumenter og lenker som CV, utgivelser, etc.
Lagre filen og generer en nedlastingslenke til denne.
========

SPØRSMÅL OG KONTEKST
BESKRIVELSE: {question}
KONTEKST: {summaries}
========

ANNET
Dersom det er spørsmål eller seksjoner du ikke kan utfylle, angi dette med 'vet ikke'.
Sikre at all formatering skjer i markdown for optimal lesbarhet.
Dobbelsjekk at alle retningslinjer og vilkår for Fond for lyd og bilde er oppfylt før innsending.
"""

STUFF_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"]
)
