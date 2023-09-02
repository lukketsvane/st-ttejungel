from typing import Any, List
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from knowledge_gpt.core.prompts import STUFF_PROMPT
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from knowledge_gpt.core.embedding import FolderIndex
from knowledge_gpt.core.debug import FakeChatModel
from pydantic import BaseModel


class AnswerWithSources(BaseModel):
    answer: str
    sources: List[Document]


def query_folder(
    query: str,
    folder_index: FolderIndex,
    return_all: bool = False,
    model: str = "openai",
    **model_kwargs: Any,
) -> AnswerWithSources:
    """Spør en mappeindeks for et svar.

    Args:
        spørsmål (str): Spørsmålet å søke etter.
        mappeindeks (FolderIndex): Indeksen av mappen å søke i.
        returner_alle (bool): Om alle dokumenter fra indekseringen skal returneres eller
        bare kildene til svaret.
        modell (str): Modellen som skal brukes for å generere svaret.
        maks_token (int): Maksimalt antall token for den genererte teksten.
        **modell_kwargs (Any): Nøkkelordargumenter for modellen.

    Returns:
        SvarMedKilder (AnswerWithSources): Svaret og kildedokumentene.
    """

    supported_models = {
        "openai": ChatOpenAI,
        "debug": FakeChatModel,
    }

    if model in supported_models:
        llm = supported_models[model](**model_kwargs)
    else:
        raise ValueError(f"Model {model} not supported.")

    chain = load_qa_with_sources_chain(
        llm=llm,
        chain_type="stuff",
        prompt=STUFF_PROMPT,
    )

    relevant_docs = folder_index.index.similarity_search(query, k=5)
    result = chain(
        {"input_documents": relevant_docs, "question": query}, return_only_outputs=True
    )
    sources = relevant_docs

    if not return_all:
        sources = get_sources(result["output_text"], folder_index)

    answer = result["output_text"].split("SOURCES: ")[0]

    return AnswerWithSources(answer=answer, sources=sources)


def get_sources(answer: str, folder_index: FolderIndex) -> List[Document]:
    """Retrieves the docs that were used to answer the question the generated answer."""

    source_keys = [s for s in answer.split("SOURCES: ")[-1].split(", ")]

    source_docs = []
    for file in folder_index.files:
        for doc in file.docs:
            if doc.metadata["source"] in source_keys:
                source_docs.append(doc)

    return source_docs
