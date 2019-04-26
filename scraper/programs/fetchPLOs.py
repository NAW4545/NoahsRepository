from PLODB import PLODB
from PLOScraper import PLOScraper


def main():
    """ Scrape all program PLO data from the butte college website and insert
        it into the database.
    """
    scraper = PLOScraper()
    db = PLODB()
    all_programs = []
    # get the list of pids
    pids = scraper.getPrograms()
    print("PIDs:", pids)
    for pid in pids:
        # get the program and plo data from the program page
        plo_data = scraper.getPLOs(pid)
        all_programs += plo_data
        print("current programs scraped: ", len(all_programs))
        for plo in plo_data:
            # insert each plo into the database
            print("inserting:", plo)
            db.insert(plo)
    print("total programs scraped", len(all_programs))

if __name__ == '__main__':
    main()
