from unittest.mock import patch

from main import main


@patch("main.HH.search_vacancion")
@patch("main.input", side_effect=["v", "медпроф", "y", "q", "n", "q", "q", "q"])
def test_main_function(input, mock_search, examle_from_hh):
    """тестируем корректность работы  связанный"""
    mock_search.return_value = examle_from_hh
    main()
