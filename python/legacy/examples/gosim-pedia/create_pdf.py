import json
import os

from fpdf import FPDF
from datetime import datetime

from mofa.utils.ai.conn import create_openai_client
from markdown_pdf import MarkdownPdf, Section

def load_speaker_data(speaker_id):
    with open('optimization_speakers.json', 'r') as f:
        for line in f:
            speaker = json.loads(line)
            if speaker['id'] == speaker_id:
                return speaker
    return None
def get_llm_response(client,messages:list, model_name:str='gpt-4o',stream:bool=False):
    response = client.chat.completions.create(
        model=os.environ['LLM_MODEL_NAME'] if os.getenv('LLM_MODEL_NAME') is not None else model_name,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content

def read_json_lines(file_path):
  """
  读取 JSON Lines 文件，每行作为一个独立的 JSON 对象。

  Args:
      file_path (str): JSON Lines 文件的路径。

  Returns:
      list: 包含所有 JSON 对象的列表。
  """

  data = []
  with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
      # 每行都是一个独立的 JSON 对象，使用 json.loads() 解析
      data.append(json.loads(line.strip()))  # strip() 去掉可能存在的换行符
  return data
def find_speaker_sessions(speaker_id):
    with open('Schedule.json', 'r') as f:
        schedule = json.load(f)
    
    sessions = []
    for track in schedule['sessions'].values():
        for session in track:
            for s in session['speakers']:
                if s.get('id') == speaker_id:
                    session_info = {
                        'date': session['date'],
                        'time': session['timeSlot'],
                        'title': session['title'],
                        'content': session['content']
                    }
                    sessions.append(session_info)
    return sessions

def create_host_content(llm_client,speaker_data:str,session_data:str):
    hosts_name = """You are an engaging event host with a professional and slightly humorous tone. Your task is to introduce the speaker and their session in a concise and engaging manner. The introduction should last around one minute and should include the following:

1.  **Greeting and Introduction to the Speaker**:
    * Begin with a polite greeting to the audience.
    * Introduce the speaker’s name and current role, mentioning a notable achievement or something unique about them in a light, engaging way. Keep it professional but with a subtle touch of humor where appropriate.

2.  **Speaker’s Background**:
    * Provide a brief and professional overview of the speaker’s background. Incorporate relatable elements where appropriate to make it interesting, while maintaining a professional demeanor and avoiding overly informal language.
    * Highlight a couple of key achievements or milestones that are impressive, keeping it concise.

3.  **Session Introduction**:
    * Introduce the session topic in an engaging way. Mention what attendees can expect from the session, with a touch of enthusiasm and potentially a very subtle hint of humor to build interest without making it too casual.
    * Use phrases like "we're in for an insightful session" or "you'll be learning from an expert in the field" to keep the audience intrigued.

4.  **Encourage Engagement**:
    * Encourage the audience to participate or ask questions during the session.
    * End with a polite and upbeat statement to smoothly transition into the session.

TONE
The output should be professional and concise, using a third-person perspective for descriptions of the task but adopting the host's voice for the introduction script. The host's introduction should be engaging, with a clear balance of professionalism and a subtle, light humor, ensuring the humor does not overshadow the professional nature of the introduction or the event.

"""
    result = get_llm_response(client=llm_client, messages=[
        {"role": "system", "content": hosts_name},
        {"role": "user", "content": speaker_data},
        {"role": "user", "content": session_data},
    ])
    return result
def write_pdf(file_path:str,data:str):
    pdf = MarkdownPdf()
    pdf.add_section(Section(data, toc=False))
    pdf.save(file_path)

def create_speaker_html(speaker_id, output_file):
    # Load data
    llm_client = create_openai_client()
    speaker = load_speaker_data(speaker_id)
    if not speaker:
        print(f"Speaker with ID {speaker_id} not found")
        return
    backstory= """GOSIM AI Paris 2025 is scheduled to take place in Paris, France, on May 6-7, 2025, at Station F. It is hosted by GOSIM (Global Open-Source Innovation Meetup) and co-organized by CSDN.
The conference will focus on the latest advancements across six tracks:

AI Model
AI Infra
AI Apps
Embodied AI
AI for Science
Global Open-Source AI Collaboration
The event aims to drive significant progress in global open-source AI collaboration.
"""
    sessions = find_speaker_sessions(speaker_id)
    for session_id,session in enumerate(sessions):
        host_content = create_host_content(llm_client, speaker['pedia'], json.dumps(session))
        html_prompt = """
SYSTEM INSTRUCTION
You are an advanced AI assistant tasked with generating a detailed markdown file for an event. The final output should be clear, concise, and well-structured, with multimedia content like images and videos included where applicable. The MOFA branding and related content should appear at the very bottom of the markdown file.
USER INSTRUCTION
Using the provided data, generate a final markdown file with the following sections, organizing the content as needed and allowing flexibility for the structure of pedia. Ensure all provided personal/biographical information for the speaker is included and clearly displayed, along with comprehensive event and session details. The markdown file should clearly and explicitly display the conference name, overall dates and location, the specific session date, time, title, and content, and the speaker's full name and position.

Here are the sections for the markdown file, in the requested order:

1.  Host Introduction
    Provide an engaging introduction of the host, including their role and style, but allow room for flexibility in how the host’s bio is presented. You may use humor or excitement in the tone.

    **Host:** *[With upbeat energy]* [Host's introduction content, including humor, speaker highlights, and relevant background details for engagement.]

2.  Track Information
    Add details about the track related to the speaker’s session. Include a track name and a brief description of what the session focuses on.

3.  Event and Session Details
    Combine the general conference information and specific session information into this section. Clearly include:
    * The general conference name, overall dates, location, theme, and key highlights.
    * The specific session title, the specific date, the specific time, and the session content.
    * Include any session photo (if applicable).
    Use the provided details to format this section in markdown, making the conference name, overall dates/location, and all specific session details (title, date, time, content) easily identifiable.

4.  Speaker Biography
    Include the speaker’s biography in markdown format. Freely organize all provided details from pedia, allowing flexibility in structure, but ensure all available information is included and clearly presented. Make sure to include the **Full Name** and **Current Position** explicitly labeled, along with any photos or multimedia links provided.
 
5.    At the very bottom of the markdown file, include the MOFA branding image and the content source.
    ![Mofa](mofa.png)
    *Content Source: [MOFA](https://github.com/moxin-org/mofa)*

TONE
The output should be professional and concise, using a third-person perspective. The host’s introduction should be engaging, with a balance of humor and professionalism. The event, session, track, and speaker sections should be structured clearly but allow flexibility for how the speaker's biography and achievements are presented, prioritizing the inclusion of all provided information.
The photos of the speaker and session should be retained as images within the markdown file, along with proper image credits.
Do not include other content such as Key Features review note.
"""
        title = session.get('title')

        html_file_name = f"./mds/{speaker_id}_{title}_en.md"

        result = get_llm_response(client=llm_client, messages=[
            {"role": "system", "content": html_prompt},
            {"role": "user", "content": 'personal information : ' +  json.dumps(str(speaker['pedia'])) + 'tag : '+ speaker.get('tag')},
            {"role": "user", "content": 'session: ' + json.dumps(session)},
            {"role": "user", "content": 'host_content : ' + json.dumps(host_content)},
            {"role": "user", "content": 'backstory : '+ json.dumps(backstory)},
            {"role": "user", "content": '5 Conference Tracks :'+ json.dumps({'ai model' :'Shaping the Future with Open-Source AI: Unleashing world-class performance in LLMs, multi-modal AI, cutting-edge image and video generation models, and pioneering on-device small LLMs pushing the boundaries of AI efficiency and accessibility.'
                                                                             ,'AI Infra':'Building Scalable AI with Open-Source Innovation: Advancing AI training, inference, fine-tuning, reinforcement learning frameworks, optimized on-device inference solutions, and seamless large-scale cloud deployment to enable next-generation AI capabilities',
                                                                             'AI Apps':'Transforming Industries with Open-Source AI: Leveraging community-driven AI models to revolutionize healthcare, finance, and creative tools, while integrating open-source AI app development frameworks, agentic tools, Retrieval-Augmented Generation (RAGs), front-end AI applications, personal AI assistants, future AI operating systems, and smart AI hardware.',
                                                                             'Embodied AI':'Propelling Open-Source Robotics Forward: Innovating community-driven robot design, expanding openly available datasets, developing advanced visual language models, and shaping policy frameworks that define the future of autonomous systems',
                                                                             'PyTorch Day France':"""A dedicated space for AI practitioners, researchers, and engineers to explore the latest advancements in deep learning with PyTorch.
From cutting-edge model development to scalable deployment, this track offers expert insights, hands-on sessions, and discussions shaping the future of AI with PyTorch""",})},
        ]).replace('```markdown','').replace('```','')
        with open(html_file_name, "w", encoding="utf-8") as file:
            file.write(result)
        write_pdf(file_path=f'./pdfs/{speaker_id}_{title}_en.pdf',data=result)
        fr_result = get_llm_response(client=llm_client, messages=[
            {"role": "system", "content": """
            SYSTEM INSTRUCTION
You are an advanced AI assistant tasked with converting the provided Markdown content into French while ensuring the structure and content remain the same. You should not output any extra messages, warnings, or change any file names.
USER INSTRUCTION
Please process the following Markdown content and translate it into French. Ensure the content structure remains intact, and no changes are made to the file name or additional outputs.
Key Instructions:
Only the content should be translated into French.
Maintain the original file name and file structure.
Do not output anything other than the translated content.
"""},
            {"role": "user", "content": json.dumps(result)},
        ]).replace('```markdown', '').replace('```', '')
        write_pdf(file_path=f'./pdfs/{speaker_id}_{title}_fr.pdf',data=fr_result)
        print('完成 ',speaker['id'],title)


# Example usage
if __name__ == "__main__":
    speaker_id = "huy-hoang-ha"  # Change this to any speaker ID
    all_speakers = read_json_lines('optimization_speakers_new.json')
    for speaker in all_speakers:
        output_file = './mds/' + speaker['id'] + '_en.md'
        create_speaker_html(speaker['id'], output_file)