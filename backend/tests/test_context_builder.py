from core.schema import RetrievedDocument
from retrieval.context_builder import ContextBuilder


def _doc(text: str) -> RetrievedDocument:
    return RetrievedDocument(id="1", score=0.5, text=text, metadata={})


def test_build_joins_documents_with_separator():
    context = ContextBuilder().build([_doc("Nội dung A"), _doc("Nội dung B")])
    assert context == "Nội dung A\n\n---\n\nNội dung B"


def test_build_caps_document_count():
    docs = [_doc(f"Doc {i}") for i in range(10)]
    context = ContextBuilder(max_documents=5, max_context_length=3000).build(docs)
    assert context.count("---") == 4


def test_build_truncates_when_exceeding_max_length():
    builder = ContextBuilder(max_documents=5, max_context_length=20)
    context = builder.build([_doc("x" * 100)])
    assert len(context) == 20


def test_build_skips_empty_text():
    docs = [_doc("   "), _doc("Nội dung thật")]
    context = ContextBuilder().build(docs)
    assert context == "Nội dung thật"


def test_build_returns_empty_for_no_documents():
    assert ContextBuilder().build([]) == ""
