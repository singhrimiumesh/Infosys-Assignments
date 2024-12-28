API_KEY = "......your api key......"
url = "https://api.groq.com/openai/v1/chat/completions"

import requests
import json
import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

# Scraping website and returning the extracted data
def scrape_website(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    extracted_data = {}

    try:
        print(f"Opening website: {url}\n")
        driver.get(url)

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        title = driver.title
        extracted_data["title"] = title

        try:
            meta_description = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content")
        except Exception:
            meta_description = "No meta description found."
        extracted_data["meta_description"] = meta_description

        try:
            meta_keywords = driver.find_element(By.XPATH, "//meta[@name='keywords']").get_attribute("content")
        except Exception:
            meta_keywords = "No meta keywords found."
        extracted_data["meta_keywords"] = meta_keywords

        headings = {}
        for level in range(1, 7):
            heading_tag = f"h{level}"
            headings[heading_tag] = [h.text for h in driver.find_elements(By.TAG_NAME, heading_tag) if h.text]
        extracted_data["headings"] = headings
        
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            page_text = driver.find_element(By.TAG_NAME, "body").text
        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
            page_text = ""
        extracted_data["textual_data"] = page_text

        links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a") if a.get_attribute("href")]
        extracted_data["links_count"] = len(links)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return extracted_data

# Chatbot using Groq Cloud API
def get_response(prompt, scraped_data):
    system_prompt = (
    "You are an intelligent assistant bot designed to answer user questions based on the data scraped from a website. "
    "Your task is to provide helpful, informative, and accurate responses by analyzing and referencing the provided data. "
    "The data includes the website's title, meta description, keywords, headings, textual content, and the number of links. "
    "Here is the structured data from the website you should refer to while answering questions:\n\n"
    f"Title: {scraped_data.get('title', 'No title found')}\n\n"
    f"Meta Description: {scraped_data.get('meta_description', 'No meta description available')}\n\n"
    f"Meta Keywords: {scraped_data.get('meta_keywords', 'No meta keywords available')}\n\n"
    f"Headings: {scraped_data.get('headings', 'No headings found')}\n\n"
    f"Textual Content: {scraped_data.get('textual_data', 'No textual content available')}\n\n"
    f"Links Count: {scraped_data.get('links_count', 'No links found')}\n\n"
    "Please ensure your responses are based solely on this provided data, and avoid providing information that is not available in it."
    "If the data doesn't contain information related to the question, inform the user politely that the data does not contain such information."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    data = {
        "messages": messages,
        "model": "llama3-8b-8192",
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"An error occurred while making the API call: {e}"

# GUI
class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrape🔍 & Chat🤖")

        self.url_label = tk.Label(root, text="Enter Website URL to Scrape:")
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.scrape_button = tk.Button(root, text="Scrape Website", command=self.scrape_website)
        self.scrape_button.pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
        self.chat_area.pack(pady=10)

        self.user_input_label = tk.Label(root, text="Ask a Question:")
        self.user_input_label.pack(pady=5)

        self.user_input = tk.Entry(root, width=50)
        self.user_input.pack(pady=5)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.scraped_data = {}

        # User-Bot Text colors
        self.chat_area.tag_configure("user", foreground="blue", font=("Helvetica", 10, "bold"))
        self.chat_area.tag_configure("bot", foreground="green", font=("Helvetica", 10, "bold"))

    def scrape_website(self):
        url = self.url_entry.get().strip()
        if urlparse(url).scheme in ["http", "https"]:
            self.scraped_data = scrape_website(url)
            self.chat_area.insert(tk.END, "Website scraped successfully. You can now ask questions.\n\n")
            
        else:
            self.chat_area.insert(tk.END, "Invalid URL. Please enter a valid URL.\n")

    def send_message(self):
        user_input = self.user_input.get().strip()
        if user_input.lower() in ["exit", "quit"]:
            self.root.quit()
            return

        if not user_input:
            return

        self.chat_area.insert(tk.END, f"\n\nYou: {user_input}\n", "user")

        response = get_response(user_input, self.scraped_data) 

        self.chat_area.insert(tk.END, f"\nBot: {response}\n", "bot")
        
        self.user_input.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatBotGUI(root)
    root.mainloop()



