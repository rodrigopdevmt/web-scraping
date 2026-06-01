from src.decipher import _extract_coordinates


def test_extract_coordinates_html_pattern() -> None:
    html = (
        '<table><tr>'
        '<td><p><span>0</span></p></td>'
        '<td><p><span>█</span></p></td>'
        '<td><p><span>2</span></p></td>'
        '</tr><tr>'
        '<td><p><span>1</span></p></td>'
        '<td><p><span>░</span></p></td>'
        '<td><p><span>1</span></p></td>'
        '</tr></table>'
    )
    result = _extract_coordinates(html)
    assert result is not None
    assert (0, "█", 2) in result
    assert (1, "░", 1) in result


def test_extract_coordinates_simple_pattern() -> None:
    html = "0█2 1░1"
    result = _extract_coordinates(html)
    assert result is not None
    assert (0, "█", 2) in result
    assert (1, "░", 1) in result


def test_extract_coordinates_invalid_char() -> None:
    result = _extract_coordinates("0X2")
    assert result is None or all(c not in ("░", "█") for _, c, _ in result)


def test_extract_coordinates_empty() -> None:
    result = _extract_coordinates("no coordinates here")
    assert result is None
