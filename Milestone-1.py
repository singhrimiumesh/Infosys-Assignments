from groq import Groq
import gradio as gr
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

def job_search_interface(query):
    bot = JobSearchBot()
    results = bot.search_jobs(query)
    return results

# Gradio Interface
def main():
    interface = gr.Interface(
        fn=job_search_interface,
        inputs=gr.Textbox(placeholder="Enter job search query (e.g., 'Frontend developer in New York')", label="Job Search Query"),
        outputs=gr.Markdown(label="Job Results"),
        title="Job Search Bot",
        description="Enter your desired job role, skills, and location to find the top 5 matches in markdown format.",
        allow_flagging="never" 
    )
    interface.launch()

if __name__ == "__main__":
    main()
