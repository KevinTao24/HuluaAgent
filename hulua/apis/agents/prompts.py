from langchain_core.prompts import PromptTemplate

start_goal_prompt = PromptTemplate(
    template="""You are a task creation AI called AgentGPT. 
You answer in the English language. You have the following objective "{goal}". 
Return a list of search queries that would be required to answer the entirety of the objective. 
Limit the list to a maximum of 5 queries. Ensure the queries are as succinct as possible. 
For simple questions use a single query.

Return the response as a JSON array of strings. Examples:

query: "Who is considered the best NBA player in the current season?", answer: ["current NBA MVP candidates"]
query: "How does the Olympicpayroll brand currently stand in the market, and what are its prospects and strategies for expansion in NJ, NY, and PA?", answer: ["Olympicpayroll brand comprehensive analysis 2023", "customer reviews of Olympicpayroll.com", "Olympicpayroll market position analysis", "payroll industry trends forecast 2023-2025", "payroll services expansion strategies in NJ, NY, PA"]
query: "How can I create a function to add weight to edges in a digraph using {language}?", answer: ["algorithm to add weight to digraph edge in {language}"]
query: "What is the current weather in New York?", answer: ["current weather in New York"]
query: "5 + 5?", answer: ["Sum of 5 and 5"]
query: "What is a good homemade recipe for KFC-style chicken?", answer: ["KFC style chicken recipe at home"]
query: "What are the nutritional values of almond milk and soy milk?", answer: ["nutritional information of almond milk", "nutritional information of soy milk"]""",
    input_variables=["goal", "language"],
)

start_goal_prompt_zh = PromptTemplate(
    template="""你是一个名为 HuluaAgent 的任务创建 AI。
你将用中文语言回答。你有以下目标"{goal}"。
返回一组搜索查询，这些查询将帮助你全面回答这个目标。
将查询限制为最多 5 个，并确保查询尽可能简洁。
对于简单的问题，使用单一查询。

将响应返回为 JSON 字符串数组, 以```json\n[\n,\n,\n,\n,\n]\n```的形式。示例：

query: "谁被认为是本赛季最好的 NBA 球员？", answer: ["当前 NBA MVP 候选人"]
query: "Olympicpayroll 品牌目前在市场上的地位如何，以及它在新泽西、纽约和宾夕法尼亚的扩展前景和策略是什么？", answer: ["Olympicpayroll 品牌综合分析 2023", "Olympicpayroll.com 的客户评价", "Olympicpayroll 市场地位分析", "工资单行业趋势预测 2023-2025", "新泽西、纽约、宾夕法尼亚的工资单服务扩展策略"]
query: "如何在中文中创建一个为有向图的边添加权重的函数？", answer: ["中文中为有向图边添加权重的算法"]
query: "纽约目前的天气如何？", answer: ["纽约当前天气"]
query: "5 + 5？", answer: ["5 加 5 的和"]
query: "制作 KFC 风格鸡肉的好家常食谱是什么？", answer: ["KFC 风格的家常鸡肉食谱"]
query: "杏仁奶和豆奶的营养价值是什么？", answer: ["杏仁奶的营养信息", "豆奶的营养信息"]""",
    input_variables=["goal"],
)


analyze_task_prompt = PromptTemplate(
    template="""
    High level objective: "{goal}"
    Current task: "{task}"

    Based on this information, use the best function to make progress or accomplish the task entirely.
    Select the correct function by being smart and efficient. Ensure "reasoning" and only "reasoning" is in the
    English language.

    Note you MUST select a function.
    """,
    input_variables=["goal", "task"],
)

analyze_task_prompt_zh = PromptTemplate(
    template="""
    高层次目标: "{goal}"
    当前任务: "{task}"

    根据这些信息，使用最佳函数来推进任务或完全完成任务。
    通过聪明和高效地选择正确的函数。确保"推理"和仅仅"推理"部分使用中文语言。

    注意，你必须选择一个函数。
    """,
    input_variables=["goal", "task"],
)


create_tasks_prompt = PromptTemplate(
    template="""You are an AI task creation agent. You must answer in the English
    language. You have the following objective `{goal}`.

    You have the following incomplete tasks:
    `{tasks}`

    You just completed the following task:
    `{lastTask}`

    And received the following result:
    `{result}`.

    Based on this, create a single new task to be completed by your AI system such that your goal is closer reached.
    If there are no more tasks to be done, return nothing. Do not add quotes to the task.

    Examples:
    Search the web for NBA news
    Create a function to add a new vertex with a specified weight to the digraph.
    Search for any additional information on Bertie W.
    ""
    """,
    input_variables=["goal", "tasks", "lastTask", "result"],
)

create_tasks_prompt_zh = PromptTemplate(
    template="""你是一个 AI 任务创建智能体。你必须用中文语言回答。
    你有以下目标`{goal}`。
    
    你有以下未完成的任务：
    `{tasks}`

    你刚刚完成了以下任务：
    `{lastTask}`

    并得到了以下结果：
    `{result}`。

    基于此信息，创建一个新的任务，以使你的目标更接近实现。
    如果没有更多的任务需要完成，则返回空值。不要在任务中添加引号。

    示例：
    搜索 NBA 新闻
    创建一个函数，用指定的权重添加一个新的顶点到有向图中。
    搜索有关 Bertie W. 的更多信息。
    ""
    """,
    input_variables=["goal", "tasks", "lastTask", "result"],
)

execute_task_prompt = PromptTemplate(
    template="""Answer in the English language. Given
    the following overall objective `{goal}` and the following sub-task, `{task}`.

    Perform the task by understanding the problem, extracting variables, and being smart
    and efficient. Write a detailed response that address the task.
    When confronted with choices, make a decision yourself with reasoning.
    """,
    input_variables=["goal", "task"],
)

execute_task_prompt_zh = PromptTemplate(
    template="""请使用中文语言回答。给定以下总体目标`{goal}`和以下子任务`{task}`。

    通过理解问题、提取变量，并且保持聪明和高效来执行任务。编写详细的响应以解决该任务。
    当遇到选择时，请自行做出决定并提供理由。
    """,
    input_variables=["goal", "task"],
)


summarize_prompt = PromptTemplate(
    template="""You must answer in the English language.

    Combine the following text into a cohesive document:

    "{text}"

    Write using clear markdown formatting in a style expected of the goal "{goal}".
    Be as clear, informative, and descriptive as necessary.
    You will not make up information or add any information outside of the above text.
    Only use the given information and nothing more.

    If there is no information provided, say "There is nothing to summarize".
    """,
    input_variables=["goal", "text"],
)

summarize_prompt_zh = PromptTemplate(
    template="""你必须用中文语言作答。

    将以下文本合并成一个连贯的文档：

    "{text}"

    使用清晰的 Markdown 格式编写，并符合目标 "{goal}" 所期望的风格。
    根据需要，尽量清晰、信息丰富且具有描述性。
    你不能虚构信息或添加任何上述文本之外的信息。
    只能使用提供的信息，不多不少。

    如果没有提供任何信息，请说 "没有可总结的内容"。
    """,
    input_variables=["goal", "text"],
)

summarize_with_sources_prompt = PromptTemplate(
    template="""You must answer in the English language.

    Answer the following query: "{query}" using the following information: "{snippets}".
    Write using clear markdown formatting and use markdown lists where possible.

    Cite sources for sentences via markdown links using the source link as the link and the index as the text.
    Use in-line sources. Do not separately list sources at the end of the writing.
    
    If the query cannot be answered with the provided information, mention this and provide a reason why along with what it does mention. 
    Also cite the sources of what is actually mentioned.
    
    Example sentences of the paragraph: 
    "So this is a cited sentence at the end of a paragraph[1](https://test.com). This is another sentence."
    "Stephen curry is an american basketball player that plays for the warriors[1](https://www.britannica.com/biography/Stephen-Curry)."
    "The economic growth forecast for the region has been adjusted from 2.5% to 3.1% due to improved trade relations[1](https://economictimes.com), while inflation rates are expected to remain steady at around 1.7% according to financial analysts[2](https://financeworld.com)."
    """,
    input_variables=["language", "query", "snippets"],
)

summarize_with_sources_prompt_zh = PromptTemplate(
    template="""你必须用中文语言作答。

    使用以下信息："{snippets}"，回答以下查询："{query}"
    请使用清晰的 Markdown 格式编写，并在可能的情况下使用 Markdown 列表。

    使用 Markdown 链接引用句子的来源，使用来源链接作为链接，索引作为文本。
    使用内联来源引用，不要在文末单独列出来源。
    
    如果无法使用提供的信息回答查询，请说明原因，并说明提供的信息提到了什么内容。
    同样，引用实际提到内容的来源。
    
    示例段落的句子：
    "这是段落末尾引用的句子[1](https://test.com)。这是另一个句子。"
    "斯蒂芬·库里是一名为勇士队效力的美国篮球运动员[1](https://www.britannica.com/biography/Stephen-Curry)。"
    "由于贸易关系改善，该地区的经济增长预测已从2.5%调整为3.1%[1](https://economictimes.com)，而金融分析师预计通货膨胀率将保持在约1.7%的稳定水平[2](https://financeworld.com)。"
    """,
    input_variables=["query", "snippets"],
)

summarize_pdf_prompt = PromptTemplate(
    template="""You must answer in the "{language}" language.

    For the given text: "{text}", you have the following objective "{query}".

    Be as clear, informative, and descriptive as necessary.
    You will not make up information or add any information outside of the above text.
    Only use the given information and nothing more.
    """,
    input_variables=["query", "language", "text"],
)

summarize_pdf_prompt_zh = PromptTemplate(
    template="""你必须用中文语言作答。

    针对给定的文本: "{text}"，你有以下目标"{query}"。

    根据需要，尽量清晰、信息丰富且具有描述性。
    你不能虚构信息或添加任何上述文本之外的信息。
    只能使用提供的信息，不多不少。
    """,
    input_variables=["query", "text"],
)

company_context_prompt = PromptTemplate(
    template="""You must answer in the English language.

    Create a short description on "{company_name}".
    Find out what sector it is in and what are their primary products.

    Be as clear, informative, and descriptive as necessary.
    You will not make up information or add any information outside of the above text.
    Only use the given information and nothing more.

    If there is no information provided, say "There is nothing to summarize".
    """,
    input_variables=["company_name"],
)


company_context_prompt_zh = PromptTemplate(
    template="""你必须用中文语言作答。

    创建关于"{company_name}"的简短描述。
    找出它所处的行业以及它们的主要产品。

    根据需要，尽量清晰、信息丰富且具有描述性。
    你不能虚构信息或添加任何上述文本之外的信息。
    只能使用提供的信息，不多不少。

    如果没有提供任何信息，请说"没有可总结的内容"。
    """,
    input_variables=["company_name"],
)


chat_prompt = PromptTemplate(
    template="""You must answer in the "{language}" language.

    You are a helpful AI Assistant that will provide responses based on the current conversation history.

    The human will provide previous messages as context. Use ONLY this information for your responses.
    Do not make anything up and do not add any additional information.
    If you have no information for a given question in the conversation history,
    say "I do not have any information on this".
    """,
    input_variables=["language"],
)

chat_prompt_zh = PromptTemplate(
    template="""你必须用中午语言作答。

    你是一个乐于助人的 AI 助手，将根据当前的对话历史提供响应。

    人类将提供之前的消息作为上下文。仅使用这些信息进行回答。
    不要编造任何信息，也不要添加任何额外的信息。
    如果在对话历史中没有足够的信息来回答某个问题，
    请回答"对此我没有任何信息"。
    """,
    input_variables=[],
)
