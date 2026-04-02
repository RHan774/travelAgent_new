# test_mcp_tools.py
import json
from app.services.amap_service import get_amap_mcp_tool
 
def run_xray_test():
    print("====== 🚀 MCP 插件底层 X光扫描 ======\n")
    
    try:
        # 1. 启动并获取工具
        tool = get_amap_mcp_tool()
        tools_list = tool._available_tools
        
        if not tools_list:
            print("❌ 致命错误：没有读取到任何可用工具！")
            return
 
        print(f"✅ 成功连接 MCP，共扫描到 {len(tools_list)} 个底层工具\n")
        
        # 2. 扒出搜索和天气的“真实名字”和“参数清单”
        print("====== 🔍 重点排查：工具真实身份与参数要求 ======")
        for t in tools_list:
            name = t.get('name', '未知')
            schema = t.get('inputSchema', {})
            # 只过滤出包含天气、搜索、路线相关的工具
            if 'weather' in name or 'search' in name or 'poi' in name:
                print(f"👉 发现工具: {name}")
                print(f"   需要参数: {json.dumps(schema, ensure_ascii=False)}")
                print("-" * 50)
                
        # 3. 暴力裸调：天气查询
        print("\n====== ⚡ 暴力裸调测试：天气 (maps_weather) ======")
        try:
            res_weather = tool.run({
                "action": "call_tool",
                "tool_name": "maps_weather",
                "arguments": {"city": "北京"} # 看看只传北京行不行
            })
            print(f"☁️ 天气返回结果: {str(res_weather)[:200]}...")
        except Exception as e:
            print(f"❌ 天气调用崩溃: {e}")
 
        # 4. 暴力裸调：景点搜索
        print("\n====== ⚡ 暴力裸调测试：搜索 (maps_text_search) ======")
        try:
            res_search = tool.run({
                "action": "call_tool",
                "tool_name": "maps_text_search",
                "arguments": {"keywords": "故宫", "city": "北京"}
            })
            print(f"🏛️ 搜索返回结果: {str(res_search)[:200]}...")
        except Exception as e:
            print(f"❌ 搜索调用崩溃: {e}")
 
    except Exception as e:
        print(f"❌ X光机启动失败: {e}")
 
if __name__ == "__main__":
    run_xray_test()