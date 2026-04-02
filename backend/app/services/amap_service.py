"""高德地图MCP服务封装"""

from typing import List, Dict, Any, Optional
from hello_agents.tools import MCPTool
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo

# 全局MCP工具实例
_amap_mcp_tool = None


def get_amap_mcp_tool() -> MCPTool:
    """
    获取高德地图MCP工具实例(单例模式)
    
    Returns:
        MCPTool实例
    """
    global _amap_mcp_tool
    
    if _amap_mcp_tool is None:
        settings = get_settings()
        
        if not settings.amap_api_key:
            raise ValueError("高德地图API Key未配置,请在.env文件中设置AMAP_API_KEY")
        
        # 创建MCP工具
        _amap_mcp_tool = MCPTool(
            name="amap",
            description="高德地图服务,支持POI搜索、路线规划、天气查询等功能",
            server_command=["uvx", "amap-mcp-server"],
            env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
            auto_expand=True  # 自动展开为独立工具
        )
        
        print(f"✅ 高德地图MCP工具初始化成功")
        print(f"   工具数量: {len(_amap_mcp_tool._available_tools)}")
        
        # 打印可用工具列表
        if _amap_mcp_tool._available_tools:
            print("   可用工具:")
            for tool in _amap_mcp_tool._available_tools[:5]:  # 只打印前5个
                print(f"     - {tool.get('name', 'unknown')}")
            if len(_amap_mcp_tool._available_tools) > 5:
                print(f"     ... 还有 {len(_amap_mcp_tool._available_tools) - 5} 个工具")
    
    return _amap_mcp_tool


class AmapService:
    """高德地图服务封装类"""
    
    def __init__(self):
        """初始化服务"""
        self.mcp_tool = get_amap_mcp_tool()
    
    def search_poi(self, keywords: str, city: str, citylimit: bool = True) -> List[POIInfo]:
        """
        搜索POI
        
        Args:
            keywords: 搜索关键词
            city: 城市
            citylimit: 是否限制在城市范围内
            
        Returns:
            POI信息列表
        """
        try:
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_text_search",
                "arguments": {
                    "keywords": keywords,
                    "city": city,
                    "citylimit": str(citylimit).lower()
                }
            })
            
            # 解析结果
            # 注意: MCP工具返回的是字符串,需要解析
            # 这里简化处理,实际应该解析JSON
            print(f"POI搜索结果: {result[:200]}...")  # 打印前200字符
            
            # 解析实际的POI数据
            import json
            import re
            
            pois = []
            
            if isinstance(result, str):
                # 用正则提取JSON数据
                match = re.search(r'\{.*\}', result, re.DOTALL)
                if match:
                    try:
                        parsed_dict = json.loads(match.group(0))
                        poi_list = parsed_dict.get("pois", [])
                        for poi in poi_list:
                            poi_info = POIInfo(
                                name=poi.get("name", ""),
                                location=poi.get("location", ""),
                                address=poi.get("address", ""),
                                tel=poi.get("tel", ""),
                                type=poi.get("type", ""),
                                typecode=poi.get("typecode", ""),
                                adcode=poi.get("adcode", ""),
                                citycode=poi.get("citycode", ""),
                                pcode=poi.get("pcode", ""),
                                adname=poi.get("adname", ""),
                                cityname=poi.get("cityname", ""),
                                pname=poi.get("pname", ""),
                                biz_type=poi.get("biz_type", ""),
                                business_area=poi.get("business_area", ""),
                                distance=poi.get("distance", ""),
                                photos=poi.get("photos", [])
                            )
                            pois.append(poi_info)
                    except Exception as e:
                        print(f"POI数据解析异常: {e}")
            
            return pois
            
        except Exception as e:
            print(f"❌ POI搜索失败: {str(e)}")
            return []
    
    def get_weather(self, city: str) -> List[WeatherInfo]:
        """
        查询天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息列表
        """
        try:
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_weather",
                "arguments": {
                    "city": city
                }
            })
            
            print(f"天气查询结果: {result[:200]}...")
            
            # 解析实际的天气数据
            import json
            import re
            
            weather_list = []
            
            if isinstance(result, str):
                # 用正则提取JSON数据
                match = re.search(r'\{.*\}', result, re.DOTALL)
                if match:
                    try:
                        parsed_dict = json.loads(match.group(0))
                        # 高德天气API返回的数据结构
                        lives = parsed_dict.get("lives", [])
                        forecasts = parsed_dict.get("forecasts", [])
                        
                        # 处理实时天气数据
                        for live in lives:
                            weather_info = WeatherInfo(
                                city=live.get("city", ""),
                                adcode=live.get("adcode", ""),
                                weather=live.get("weather", ""),
                                temperature=live.get("temperature", ""),
                                winddirection=live.get("winddirection", ""),
                                windpower=live.get("windpower", ""),
                                humidity=live.get("humidity", ""),
                                reporttime=live.get("reporttime", ""),
                                temperature_float=live.get("temperature_float", ""),
                                humidity_float=live.get("humidity_float", "")
                            )
                            weather_list.append(weather_info)
                        
                        # 处理预报数据（如果有）
                        for forecast in forecasts:
                            casts = forecast.get("casts", [])
                            for cast in casts:
                                weather_info = WeatherInfo(
                                    city=forecast.get("city", ""),
                                    adcode=forecast.get("adcode", ""),
                                    weather=cast.get("dayweather", ""),
                                    temperature=f"{cast.get('nighttemp', '')}-{cast.get('daytemp', '')}",
                                    winddirection=cast.get("daywind", ""),
                                    windpower=cast.get("daypower", ""),
                                    humidity="",
                                    reporttime=forecast.get("reporttime", ""),
                                    date=cast.get("date", ""),
                                    week=cast.get("week", ""),
                                    dayweather=cast.get("dayweather", ""),
                                    nightweather=cast.get("nightweather", ""),
                                    daytemp=cast.get("daytemp", ""),
                                    nighttemp=cast.get("nighttemp", ""),
                                    daywind=cast.get("daywind", ""),
                                    nightwind=cast.get("nightwind", ""),
                                    daypower=cast.get("daypower", ""),
                                    nightpower=cast.get("nightpower", "")
                                )
                                weather_list.append(weather_info)
                                
                    except Exception as e:
                        print(f"天气数据解析异常: {e}")
            
            return weather_list
            
        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []
    
    def plan_route(
        self,
        origin_address: str,
        destination_address: str,
        origin_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        route_type: str = "walking"
    ) -> Dict[str, Any]:
        """
        规划路线
        
        Args:
            origin_address: 起点地址
            destination_address: 终点地址
            origin_city: 起点城市
            destination_city: 终点城市
            route_type: 路线类型 (walking/driving/transit)
            
        Returns:
            路线信息
        """
        try:
            # 根据路线类型选择工具
            tool_map = {
                "walking": "maps_direction_walking_by_address",
                "driving": "maps_direction_driving_by_address",
                "transit": "maps_direction_transit_integrated_by_address"
            }
            
            tool_name = tool_map.get(route_type, "maps_direction_walking_by_address")
            
            # 构建参数
            arguments = {
                "origin_address": origin_address,
                "destination_address": destination_address
            }
            
            # 公共交通需要城市参数
            if route_type == "transit":
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            else:
                # 其他路线类型也可以提供城市参数提高准确性
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            
            # 调用MCP工具
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": tool_name,
                "arguments": arguments
            })
            
            print(f"路线规划结果: {result[:200]}...")
            
            # 解析实际的路线数据
            import json
            import re
            
            clean_data = {}
            
            if isinstance(result, str):
                # 用正则精准切除中文字符，只提取 {} 里的 JSON
                match = re.search(r'\{.*\}', result, re.DOTALL)
                if match:
                    try:
                        parsed_dict = json.loads(match.group(0))
                        paths = parsed_dict.get("route", {}).get("paths", [])
                        if paths:
                            # 组装结构化数据
                            clean_data = {
                                "distance": int(paths[0].get("distance", 0)),
                                "duration": int(paths[0].get("duration", 0)),
                                "route_type": route_type,
                                "description": f"获取成功！全程距离约 {int(paths[0].get('distance', 0))/1000:.1f} 公里",
                                "paths": paths,
                                "raw_response": parsed_dict
                            }
                    except Exception as e:
                        print(f"数据清洗异常: {e}")
            
            # 兜底处理
            if not clean_data:
                clean_data = {
                    "distance": 0,
                    "duration": 0,
                    "route_type": route_type,
                    "description": "已连通服务，但未获取到有效距离数据",
                    "paths": [],
                    "raw_response": {}
                }
            
            return clean_data
            
        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            return {}
    
    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        """
        地理编码(地址转坐标)

        Args:
            address: 地址
            city: 城市

        Returns:
            经纬度坐标
        """
        try:
            arguments = {"address": address}
            if city:
                arguments["city"] = city

            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_geo",
                "arguments": arguments
            })

            print(f"地理编码结果: {result[:200]}...")

            # 解析实际的坐标数据
            import json
            import re
            
            if isinstance(result, str):
                # 用正则提取JSON数据
                match = re.search(r'\{.*\}', result, re.DOTALL)
                if match:
                    try:
                        parsed_dict = json.loads(match.group(0))
                        geocodes = parsed_dict.get("geocodes", [])
                        if geocodes:
                            location_str = geocodes[0].get("location", "")
                            if location_str:
                                # 高德返回的坐标格式为 "经度,纬度"
                                lng, lat = location_str.split(",")
                                return Location(
                                    longitude=float(lng),
                                    latitude=float(lat),
                                    address=geocodes[0].get("formatted_address", address),
                                    adcode=geocodes[0].get("adcode", ""),
                                    city=geocodes[0].get("city", ""),
                                    district=geocodes[0].get("district", ""),
                                    street=geocodes[0].get("street", ""),
                                    number=geocodes[0].get("number", "")
                                )
                    except Exception as e:
                        print(f"坐标数据解析异常: {e}")
            
            return None

        except Exception as e:
            print(f"❌ 地理编码失败: {str(e)}")
            return None

    def get_poi_detail(self, poi_id: str) -> Dict[str, Any]:
        """
        获取POI详情

        Args:
            poi_id: POI ID

        Returns:
            POI详情信息
        """
        try:
            result = self.mcp_tool.run({
                "action": "call_tool",
                "tool_name": "maps_search_detail",
                "arguments": {
                    "id": poi_id
                }
            })

            print(f"POI详情结果: {result[:200]}...")

            # 解析结果并提取图片
            import json
            import re

            # 尝试从结果中提取JSON
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data

            return {"raw": result}

        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}


# 创建全局服务实例
_amap_service = None


def get_amap_service() -> AmapService:
    """获取高德地图服务实例(单例模式)"""
    global _amap_service
    
    if _amap_service is None:
        _amap_service = AmapService()
    
    return _amap_service

