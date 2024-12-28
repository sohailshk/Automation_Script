import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import time


# Function to fetch a single page with retry logic
def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response  # Return response if successful
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    print(f"Failed to fetch {url} after {retries} retries.")
    return None


# Function to scrape data from one page
def scrape_books_page(url):
    response = fetch_page(url)
    if response is None:
        return []  # Return an empty list if the page couldn't be fetched

    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    for book in soup.select(".product_pod"):  # Select all books on the page
        try:
            title = book.select_one("h3 a")["title"]
        except AttributeError:
            title = "Title not available"

        try:
            price = book.select_one(".price_color").text.strip()
        except AttributeError:
            price = "Price not available"

        try:
            availability = book.select_one(".availability").text.strip()
        except AttributeError:
            availability = "Availability not available"

        try:
            rating = book.select_one(".star-rating")["class"][1]  # Get rating from class name
        except (AttributeError, IndexError):
            rating = "Rating not available"

        try:
            product_url = "http://books.toscrape.com/catalogue/" + book.select_one("h3 a")["href"]
        except AttributeError:
            product_url = "URL not available"

        books.append({
            "Title": title,
            "Price": price,
            "Availability": availability,
            "Rating": rating,
            "Product URL": product_url
        })
    return books


# Function to handle pagination and scrape all pages
def scrape_all_books(base_url):
    page = 1
    all_books = []

    while True:
        url = f"{base_url}page-{page}.html"
        print(f"Scraping page {page}...")

        try:
            books = scrape_books_page(url)
            if not books:  # Stop if no books are found
                print("No more data found.")
                break

            all_books.extend(books)
            page += 1
            time.sleep(1)  # Throttle requests to avoid overloading the server

        except Exception as e:
            print(f"Error occurred on page {page}: {e}")
            break  # Stop on critical errors

    return all_books


# Save scraped data to CSV
def save_data_to_csv(data, csv_file):
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")


# Visualize scraped data with bar graphs
def visualize_data(data):
    df = pd.DataFrame(data)

    # Clean and preprocess data for visualization
    df["Price"] = df["Price"].str.extract(r'(\d+\.\d+)').astype(float)  # Extract numeric values from price
    rating_order = ["One", "Two", "Three", "Four", "Five"]
    df["Rating"] = pd.Categorical(df["Rating"], categories=rating_order, ordered=True)
    
    # Bar chart: Number of books by rating
    rating_counts = df["Rating"].value_counts().sort_index()
    rating_counts.plot(kind="bar", title="Number of Books by Rating", xlabel="Rating", ylabel="Count", color="skyblue")
    plt.xticks(rotation=0)
    plt.show()

    # Bar chart: Average price by availability
    availability_price = df.groupby("Availability")["Price"].mean().dropna()
    availability_price.plot(kind="bar", title="Average Price by Availability", xlabel="Availability", ylabel="Average Price", color="orange")
    plt.xticks(rotation=0)
    plt.show()


# Main script
if __name__ == "__main__":
    base_url = "http://books.toscrape.com/catalogue/"
    print("Starting the scraping process...")
    
    # Scrape all book data
    books_data = scrape_all_books(base_url)

    if books_data:
        # Save data to a CSV file
        save_data_to_csv(books_data, "books_data.csv")

        # Visualize the data
        visualize_data(books_data)

    print("Scraping process completed!")
