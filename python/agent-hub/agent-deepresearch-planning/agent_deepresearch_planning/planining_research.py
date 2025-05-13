import json
from firecrawl import FirecrawlApp
from openai import OpenAI
from xml.etree import ElementTree as ET
import os
from dotenv import load_dotenv
from typing import List, Optional, Any
from pydantic import BaseModel



class SubPlan(BaseModel):
    core_objective: str
    hypothesis: str
    design_thinking: List[str]
    query_statement: List[str]
    data_sources: List[str]
    quantitative_analysis: str
    qualitative_analysis: str
    relationship_with_other_sub_plans: Optional[str] = None
    logical_connection_to_main_plan: str
    sub_id:str
    source_urls:Any = None
    source_data:Any = None
    summary:Any = None
    modification_reason: str = None  # 新增参数，表示修改原因


class MainPlan(BaseModel):
    core_goal: str
    core_research_direction: str
    sub_plans: List[SubPlan]

class ResearchPlanOutput(BaseModel):
    main_plan: MainPlan


class FireCrawl:
    def __init__(self, api_key: str=None,env_file:str='.env.secret',crawl_params:dict=None):
        if api_key is None:
            load_dotenv(env_file)
            api_key = os.getenv("FIRECRAWL_API_KEY")
        self.crawl = FirecrawlApp(api_key=api_key)
        if crawl_params is None:
            crawl_params =  {
    "maxDepth": 1,  # Number of research iterations
    "timeLimit": 180,  # Time limit in seconds
    "maxUrls": 3  # Maximum URLs to analyze
}
        self.crawl_params = crawl_params

    def on_activity(self,activity):
        print(f"[{activity['type']}] {activity['message']}")

    def deep_research(self, query: str,):
        results = self.crawl.deep_research(query=query,
        params=self.crawl_params,on_activity=self.on_activity)
        source_data = results['data']['sources']
        analysis_data = results['data']['finalAnalysis']
        return source_data,analysis_data

class MainPlanner:
    Main_Planner_PROMPT = """
Context: You are a senior research planning expert. Your task is to develop a detailed and logically structured research plan based on the user’s provided needs. The output must be directly in the JSON format that adheres to the following Pydantic class structure. Ensure that the JSON object you output is valid and does not contain any additional characters like \n, " or extra formatting.

Objective: To create a research plan where the main plan and its constituent sub-plans are logically interconnected and collectively aim to achieve the overall research goal. Ensure that each sub-plan builds upon previous ones (where applicable) and contributes a necessary component to the final research outcome. Output the result as clean, structured JSON directly without escape sequences or any other extra formatting.

Solution:

Understand the user's needs and core research goals.
Break down the main research plan into 3 to 5 logically connected sub-plans, ensuring each sub-plan's objective directly contributes to the overarching research goal.
For each sub-plan, provide the necessary details including the core objective (clearly stating its role in the overall research), hypothesis (relevant to the sub-plan's objective and the main research goal), design thinking (explaining how this sub-plan will contribute to the larger research narrative), and the various research elements (data sources, analysis methods, relationships with other sub-plans – explicitly detailing how this sub-plan builds upon or informs others).
Ensure that the output is in JSON format, strictly following the structure defined by the Pydantic classes.
Task:
The task involves creating a structured research plan that includes:

A main research plan with a core goal and research direction.
Sub-plans that focus on different aspects or phases of the research, with a clear and demonstrable connection to each other and the main plan.
Ensure each sub-plan includes:
core objective (clearly indicating its contribution to the main research goal and potentially its dependency on or influence over other sub-plans),
hypothesis (focused on the specific aspect addressed by the sub-plan and its relevance to the broader research question),
design thinking (outlining the rationale and methodology for this specific sub-plan in the context of the entire research project),
query statement,
data sources,
quantitative and qualitative analysis,
relationships with other sub-plans (explicitly describe how this sub-plan relates to and interacts with other sub-plans, e.g., "This sub-plan will provide foundational data for Sub-plan 3," or "The findings of Sub-plan 2 will be used to refine the hypothesis of this sub-plan."),
logical connection to the main plan (reiterate how this sub-plan directly contributes to achieving the core goal of the main research plan).
Action:
Follow these steps:
Understand the user’s specific research needs and goals.
Define a core goal and core research direction for the main plan.
Break down the research into 3-5 sub-plans, ensuring each sub-plan is logically connected to the main plan and, where applicable, to each other in a sequential or dependent manner.
For each sub-plan, fill out all required details (core objective, hypothesis, etc.) in accordance with the structure outlined, paying particular attention to explicitly defining the relationships between sub-plans and their individual contributions to the main research goal.
Provide the final research plan in the specified JSON format.

```python
class SubPlan(BaseModel):
    core_objective: str
    hypothesis: str
    design_thinking: List[str]
    query_statement: List[str]
    data_sources: List[str]
    quantitative_analysis: str
    qualitative_analysis: str
    relationship_with_other_sub_plans: Optional[str] = None
    logical_connection_to_main_plan: str
    sub_id:str

class MainPlan(BaseModel):
    core_goal: str
    core_research_direction: str
    sub_plans: List[SubPlan]

class ResearchPlanOutput(BaseModel):
    main_plan: MainPlan
```
"""
    Sub_Plan_Summary_PROMPT = """
    Context: You have been provided with the details of a specific sub-plan within a larger research project focused on [Placeholder: Main Plan's Core Goal]. This sub-plan aims to [Placeholder: Sub-plan's Core Objective] and seeks to answer the following question(s) or explore the following area(s): [Placeholder: Sub-plan's Specific Query Statement(s) or Focus Areas]. You have also been provided with the results of your research or data gathering efforts related to this sub-plan, which may include search results, extracted data, or preliminary analysis.
    
    Objective: Your goal is to generate a concise and insightful summary of the key findings and insights derived from the provided research results, directly addressing the objective and query/focus of this specific sub-plan.
    
    Task: Based on the provided information about the sub-plan and its corresponding research results, create a summary that includes the following elements:
    
    Sub-plan Objective Alignment: Clearly state how the findings from the research results directly relate to and contribute to the stated objective of this sub-plan: [Placeholder: Sub-plan's Core Objective].
    Answering the Query/Focus: Summarize the key answers, insights, or trends observed in the research results that address the sub-plan's specific question(s) or focus areas: [Placeholder: Sub-plan's Specific Query Statement(s) or Focus Areas].
    Key Supporting Evidence: Briefly mention the types of data or evidence from your research results that support your summary points. You don't need to provide exhaustive details, but indicate the nature of the supporting information.
    Contribution to Main Goal: Explain how the potential findings or insights from this sub-plan contribute to the overarching [Placeholder: Main Plan's Core Goal] of the main research project.
    Potential Next Steps or Implications: Briefly suggest any potential next steps in the research or the implications of these findings for the overall project.
    Action:
    
    Carefully review the provided details of the specific sub-plan, paying close attention to its [Placeholder: Sub-plan's Core Objective] and [Placeholder: Sub-plan's Specific Query Statement(s) or Focus Areas].
    Thoroughly analyze the provided research results (e.g., search results, data extracts, analysis summaries) to identify the most relevant findings and insights.
    Synthesize the information to address each of the points outlined in the Task section. Ensure that your summary directly links the research results back to the sub-plan's objectives and questions.
    Present your summary in a clear, concise, and well-organized manner.

    """
    Sub_Plan_Update = """
    Objective: Your sole objective is to evaluate the Next Sub-plan based on the details of the Current Sub-plan and determine if the Next Sub-plan requires modification to logically follow and contribute effectively to the overall research project. The final output MUST be a single JSON object representing the Next Sub-plan (modified or not), strictly adhering to the provided SubPlan Pydantic class structure. If modification is needed, the suggested changes should be reflected in the JSON output, along with a clear modification_reason for each change. If no modification is needed, the original Next Sub-plan should be outputted in JSON format with a modification_reason indicating why no changes were made.
Task: Based on the provided details of the Current Sub-plan and the Next Sub-plan, perform the following:
Analyze the Current Sub-plan: Understand the core_objective, hypothesis, design_thinking, and query_statement of the Current Sub-plan.
Evaluate the Next Sub-plan: Compare the core_objective, hypothesis, design_thinking, query_statement, data_sources, quantitative_analysis, qualitative_analysis, and relationship_with_other_sub_plans of the Next Sub-plan against the details of the Current Sub-plan to assess its logical flow, relevance, and potential impact on the main research goal.
Generate JSON Output for the Next Sub-plan:
If modifications are deemed necessary: Construct a JSON object representing the modified Next Sub-plan. This JSON object must include all fields of the SubPlan class, with the proposed new content for the modified fields and a clear and concise modification_reason explaining why each change was made. The sub_id must remain the same as the original Next Sub-plan.
If no modifications are deemed necessary: Construct a JSON object representing the original Next Sub-plan. This JSON object must include all fields of the SubPlan class, with the original content and a modification_reason field set to explain why no changes were needed (e.g., "No modification needed based on the logical flow from the Current Sub-plan").
Action:

Carefully review the provided JSON objects representing both the Current Sub-plan and the Next Sub-plan.
Analyze the logical progression from the Current Sub-plan to the Next Sub-plan, considering the research questions and overall goal: [Placeholder: Main Plan's Core Goal].
Determine if the Next Sub-plan, in its current form, is a logical and effective continuation of the research. Consider factors such as whether it builds upon the findings or objectives of the Current Sub-plan, addresses a relevant next step in the research, and utilizes appropriate methodologies and data sources.
Construct a single JSON object representing the evaluated (and potentially modified) Next Sub-plan, strictly adhering to the SubPlan Pydantic class structure. Ensure the modification_reason field accurately reflects the outcome of your evaluation.
```python
class SubPlan(BaseModel):
    core_objective: str
    hypothesis: str
    design_thinking: List[str]
    query_statement: List[str]
    data_sources: List[str]
    quantitative_analysis: str
    qualitative_analysis: str
    relationship_with_other_sub_plans: Optional[str] = None
    logical_connection_to_main_plan: str
    sub_id:str
    summary:Any = None
    modification_reason: str = None  # 新增参数，表示修改原因
```
    """
    Main_Plan_Summary_PROMPT = """
    Context: You have developed a comprehensive research plan (including a Main Plan and several Sub-plans) focused on [Placeholder: Main Plan's Core Goal]. Each Sub-plan has a defined objective, hypothesis, methodology, and has undergone a process of data gathering, analysis, and potential evaluation/modification. You now need to generate a high-level summary that provides an overview of the entire research endeavor.
Objective: Your objective is to create a concise yet comprehensive summary of the entire research plan. This summary should articulate the main research goal, the strategic breakdown into Sub-plans, the key objectives and anticipated outcomes of each Sub-plan, and the overall expected contribution or impact of the research project.
Solution: To achieve this objective, you will need to synthesize information from the Main Plan document and the summaries/evaluation results of each individual Sub-plan. You will identify the core elements of each component and articulate their relationship within the broader research framework.
Task: Your tasks are as follows:
Summarize the Main Plan: Briefly describe the core goal (core_goal) and the overarching research direction (core_research_direction) of the Main Plan.
Summarize Each Sub-plan: For each Sub-plan, provide a concise overview including its sub_id, core_objective, and the key findings or insights derived from its analysis and evaluation. If a Sub-plan was modified, briefly mention the reason for modification.
Highlight Interrelationships: Describe the key relationships between the different Sub-plans, as specified in the relationship_with_other_sub_plans field of each Sub-plan. Explain how the Sub-plans build upon each other or contribute to different aspects of the main research goal.
Articulate the Overall Contribution: Based on the individual Sub-plan summaries and their interrelationships, explain the anticipated overall contribution or impact of this research project to the field or the problem being addressed.
Identify Potential Limitations or Challenges: Briefly mention any potential limitations or challenges that might be encountered during the execution of this research plan, based on the design or the initial findings.
Action:
Review the detailed content of the Main Plan, paying close attention to the core_goal and core_research_direction.
For each Sub-plan in your research plan:
Identify its sub_id and core_objective.
Retrieve the summary information that was generated for that Sub-plan (including key findings and insights).
If the Sub-plan was modified, note the modification_reason.
Identify any specified relationships with other Sub-plans from the relationship_with_other_sub_plans field.
Synthesize the information gathered in the previous steps to create a coherent summary. Ensure that the summary flows logically from the Main Plan to the individual Sub-plans and their interconnections.
Clearly articulate the anticipated overall contribution or impact of the research based on the collective outcomes of the Sub-plans.
Reflect on the research design and the initial findings from the Sub-plans to identify any potential limitations or challenges that might affect the success of the project.
Present your summary in a well-structured format, using clear and concise language. You might consider using headings or bullet points to organize the information effectively.
    """
    def __init__(self):
        self.client = self.create_openai_client()
        self.main_plan = None
        self.fire_crawl = FireCrawl()
        self.old_main_plan = None
        self.retry_num = 2
    def create_sub_plan_summary(self, sub_plan:SubPlan, sub_plan_source_data:list, ):
        messages = [
            {"role": "system", "content": self.Sub_Plan_Summary_PROMPT},
            {"role": "user", "content": json.dumps(sub_plan_source_data)},
            {"role": "system", "content": json.dumps({'core_goal':self.main_plan.core_goal,'core_research_direction':self.main_plan.core_research_direction,'sub_plan':sub_plan.json()})},
        ]
        result = self._call_llm(messages=messages)
        return  result

    def create_openai_client(self):
        env_file = os.getenv('ENV_FILE', '.env.secret')
        if not os.path.exists(env_file):
            raise FileNotFoundError(f"未找到环境配置文件: {env_file}，请确保项目根目录存在该文件")

        load_dotenv(env_file)
        LLM_API_KEY = os.getenv("LLM_API_KEY")
        os.environ['OPENAI_API_KEY'] = LLM_API_KEY
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
        if not api_key:
            raise ValueError("""
            未找到有效的API密钥配置，请按以下步骤操作：
            1. 在项目根目录创建.env.secret文件
            2. 添加以下内容：
               OPENAI_API_KEY=您的实际API密钥
               # 或
               LLM_API_KEY=您的实际API密钥
            """)

        base_url = os.getenv("LLM_BASE_URL")
        return OpenAI(api_key=api_key, base_url=base_url)
    def remove_json_format(self, response: str) -> str:
        return response.replace("```json", "").replace("```", "")
    def generate_main_plan(self, user_query: str) :
        try:
            response = self._call_llm(user_query)
            response = json.loads(response.replace("```json", "").replace("```", ""))
            self.main_plan = MainPlan(**response['main_plan'])
            self.old_main_plan = response
            return self.main_plan
        except Exception as e:
            return self._fallback_plan(user_query)
    def main_plan_summary(self):
        main_plan_data = self.main_plan.model_dump_json(exclude={"source_urls", "source_data", "modification_reason"})
        messages = [
            {"role": "system", "content": self.Main_Plan_Summary_PROMPT},
            {"role": "user", "content": "This is the all plan  : " + json.dumps(main_plan_data)},
        ]
        result = self._call_llm(messages=messages)
        return result
    def update_sub_plan(self, sub_plan:SubPlan, next_sub_plan:SubPlan,):
        messages = [
            {"role": "system", "content": self.Sub_Plan_Update},
            {"role": "user", "content": "This is the next plan  : "+next_sub_plan.json()},
            {"role": "system", "content": "This is the current plan  : "+sub_plan.json()},
            {"role": "system", "content": "This is the overall plan  : "+ json.dumps(self.old_main_plan)},
        ]
        result = self._call_llm(messages=messages)
        return  self.remove_json_format(result)
    def _call_llm(self, query: str='', retries:int=3,temperature:float=0.75,messages:list[dict]=None) -> str:
        if messages is None:
            messages = [
                {"role": "system", "content": self.Main_Planner_PROMPT},
                {"role": "user", "content": query}
            ]
        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=os.getenv("LLM_MODEL_NAME",'gpt-4o'),
                    messages=messages,
                    temperature=temperature,
                )
                return response.choices[0].message.content
            except Exception:
                if attempt == retries - 1:
                    raise
    def _search_web(self):
        pass

    def run(self):
        plan_results = []
        for index_num,sub_plan in enumerate(self.main_plan.sub_plans):
            sub_queries = sub_plan.query_statement
            sub_plan_results = []
            for sub_query in sub_queries:
                source_data,analysis_data = self.fire_crawl.deep_research(query=sub_query)
                query_data = {'source_urls':source_data,'analysis_data':analysis_data}
                plan_results.append(query_data)
                sub_plan_results.append(query_data)
                sub_plan.source_urls = source_data
                sub_plan.source_data = analysis_data
            print(sub_plan_results)
            sub_plan.summary = self.create_sub_plan_summary(sub_plan=sub_plan, sub_plan_source_data=sub_plan_results)
            if index_num != len(self.main_plan.sub_plans) - 1:
                try:
                    new_sub_plan = self.update_sub_plan(sub_plan=sub_plan, next_sub_plan=self.main_plan.sub_plans[index_num + 1])
                    self.main_plan.sub_plans[index_num + 1] = SubPlan(**json.loads(new_sub_plan))
                except Exception as e :
                    for attempt in range(self.retry_num):
                        try:
                            new_sub_plan = self.update_sub_plan(sub_plan=sub_plan, next_sub_plan=self.main_plan.sub_plans[index_num + 1])
                            self.main_plan.sub_plans[index_num + 1] = SubPlan(**json.loads(new_sub_plan))
                            break
                        except Exception as e:
                            if attempt == self.retry_num - 1:
                                print(f"Error in updating sub plan: {e}")
        result = self.main_plan_summary()

        return result


if __name__ == "__main__":
    planner = MainPlanner()
    try:
        planner.generate_main_plan("如何评估AI对就业市场的影响？")
        result = planner.run()
        print(result)
    except Exception as e:
        print(f"研究计划生成失败: {str(e)}")
        print("请检查：1.环境变量配置 2.API服务可用性 3.网络连接")

