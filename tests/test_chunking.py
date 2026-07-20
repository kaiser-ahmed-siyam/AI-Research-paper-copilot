from research_copilot.chunking import chunk_text


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_chunk_text_shorter_than_chunk_size():
    text = "one two three four five"
    assert chunk_text(text, chunk_size=10, overlap=2) == [text]


def test_chunk_text_overlaps_and_covers_all_words():
    words = [f"w{i}" for i in range(25)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=10, overlap=3)

    # Every word should appear in at least one chunk.
    covered = set(" ".join(chunks).split())
    assert covered == set(words)

    # Consecutive chunks should overlap by the requested word count.
    first_tail = chunks[0].split()[-3:]
    second_head = chunks[1].split()[:3]
    assert first_tail == second_head


def test_chunk_text_rejects_non_positive_size():
    try:
        chunk_text("a b c", chunk_size=0)
    except ValueError:
        return
    raise AssertionError("expected ValueError for non-positive chunk_size")
