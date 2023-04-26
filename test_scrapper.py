import pytest

from scrapper_vacancies import getPage

def test_getPage():
   ds = getPage(1)
   assert ds is not None
