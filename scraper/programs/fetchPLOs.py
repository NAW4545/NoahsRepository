from PLODB import PLODB
from PLOScraper import PLOScraper


def main():
    """ Scrape all program PLO data from the butte college website and insert
        it into the database.
    """
    scraper = PLOScraper()
    db = PLODB()
    plo_data = scraper.getAllPLOs()
    for plo in plo_data:
        # insert each plo into the database
        print("inserting:\n", plo)
        db.insert(plo)


    # # get the list of pids
    # pids = scraper.getPrograms()
    # # get the program and plo data from the program page
    # for pid in pids:
    #     plo_data = scraper.getPLOs(pid)
    #     for plo in plo_data:
    #         # insert each plo into the database
    #         print("inserting:\n", plo)
    #         db.insert(plo)

if __name__ == '__main__':
    main()
