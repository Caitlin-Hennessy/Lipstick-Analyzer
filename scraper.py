import requests
from bs4 import BeautifulSoup
'''
HTML structure:
<div class="search-results">
    <table class="table">
        <tbody>
            <tr>
                {
                td #2 contains name;
                td #4 contains avg rating;
                td # 5 contains num reviews;
                td # 6 contains % buy again}
            </tr>
        </tbody>
    </table>
</div>
'''
def main():
    data_file = open("data.csv", "w")

    for i in range(1, 68):
        page = requests.get("https://www.makeupalley.com/product/searching.asp/Brand=287/CategoryId=201/BrandName=MAC%20Cosmetics/page=" + str(i))
        soup = BeautifulSoup(page.content, "html.parser")

        name_anchors = soup.select("div.search-results tr > td:nth-of-type(2) > a")
        names = [anchor.get_text().encode("ascii", "ignore").replace(",", "") for anchor in name_anchors]

        avg_review_tds = soup.select("div.search-results tr > td:nth-of-type(4)")
        avg_reviews = [float(td.get_text()) for td in avg_review_tds]

        review_count_tds = soup.select("div.search-results tr > td:nth-of-type(5)")
        review_counts = [int(td.get_text()) for td in review_count_tds]

        percent_buy_again_tds = soup.select("div.search-results tr > td:nth-of-type(6)")
        percent_buy_agains = [int(td.get_text()[:-1]) for td in percent_buy_again_tds]

        try:
            assert len(names) == len(avg_reviews) == len(review_counts) == len(percent_buy_agains)
        except AssertionError:
            print "Something went wrong on page " + str(i)
            return

        data_rows = map(lambda x: ",".join(map(str, x)), zip(names, avg_reviews, review_counts, percent_buy_agains))

        for row in data_rows:
            data_file.write(row + "\n")

        print "Processed " + str(len(names)) + " results from page " + str(i)

main()