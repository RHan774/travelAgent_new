"""对话API路由"""

from fastapi import APIRouter, HTTPException
from ...models.schemas import (
    DialogueRequest,
    DialogueResponse,
    ErrorResponse
)
from ...agents.dialogue_agent import get_dialogue_agent_system

router = APIRouter(prefix="/chat", tags=["对话"])


@router.post(
    "/message",
    response_model=DialogueResponse,
    summary="发送对话消息",
    description="发送用户消息并获取Agent响应"
)
async def send_chat_message(request: DialogueRequest):
    """
    发送对话消息
    
    Args:
        request: 对话请求
        
    Returns:
        对话响应
    """
    try:
        print(f"\n{'='*60}")
        print(f"📥 收到对话请求")
        print(f"{'='*60}\n")
        
        # 获取对话Agent系统实例
        agent_system = get_dialogue_agent_system()
        
        # 处理对话
        response = agent_system.process_dialogue(request)
        
        print(f"✅ 对话处理完成，准备返回响应\n")
        
        return response
        
    except Exception as e:
        print(f"❌ 处理对话失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"处理对话失败: {str(e)}"
        )


@router.get(
    "/health",
    summary="健康检查",
    description="检查对话服务是否正常"
)
async def health_check():
    """健康检查"""
    try:
        # 检查Agent系统是否可用
        agent_system = get_dialogue_agent_system()
        
        return {
            "status": "healthy",
            "service": "chat-agent"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"服务不可用: {str(e)}"
        )
