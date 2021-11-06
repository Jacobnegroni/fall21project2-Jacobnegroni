# FALL 2021
# SI 206
# Name: Jacob Negroni
# Who did you work with: Umang Bhojani, Abby Williams
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results():
    """
    Write a function that creates a BeautifulSoup object on "search_results.html". Parse
    through the object and return a list of tuples containing book titles, authors, and rating
    (as printed on the Goodreads website) in the format given below. Make sure to strip()
    any newlines from the book titles and author names.

    [('Book title 1', 'Author 1','Rating 1'), ('Book title 2', 'Author 2', 'Rating 2')...]
    """
    html_file = open("search_results.html",'r')
    soup = BeautifulSoup(html_file,'html.parser')
    html_file.close()

    book_list = []
    tr_list = soup.find_all("tr")
    for tr in tr_list:
        td = tr.find("td",{"width":"100%"})
        title = td.a.text.strip()
        author = td.div.text.strip()
        rating = td.find("span",{"class":"minirating"}).text.strip()[:4]
        book_list += [(title,author,rating)]
    
    return(book_list)


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "/book/show/" to 
    your list, and be sure to append the full path (https://www.goodreads.com) to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

    urls = []

    page = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(page.content,'html.parser')

    books = soup.find_all('a',{"class":"bookTitle"})[:10]
    for book in books:
        url = book.get('href').strip()
        urls = urls + ["https://www.goodreads.com"+url]

    return(urls)


def get_book_summary(book_html):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the HTML file of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, number of pages, 
    and book rating. This function should return a tuple in the following format:
    
    ('Some book title', 'the book's author', number of pages, book rating)
    
    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title, number of pages, and rating.

    """

    # Assuming that the book_html is filepath
    file = open(book_html)
    soup = BeautifulSoup(file,'html.parser')
    file.close()

    title = soup.find("h1",{"id":"bookTitle"}).text.strip()
    author = soup.find("span",{"itemprop":"name"}).text.strip()
    pages = soup.find("span",{"itemprop":"numberOfPages"}).text.strip().split()[0]
    rating = soup.find("span",{"itemprop":"ratingValue"}).text.strip()

    return((title,author,int(pages),float(rating)))


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST 
    BOOKS OF 2020" page in "best_books_2020.html". This function should create a 
    BeautifulSoup object from a filepath and return a list of (category, book title, 
    URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The 
    Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should 
    append("Fiction", "The Testaments (The Handmaid's Tale, #2)", 
    "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
    to your list of tuples.

    """
    best = []

    file = open(filepath)
    soup = BeautifulSoup(file,'html.parser')
    file.close()

    divs = soup.find_all("div",{"class":"category clearFix"})
    for div in divs:
        category = div.h4.text.strip()
        book = div.img.get("alt").strip()
        url = div.a.get('href').strip()
        best = best + [(category,book,url)]

    return(best)


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
   one that is returned by get_titles_from_search_results()), sorts the tuples in 
   descending order by largest rating, writes the data to a csv file, and saves it to 
   the passed filename.
   The first row of the csv should contain "Book title", "Author Name", “Rating”, 
   respectively as column headers. For each tuple in data, write a new
   row to the csv, placing each element of the tuple in the correct column.
 
   When you are done your CSV file should look like this:
 
   Book title,Author Name,Rating
   Book1,Author1,Rating1
   Book2,Author2,Rating2
   Book3,Author3,Rating3
   
   In order of highest rating to lowest rating.
 
   This function should not return anything.

    """
    csvfile = open(filename,'w')
    csvfile.write("Book title,Author Name,Rating")
    new_data = []
    # Sort by rating - third element in tuple
    for tup in data:
        new_data = new_data + [(tup[0],tup[1],float(tup[2]))]
    new_data.sort(key=lambda tup: -tup[2]) 
    for d in new_data:
        csvfile.write("\n")
        csvfile.write('"'+d[0]+'","'+d[1]+'",'+str(d[2]))
    csvfile.close()



def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() and save to a local variable
        results = get_titles_from_search_results()
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(results),20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(results),list)
        # check that each item in the list is a tuple
        for result in results:
            self.assertEqual(type(result),tuple)
        # check that the first book and author tuple is correct (open search_results.html and find it)
        self.assertEqual(results[0],('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling', '4.62'))
        # check that the last title is correct (open search_results.html and find it)
        self.assertEqual(results[-1],('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling', '4.18'))

    def test_get_search_links(self):
        urls = get_search_links()
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls),list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls),10)

        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertEqual(type(url),str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for url in TestCases.search_urls:
            self.assertTrue(url.startswith("https://www.goodreads.com/book/show/"))

    def test_get_book_summary(self):
        # the list of webpages you want to pass in one by one into get_book_summary 
        html_list = ['book_summary_html_files/Fantasy Lover (Hunter Legends, #1) by Sherrilyn Kenyon.html',
                        'book_summary_html_files/Fantasy in Death (In Death, #30) by J.D. Robb.html',
                        'book_summary_html_files/Fantasy of Frost (The Tainted Accords, #1) by Kelly St. Clare.html',
                        'book_summary_html_files/The Mind’s I_ Fantasies and Reflections on Self and Soul by Douglas R. Hofstadter.html',
                        'book_summary_html_files/Gods and Mortals_ Fourteen Free Urban Fantasy & Paranormal Novels Featuring Thor, Loki, Greek Gods, Native American Spirits, Vampires, Werewolves, & More by C. Gockel.html',
                        'book_summary_html_files/Epic_ Legends of Fantasy by John Joseph Adams.html',
                        'book_summary_html_files/The Kingdom of Fantasy by Geronimo Stilton.html',
                        'book_summary_html_files/Kurintor Nyusi_ Diverse Epic Fantasy by Aaron-Michael Hall.html',
                        'book_summary_html_files/Kurintor Nyusi_ Diverse Epic Fantasy by Aaron-Michael Hall.html',
                        'book_summary_html_files/Die, Vol. 1_ Fantasy Heartbreaker by Kieron Gillen.html']
        # check that the number of book summaries is correct (10)
        summaries = []
        for html in html_list:
            summaries += [get_book_summary(html)]
        self.assertEqual(len(summaries),10)
        for summary in summaries:
            # check that each item in the list is a tuple
            self.assertEqual(type(summary),tuple)
            # check that each tuple has 4 elements
            self.assertEqual(len(summary),4)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(summary[0]),str)
            self.assertEqual(type(summary[1]),str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(summary[2]),int)
            # check that the fourth element in the tuple, i.e. rating is a float
            self.assertEqual(type(summary[3]),float)
        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2],337)
        # check the last book has 4.02 rating
        self.assertEqual(summaries[-1][3],4.02)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best = summarize_best_books("best_books_2020.html")
        # check that we have the right number of best books (20)
        self.assertEqual(len(best),20)

        for each_summary in best:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(each_summary),tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(each_summary),3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best[0],('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best[-1],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.html and save the result to a variable
        titles = get_titles_from_search_results()
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles,"test.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        file = open("test.csv")
        csv_lines = []
        for line in file.readlines():
            csv_lines += [line.strip()]
        file.close()
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines),21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0],'Book title,Author Name,Rating')
        # check that the next row is 'Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)', 'J.K. Rowling,', '4.78'
        # ^^this version has a comma after J.K Rowling, however other versions of the answer might not have a comma. We accept both
        self.assertEqual(csv_lines[1],'"Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)","J.K. Rowling,",4.78')
        # check that the last row is 'Harry Potter and the Cursed Child: Parts One and Two (Harry Potter, #8)', 'John Tiffany (Adaptation),', '3.62'
        # ^^^again in a different answer the result for authoer is J.K Rowling. We should accept both
        self.assertEqual(csv_lines[-1],'"Harry Potter and the Cursed Child: Parts One and Two (Harry Potter, #8)","John Tiffany (Adaptation),",3.62')
        


if __name__ == '__main__':
    print(extra_credit("extra_credit.html"))
    unittest.main(verbosity=2)



