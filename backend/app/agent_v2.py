import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

from app.tools.order_tools import track_order
from app.tools.product_tools import check_product_availability
from app.tools.rag_tools import lookup_policy
from app.config import GROQ_API_KEY

# Register available tools
tools = [track_order, check_product_availability, lookup_policy]
tools_by_name = {tool.name: tool for tool in tools}

# Initialize LLM with tool calling enabled
llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-120b",
    groq_api_key=GROQ_API_KEY
)
llm_with_tools = llm.bind_tools(tools)

system_prompt = (
    "You are the official AI Customer Support Assistant for ShopEase. "
    "Answer concisely, politely, and directly in plain text without raw markdown bolding (**). "
    "Structure responses with short paragraphs and clean bullet points using '-' so they are easy to scan in a chat window. "
    "Highlight key numbers (like 7 days, 48 hours, or 5-7 business days) clearly in the sentence. "
    "Always use `lookup_policy` for shipping, returns, refunds, cancellations, warranties, and payments. "
    "Use `track_order` and `check_product_availability` for order status and stock checks. "
    "Never invent order details or promise a refund before system confirmation. "
    "Never ask customers for passwords, OTPs, CVVs, UPI PINs, or full card numbers. "
    "End with a brief, helpful next step (such as asking for their Order ID if they want to check a specific order). "
    "If a policy is unclear or disputed, refer them to human support at support@shopease.example (Mon-Sat, 9 AM-6 PM IST)."
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
])

def process_query(user_message: str, chat_history: list = None) -> str:
    """Agent execution loop with tool invocation."""
    if chat_history is None:
        chat_history = []
    
    messages = list(chat_history) + [HumanMessage(content=user_message)]
    
    # Format messages through the prompt template
    formatted_prompt = prompt_template.invoke({"messages": messages})
    ai_msg = llm_with_tools.invoke(formatted_prompt)
    messages.append(ai_msg)
    
    # Execute tools if requested by the LLM
    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            selected_tool = tools_by_name.get(tool_call["name"])
            if selected_tool:
                tool_output = selected_tool.invoke(tool_call["args"])
            else:
                tool_output = f"Error: Tool {tool_call['name']} not found."
            
            messages.append(
                ToolMessage(
                    content=str(tool_output),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"]
                )
            )
        
        # Call the model again with tool outputs to get the final answer
        formatted_prompt = prompt_template.invoke({"messages": messages})
        final_response = llm_with_tools.invoke(formatted_prompt)
        return final_response.content
    
    return ai_msg.content