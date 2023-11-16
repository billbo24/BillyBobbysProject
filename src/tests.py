import unittest

from src.scrapeWikiBaseball import scrape_and_save

class ScrapeTest(unittest.TestCase):

    def test_scrape(self):

        page = 'List of Members Baseball Hall of Fame'
        bad_words = ["Chicago","AFL","AFC","National","American","Academy"]
        persons = set(scrape_and_save(page, bad_words))

        # for i, person in enumerate(persons):
        #     print(i, person)

        self.assertIn('Ty Cobb', persons)
        self.assertIn('Honus Wagner', persons)
        self.assertIn('Tris Speaker', persons)