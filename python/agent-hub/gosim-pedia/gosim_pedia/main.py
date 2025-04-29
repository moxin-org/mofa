import json
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.kernel.rag.embedding.huggingface import load_embedding_model
def get_llm_response(client,messages:list, model_name:str='gpt-4o',stream:bool=False):
    response = client.chat.completions.create(
        model=os.environ['LLM_MODEL_NAME'] if os.getenv('LLM_MODEL_NAME') is not None else model_name,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content
def create_openai_client(api_key: str=os.getenv("OPENAI_API_KEY",None),env_file:str=os.getenv('ENV_FILE','.env.secret'),*args,**kwargs) -> OpenAI:
    load_dotenv(env_file)
    if api_key is not None:
        client = OpenAI(api_key=api_key,**kwargs)
    else:
        if os.getenv('LLM_API_KEY') is not None:
            os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
        if os.getenv('LLM_BASE_URL', None) is None:
            client =OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        else:
            client =OpenAI(api_key=os.environ['OPENAI_API_KEY'], base_url=os.getenv('LLM_BASE_URL'), )
    return client
extract_speaker_prompt = """
# CONTEXT #
You are an advanced AI assistant trained to extract and organize detailed information from speaker biographies. The provided text contains a speaker's professional background, achievements, and areas of expertise.

# OBJECTIVE #
Extract the following information from the provided biography:
1. **Name**: The full name of the speaker.
2. **Organization**: The current organization or company the speaker is affiliated with.
3. **Keywords**: A list of at least five keywords or phrases that encapsulate the speaker's areas of expertise or focus.
4. **Personal Journey**: A brief narrative highlighting the speaker's career path, significant achievements, and contributions to their field.

# STYLE #
Present the information in a structured and clear format, using bullet points or numbered lists where appropriate. Ensure that the response is easy to read and understand.

# TONE #
Maintain a professional and neutral tone throughout the response.

# AUDIENCE #
This information is intended for event organizers, researchers, and professionals seeking to understand the speaker's background and expertise.

# RESPONSE FORMAT #
Provide the extracted information in the following JSON format:
{
  "name": "Speaker's Full Name",
  "organization": "Current Organization or Company",
  "keywords": ["Keyword1", "Keyword2", "Keyword3", "Keyword4", "Keyword5"],
  "personal_journey": "A brief narrative of the speaker's career path and achievements."
}

Input Biography:
{Insert the speaker's biography text here}

"""
summary_prompt = """
# SYSTEM INSTRUCTION #
You are an advanced AI assistant tasked with compiling a detailed biography of the speaker, organized chronologically. The biography should include multimedia content, such as images, videos, blogs, and proper citations for all the provided information. If any multimedia links (e.g., video URLs, blog URLs, publication URLs) are available, include them with clear descriptions and source citations.

# USER INSTRUCTION #
Please process the following data to create a detailed and structured speaker biography in markdown format:

<<Insert Data Here>>

# TASK 1: Biography Compilation #
Using the provided data, compile a **chronological** speaker biography. The biography should include the following sections:

### 1. **Full Name**:
- The speaker’s complete name.

### 2. **Current Position**:
- The speaker’s current job title and the organization they are affiliated with.

### 3. **Education**:
- Academic qualifications, including institutions attended, degrees earned, and relevant coursework or honors.

### 4. **Career Path**:
- Provide a **chronological** overview of the speaker’s career, including:
  - **Year(s)**: The year(s) the speaker held each position.
  - **Position**: Job title and the organization or institution.
  - **Responsibilities**: A brief description of their role and contributions.

### 5. **Major Contributions**:
- Significant achievements and contributions in their field, including innovative projects, research, or initiatives.

### 6. **Publications**:
- A list of notable publications authored by the speaker:
  - **Year**: The year of publication.
  - **Title**: The title of the publication.
  - **Brief Description**: A short description of the publication and its impact.
  - **Publication URL**: The link to the full paper or article.

### 7. **Media Appearances**:
- List any media appearances, interviews, or podcasts:
  - **Year**: The year of the appearance.
  - **Title**: The title of the media appearance or podcast.
  - **Brief Description**: A short description of the topic or discussion.

### 8. **Awards and Recognitions**:
- Any awards or honors the speaker has received:
  - **Year**: The year the award was received.
  - **Award Name**: The name of the award.
  - **Brief Description**: A brief description of the award and its significance.

### 9. **Personal Insights**:
- Any personal anecdotes, insights, or reflections that provide a deeper understanding of the speaker’s journey and motivations.

### 10. **Social Media Presence**:
- Links to the speaker’s social media profiles, such as LinkedIn, Twitter, etc., allowing readers to connect with the speaker professionally and personally.

### 11. **Influence and Impact**:
- A description of the speaker's influence in their field, industry, or community, showcasing how they have contributed to shaping trends, practices, or philosophies.

### 12. **Key Projects and Collaborations**:
- A section dedicated to major projects or collaborations the speaker has been a part of, demonstrating their hands-on contributions in the field.

### 13. **Future Goals and Plans**:
- Any known upcoming projects, goals, or endeavors the speaker is working on, showing the forward-looking aspect of their career.

### 14. **Quotes or Testimonials**:
- Notable quotes from the speaker or testimonials from colleagues or collaborators, offering personal insights into the speaker's character and contributions.

### 15. **Public Engagements (Conferences, Talks, Webinars)**:
- A specific section on public speaking engagements, such as keynote addresses, webinars, or appearances at major conferences, which demonstrate the speaker’s influence and thought leadership.

### 16. **Skills and Expertise**:
- A list of the speaker's key skills and expertise, highlighting any certifications or training relevant to their field of work.

### 17. **References**:
- A section acknowledging individuals who have influenced the speaker's journey or have been key collaborators (with permission).

### 18. **Images**:
- If the data contains images, include them with descriptions, URLs, and corresponding data sources:
  - **Image Description**: A brief caption or description of the image.
  - **Image URL**: A link to the image.
  - **Source**: The URL or name of the source where the image was found.

### 19. **Videos**:
- If video URLs are available, provide them with brief descriptions of the content:
  - **Video Title**: The title of the video or lecture.
  - **Video URL**: The link to the video.
  - **Description**: A short description of the video content.

### 20. **Blogs**:
- If blog URLs are provided, include them with a brief description of the blog post:
  - **Blog Title**: The title of the blog.
  - **Blog URL**: The link to the blog post.
  - **Description**: A short summary of the blog post content.

# TASK 2: Markdown Formatting #
Format the biography in markdown using the following structure. Ensure each section is clearly organized and adheres to the timeline:

## Speaker Biography: [Speaker's Full Name]

### 🧾 Personal Information
- **Full Name**: [Full Name]
- **Current Position**: [Position]
- **Education**: [Education Details]
- **Location**: [Location]

### 🧭 Career Path (Timeline)
- **[Year]**: [Position at Organization] – [Brief Description]
- **[Year]**: [Position at Organization] – [Brief Description]
- ...

### 📚 Publications
- **[Year]**: [Title of Publication] – [Brief Description]  
  [Read the full paper here](Publication URL)
- **[Year]**: [Title of Publication] – [Brief Description]  
  [Read the full paper here](Publication URL)
- ...

### 🏆 Awards and Recognitions
- **[Year]**: [Award Name] – [Brief Description]
- **[Year]**: [Award Name] – [Brief Description]
- ...

### 🎤 Media Appearances
- **[Year]**: [Title of Appearance] – [Brief Description]
- **[Year]**: [Title of Appearance] – [Brief Description]
- ...

### 🧠 Personal Insights
- [Insight or Anecdote]

### 📸 Images
![Image Description](Image URL)  
*Image Source: [Source URL]*

### 🎬 Videos
- **[Year]**: [Video Title] – [Brief Description]  
  [Watch the Video Here](Video URL)

### 📖 Blogs
- **[Blog Title]** – [Brief Description]  
  [Read the Blog Here](Blog URL)

### 🔗 Source Citations
- [Source 1](Source URL)
- [Source 2](Source URL)
- ...

# OUTPUT FORMAT #
Provide the biography in markdown format, with sections organized chronologically. Include videos, blogs, publications (with URLs), images, their descriptions, URLs, and source citations. Ensure all information is accurate, well-organized, and properly cited.

# TONE #
Use third-person consistently for professional bio tone.
"""

@run_agent
def run(agent:MofaAgent):
    env_file = '.env.secret'
    load_dotenv(env_file)
    query = agent.receive_parameter('query')
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(formatted_time, '      received data:', query, )
    llm_client = create_openai_client()
    speaker_info = get_llm_response(client=llm_client, messages=[
        {"role": "system", "content": extract_speaker_prompt},
        {"role": "user", "content": query},
    ])
    speaker_info_data = speaker_info.replace('\n', '').replace('```json', '').replace('\n```', '').replace('```', '')
    speaker_info_data = json.loads(speaker_info_data)
    speaker_name_and_organization = speaker_info_data.get('name') + ' - ' + speaker_info_data.get('organization')
    agent.send_output(agent_output_name='speaker_query', agent_result=speaker_name_and_organization)
    speaker_link_search = f""""{speaker_info_data.get('name')}" ({speaker_info_data.get('organization')}) (site:github.com OR site:linkedin.com OR site:twitter.com OR site:x.com OR site:youtube.com OR site:medium.com OR site:dev.to OR site:substack.com OR site:gitlab.com OR site:bitbucket.org OR site:facebook.com OR site:instagram.com OR blog OR website OR "about.me" OR "speakerdeck.com" OR "personal website" OR "site:discord.com" OR "site:reddit.com")"""

    agent.send_output(agent_output_name='speaker_link_query', agent_result=speaker_link_search)
    tool_results = agent.receive_parameters(['firecrawl_result','serper_result','rag_result','firecrawl_link_result'])

    summary_messages = [
                {"role": "system", "content": summary_prompt},
                {"role": "user", "content": 'firecrawl_result: ' + json.dumps(tool_results.get('firecrawl_result'))},
                {"role": "user", "content": 'serper_result: ' +json.dumps(tool_results.get('serper_result'))},
                {"role": "user", "content": 'rag_result : '+json.dumps(tool_results.get('rag_result'))},
                {"role": "user", "content": 'firecrawl_link_result : '+json.dumps(tool_results.get('firecrawl_link_result'))},
        ]
    summary_speaker_info = get_llm_response(client=llm_client,messages=summary_messages)
    agent.send_output('speaker_summary', summary_speaker_info)
def main():
    agent = MofaAgent(agent_name='gosim-pedia-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()