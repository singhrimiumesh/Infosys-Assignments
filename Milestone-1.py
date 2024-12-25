from groq import Groq
import os

class JobSearchBot:
    def __init__(self):
        self.groq_client = Groq(api_key='gsk_moTKAED8kmrCFtrIUCmEWGdyb3FYNAFaTeLXkH1wTVlO6Mo0rIiXmUim')  

    def search_jobs(self, query):
        prompt = f"""Find 5 relevant jobs based on this search: {query}
        Format each job as a clickable link with role, location, and salary like this:
        [Role - Location - $Salary Range](job_url)
        
        Include only current market-relevant roles with realistic salaries."""

        response = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a job search assistant that provides results in markdown link format."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content

    def chat_loop(self):
        print("Job Search Bot (type 'exit' to quit)")
        while True:
            query = input("\nWhat jobs are you looking for? (Include skills/location): ")
            
            if query.lower() == 'exit':
                print("\nGoodbye!")
                break
                
            results = self.search_jobs(query)
            print("\nTop 5 Matches:\n" + results)

bot = JobSearchBot()
bot.chat_loop()
