"""对话Agent系统 - 意图识别和路由"""

import json
from typing import List, Dict, Any, Tuple
from hello_agents import SimpleAgent
from ..services.llm_service import get_llm
from ..models.schemas import (
    DialogueRequest,
    DialogueResponse,
    AgentResponse,
    TripPlan,
    Message
)
from ..config import get_settings
from .trip_planner_agent import get_trip_planner_agent

# ============ 提示词 ============

INTENT_RECOGNITION_PROMPT = """你是一个专业的意图识别专家。你的任务是分析用户输入，识别用户的意图。

**可识别的意图类型：**
1. search_attraction - 搜索景点（用户想要查找、搜索、了解某个或某些景点）
2. weather_query - 天气查询（用户询问天气情况）
3. hotel_recommend - 酒店推荐（用户想要推荐、查找酒店，包括入住特定类型酒店如豪华型、经济型等）
4. modify_trip - 更改行程（用户想要修改、调整当前的旅行计划）
5. general_chat - 普通对话（不属于以上任何一种的对话）

**输出格式要求：**
请严格按照以下JSON格式返回结果：
```json
{
  "intents": ["intent1", "intent2"],
  "extracted_info": {
    "search_attraction": {
      "keywords": "景点关键词",
      "city": "城市名"
    },
    "weather_query": {
      "city": "城市名",
      "date": "日期（如：明天、后天、2025-06-01）"
    },
    "hotel_recommend": {
      "city": "城市名",
      "preferences": "偏好描述，如：豪华型、经济型、靠近景点等"
    },
    "modify_trip": {
      "requirements": "用户的具体需求描述"
    }
  }
}
```

**重要提示：**
1. 一个用户输入可能包含多个意图，请全部识别出来！！！
   - 例如："我想改成入住豪华型酒店"，既包含hotel_recommend（需要先推荐豪华型酒店），也包含modify_trip（要修改行程中的酒店）
   - 例如："帮我查一下明天的天气，再推荐几个景点"，包含weather_query和search_attraction
   - 例如："推荐几家酒店，然后把它们加入行程"，包含hotel_recommend和modify_trip
2. 如果意图不明确，默认归类为general_chat
3. 尽可能提取出相关的参数信息
4. 如果某个意图没有相关信息，该字段可以为空对象或省略

**示例1：**
用户输入："我想看看上海的天气，再推荐几个酒店"
输出：
```json
{
  "intents": ["weather_query", "hotel_recommend"],
  "extracted_info": {
    "weather_query": {
      "city": "上海"
    },
    "hotel_recommend": {
      "city": "上海"
    }
  }
}
```

**示例2：**
用户输入："我早上想晚点起来"
输出：
```json
{
  "intents": ["modify_trip"],
  "extracted_info": {
    "modify_trip": {
      "requirements": "早上想晚点起来"
    }
  }
}
```

**示例3：**
用户输入："我想改成入住豪华型酒店"
输出：
```json
{
  "intents": ["hotel_recommend", "modify_trip"],
  "extracted_info": {
    "hotel_recommend": {
      "preferences": "豪华型酒店"
    },
    "modify_trip": {
      "requirements": "改成入住豪华型酒店"
    }
  }
}
```

**示例4：**
用户输入："帮我查一下明天北京的天气，再推荐几个文化景点"
输出：
```json
{
  "intents": ["weather_query", "search_attraction"],
  "extracted_info": {
    "weather_query": {
      "city": "北京",
      "date": "明天"
    },
    "search_attraction": {
      "city": "北京",
      "keywords": "文化景点"
    }
  }
}
```
"""

GENERAL_CHAT_PROMPT = """你是一个友好的旅行助手。请根据当前的行程信息，用中文友好地回应用户。

当前行程信息：
{trip_info}

请确保你的回答：
1. 友好、专业、有帮助
2. 结合当前行程信息进行回应
3. 如果用户询问行程相关问题，基于当前行程信息回答
4. 保持回答简洁明了
"""

MODIFY_TRIP_PROMPT = """你是行程修改专家。请根据用户的需求修改当前的旅行计划。

**当前行程信息：**
{current_trip}

**用户的修改需求：**
{user_requirements}

**其他相关信息（如果有）：**
{additional_info}

请严格按照以下JSON格式返回修改后的行程：
{json_schema}

**重要提示：**
1. 保持原行程的基本结构不变
2. 只修改与用户需求相关的部分
3. 确保所有日期、经纬度等信息合理
4. 保持预算信息的一致性
5. 如果用户没有明确指定某些细节，保持原行程的设置
"""


class DialogueAgentSystem:
    """对话Agent系统"""

    def __init__(self):
        """初始化对话Agent系统"""
        print("🔄 初始化对话Agent系统...")
        
        try:
            self.llm = get_llm()
            self.settings = get_settings()
            
            # 创建意图识别Agent
            self.intent_agent = SimpleAgent(
                name="意图识别专家",
                llm=self.llm,
                system_prompt=INTENT_RECOGNITION_PROMPT
            )
            
            # 创建普通对话Agent
            self.general_chat_agent = SimpleAgent(
                name="旅行助手",
                llm=self.llm,
                system_prompt=""  # 动态设置
            )
            
            # 获取行程规划Agent
            self.trip_planner = get_trip_planner_agent()
            
            print("✅ 对话Agent系统初始化成功")
            
        except Exception as e:
            print(f"❌ 对话Agent系统初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def process_dialogue(self, request: DialogueRequest) -> DialogueResponse:
        """
        处理对话请求
        
        Args:
            request: 对话请求
            
        Returns:
            对话响应
        """
        try:
            print(f"\n{'='*60}")
            print(f"💬 处理对话请求")
            print(f"用户输入: {request.user_input}")
            print(f"{'='*60}\n")
            
            # 步骤1: 意图识别
            print("🔍 步骤1: 识别用户意图...")
            intents, extracted_info = self._recognize_intent(request.user_input)
            print(f"识别到的意图: {intents}")
            print(f"提取的信息: {extracted_info}\n")
            
            # 初始化响应
            response = DialogueResponse(
                success=True,
                recognized_intents=intents,
                agent_responses=[],
                general_response=None,
                modified_trip=None,
                requires_trip_modification=False
            )
            
            # 收集其他Agent的结果（用于行程修改）
            additional_agent_results = []
            
            # 步骤2: 路由到对应Agent
            for intent in intents:
                if intent == "search_attraction":
                    print("📍 调用景点搜索Agent...")
                    result = self._handle_search_attraction(extracted_info, request.current_trip)
                    response.agent_responses.append(result)
                    additional_agent_results.append(f"[景点搜索结果]: {result.content}")
                elif intent == "weather_query":
                    print("🌤️  调用天气查询Agent...")
                    result = self._handle_weather_query(extracted_info, request.current_trip)
                    response.agent_responses.append(result)
                    additional_agent_results.append(f"[天气查询结果]: {result.content}")
                elif intent == "hotel_recommend":
                    print("🏨 调用酒店推荐Agent...")
                    result = self._handle_hotel_recommend(extracted_info, request.current_trip)
                    response.agent_responses.append(result)
                    additional_agent_results.append(f"[酒店推荐结果]: {result.content}")
                elif intent == "modify_trip":
                    print("📋 准备行程修改...")
                    # 标记需要行程修改，但先不执行，等待其他Agent结果
                    response.requires_trip_modification = True
                elif intent == "general_chat":
                    print("💬 处理普通对话...")
                    response.general_response = self._handle_general_chat(
                        request.user_input,
                        request.current_trip,
                        request.conversation_history
                    )
            
            # 如果需要修改行程，在所有其他Agent完成后执行
            if response.requires_trip_modification:
                print("🔄 调用行程规划Agent修改行程...")
                modify_info = extracted_info.get("modify_trip", {})
                modified_trip = self._handle_modify_trip(
                    modify_info,
                    request.current_trip,
                    "\n".join(additional_agent_results)
                )
                response.modified_trip = modified_trip
                
                # 添加行程修改的AgentResponse
                modify_summary = self._generate_modify_summary(
                    modify_info,
                    request.current_trip,
                    modified_trip
                )
                response.agent_responses.append(AgentResponse(
                    agent_type="modify_trip",
                    content=modify_summary,
                    success=True
                ))
            
            print(f"\n{'='*60}")
            print(f"✅ 对话处理完成")
            print(f"{'='*60}\n")
            
            return response
            
        except Exception as e:
            print(f"❌ 对话处理失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return DialogueResponse(
                success=False,
                recognized_intents=[],
                agent_responses=[],
                general_response=f"抱歉，处理您的请求时出错了：{str(e)}"
            )
    
    def _recognize_intent(self, user_input: str) -> Tuple[List[str], Dict[str, Any]]:
        """
        识别用户意图
        
        Args:
            user_input: 用户输入
            
        Returns:
            (意图列表, 提取的信息)
        """
        try:
            response = self.intent_agent.run(user_input)
            
            # 解析JSON响应
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                return ["general_chat"], {}
            
            result = json.loads(json_str)
            intents = result.get("intents", ["general_chat"])
            extracted_info = result.get("extracted_info", {})
            
            # 确保至少有一个意图
            if not intents:
                intents = ["general_chat"]
            
            return intents, extracted_info
            
        except Exception as e:
            print(f"⚠️  意图识别失败: {str(e)}, 使用默认意图")
            return ["general_chat"], {}
    
    def _handle_search_attraction(self, info: Dict[str, Any], current_trip: TripPlan) -> AgentResponse:
        """处理景点搜索"""
        try:
            city = info.get("search_attraction", {}).get("city", current_trip.city)
            keywords = info.get("search_attraction", {}).get("keywords", "景点")
            
            query = f"请搜索{city}的{keywords}相关景点"
            response = self.trip_planner.attraction_agent.run(query)
            
            return AgentResponse(
                agent_type="search_attraction",
                content=response,
                success=True
            )
        except Exception as e:
            return AgentResponse(
                agent_type="search_attraction",
                content=f"搜索景点失败: {str(e)}",
                success=False
            )
    
    def _handle_weather_query(self, info: Dict[str, Any], current_trip: TripPlan) -> AgentResponse:
        """处理天气查询"""
        try:
            city = info.get("weather_query", {}).get("city", current_trip.city)
            
            query = f"请查询{city}的天气信息"
            response = self.trip_planner.weather_agent.run(query)
            
            return AgentResponse(
                agent_type="weather_query",
                content=response,
                success=True
            )
        except Exception as e:
            return AgentResponse(
                agent_type="weather_query",
                content=f"查询天气失败: {str(e)}",
                success=False
            )
    
    def _handle_hotel_recommend(self, info: Dict[str, Any], current_trip: TripPlan) -> AgentResponse:
        """处理酒店推荐"""
        try:
            city = info.get("hotel_recommend", {}).get("city", current_trip.city)
            preferences = info.get("hotel_recommend", {}).get("preferences", "")
            
            query = f"请搜索{city}的酒店"
            if preferences:
                query += f"，偏好：{preferences}"
            
            response = self.trip_planner.hotel_agent.run(query)
            
            return AgentResponse(
                agent_type="hotel_recommend",
                content=response,
                success=True
            )
        except Exception as e:
            return AgentResponse(
                agent_type="hotel_recommend",
                content=f"推荐酒店失败: {str(e)}",
                success=False
            )
    
    def _handle_general_chat(
        self,
        user_input: str,
        current_trip: TripPlan,
        conversation_history: List[Message]
    ) -> str:
        """处理普通对话"""
        try:
            # 构建行程信息摘要
            trip_info = self._format_trip_info(current_trip)
            
            # 设置系统提示词
            self.general_chat_agent.system_prompt = GENERAL_CHAT_PROMPT.format(
                trip_info=trip_info
            )
            
            response = self.general_chat_agent.run(user_input)
            return response
        except Exception as e:
            return f"抱歉，我遇到了一些问题：{str(e)}"
    
    def _handle_modify_trip(
        self,
        info: Dict[str, Any],
        current_trip: TripPlan,
        additional_info: str
    ) -> TripPlan:
        """处理行程修改"""
        try:
            requirements = info.get("requirements", "")
            
            # 将当前行程转换为JSON字符串
            current_trip_json = current_trip.model_dump_json(indent=2)
            
            # 获取行程规划Agent的JSON schema（从PLANNER_AGENT_PROMPT中提取）
            from .trip_planner_agent import PLANNER_AGENT_PROMPT
            json_schema_start = PLANNER_AGENT_PROMPT.find("```json")
            json_schema_end = PLANNER_AGENT_PROMPT.find("```", json_schema_start + 7)
            json_schema = PLANNER_AGENT_PROMPT[json_schema_start:json_schema_end + 3]
            
            # 构建查询
            query = MODIFY_TRIP_PROMPT.format(
                current_trip=current_trip_json,
                user_requirements=requirements,
                additional_info=additional_info if additional_info else "无",
                json_schema=json_schema
            )
            
            # 调用行程规划Agent
            response = self.trip_planner.planner_agent.run(query)
            
            # 解析响应
            # 创建一个临时的request对象用于解析
            from ..models.schemas import TripRequest
            from datetime import datetime, timedelta
            temp_request = TripRequest(
                city=current_trip.city,
                start_date=current_trip.start_date,
                end_date=current_trip.end_date,
                travel_days=len(current_trip.days),
                transportation="",
                accommodation=""
            )
            
            modified_trip = self.trip_planner._parse_response(response, temp_request)
            return modified_trip
            
        except Exception as e:
            print(f"❌ 修改行程失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return current_trip
    
    def _generate_modify_summary(
        self,
        info: Dict[str, Any],
        original_trip: TripPlan,
        modified_trip: TripPlan
    ) -> str:
        """
        生成行程修改的摘要说明
        
        Args:
            info: 修改信息
            original_trip: 原行程
            modified_trip: 修改后的行程
            
        Returns:
            修改摘要文本
        """
        requirements = info.get("requirements", "")
        
        summary = f"""## 行程修改建议

根据您的需求：**{requirements}**，我为您重新规划了行程。

### 修改要点：
- 目的地：{modified_trip.city}
- 日期：{modified_trip.start_date} 至 {modified_trip.end_date}
- 天数：{len(modified_trip.days)}天

### 每日行程概览：
"""
        for day in modified_trip.days:
            summary += f"\n**第{day.day_index + 1}天 ({day.date})**\n"
            summary += f"- {day.description}\n"
            summary += f"- 景点：{', '.join([a.name for a in day.attractions])}\n"
        
        summary += f"\n### 总体建议：\n{modified_trip.overall_suggestions}\n"
        summary += "\n---\n\n**请确认是否应用此修改？**"
        
        return summary
    
    def _format_trip_info(self, trip: TripPlan) -> str:
        """格式化行程信息为文本"""
        info = f"""
目的地: {trip.city}
日期: {trip.start_date} 至 {trip.end_date}
天数: {len(trip.days)}天

每日行程概览:
"""
        for day in trip.days:
            info += f"  第{day.day_index + 1}天({day.date}): {day.description}\n"
            info += f"    景点: {', '.join([a.name for a in day.attractions])}\n"
        
        info += f"\n总体建议: {trip.overall_suggestions}"
        return info


# 全局对话Agent系统实例
_dialogue_agent_system = None


def get_dialogue_agent_system() -> DialogueAgentSystem:
    """获取对话Agent系统实例（单例模式）"""
    global _dialogue_agent_system
    
    if _dialogue_agent_system is None:
        _dialogue_agent_system = DialogueAgentSystem()
    
    return _dialogue_agent_system
