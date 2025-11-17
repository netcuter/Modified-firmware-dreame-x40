"""FastAPI server for Dreame X40 AI Assistant"""

import logging
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..config import get_config
from ..valetudo import ValetudoAPIClient, CommandMapper
from ..ai import AIManager, PromptTemplates
from .websocket import ws_manager

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Dreame X40 AI Assistant API",
    description="AI-powered interface for Dreame X40 with Valetudo",
    version="1.0.0"
)

# Configure CORS
config = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
valetudo_client: Optional[ValetudoAPIClient] = None
ai_manager: Optional[AIManager] = None
command_mapper: Optional[CommandMapper] = None


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    include_context: bool = True


class ChatResponse(BaseModel):
    response: str
    model_used: str
    intent: Optional[str] = None


class CommandRequest(BaseModel):
    command: str


class ModelSwitchRequest(BaseModel):
    model: str  # "local", "openai", "anthropic", "google"


class RobotStatusResponse(BaseModel):
    state: str
    battery: int
    error: Optional[str] = None


# Startup/Shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize clients on startup"""
    global valetudo_client, ai_manager, command_mapper

    logger.info("Starting Dreame X40 AI Assistant API...")

    # Initialize Valetudo client
    valetudo_config = config.valetudo
    base_url = f"{valetudo_config.protocol}://{valetudo_config.host}:{valetudo_config.port}{valetudo_config.api_base}"

    valetudo_client = ValetudoAPIClient(
        base_url=base_url,
        timeout=valetudo_config.timeout
    )
    logger.info("Valetudo client initialized")

    # Initialize AI manager
    ai_manager = AIManager(config.ai)
    await ai_manager.initialize()
    logger.info("AI manager initialized")

    # Initialize command mapper
    command_mapper = CommandMapper(language=config.ai.language)
    logger.info("Command mapper initialized")

    logger.info("API server ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down API server...")

    if valetudo_client:
        await valetudo_client.close()

    if ai_manager:
        await ai_manager.close()

    logger.info("API server stopped")


# API Routes
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Dreame X40 AI Assistant API",
        "version": "1.0.0",
        "status": "running"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    valetudo_healthy = False
    ai_healthy = False

    try:
        await valetudo_client.get_robot_info()
        valetudo_healthy = True
    except:
        pass

    try:
        available_models = ai_manager.get_available_models()
        ai_healthy = len(available_models) > 0
    except:
        pass

    return {
        "status": "healthy" if (valetudo_healthy and ai_healthy) else "degraded",
        "valetudo": "connected" if valetudo_healthy else "disconnected",
        "ai": "available" if ai_healthy else "unavailable",
        "available_models": ai_manager.get_available_models() if ai_healthy else []
    }


# === Robot Status ===
@router.get("/robot/status", response_model=RobotStatusResponse)
async def get_robot_status():
    """Get current robot status"""
    try:
        status = await valetudo_client.get_friendly_status()
        return RobotStatusResponse(
            state=status.state,
            battery=status.battery,
            error=status.error
        )
    except Exception as e:
        logger.error(f"Failed to get robot status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/robot/info")
async def get_robot_info():
    """Get robot information"""
    try:
        return await valetudo_client.get_robot_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/robot/capabilities")
async def get_robot_capabilities():
    """Get robot capabilities"""
    try:
        return await valetudo_client.get_capabilities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Robot Control ===
@router.post("/robot/start")
async def start_cleaning():
    """Start full cleaning"""
    try:
        result = await valetudo_client.start_cleaning()
        return {"status": "success", "message": "Cleaning started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/robot/stop")
async def stop_cleaning():
    """Stop cleaning"""
    try:
        result = await valetudo_client.stop_cleaning()
        return {"status": "success", "message": "Cleaning stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/robot/pause")
async def pause_cleaning():
    """Pause cleaning"""
    try:
        result = await valetudo_client.pause_cleaning()
        return {"status": "success", "message": "Cleaning paused"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/robot/home")
async def return_home():
    """Return to dock"""
    try:
        result = await valetudo_client.return_to_dock()
        return {"status": "success", "message": "Returning to dock"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/robot/locate")
async def locate_robot():
    """Play locate sound"""
    try:
        result = await valetudo_client.locate_robot()
        return {"status": "success", "message": "Playing locate sound"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === AI Chat ===
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with AI assistant"""
    try:
        # Get robot context if requested
        context = None
        if request.include_context:
            try:
                status = await valetudo_client.get_friendly_status()
                context = {
                    "state": status.state,
                    "battery": status.battery
                }
            except:
                logger.warning("Failed to get robot context")

        # Parse command to detect intent
        parsed_command = command_mapper.parse_command(request.message)

        # Get AI response
        response = await ai_manager.chat(request.message, context=context)

        # Extract intent if command was parsed
        intent = parsed_command.action if parsed_command else None

        # If command detected, execute it
        if parsed_command and parsed_command.confidence > 0.7:
            try:
                await execute_command(parsed_command.action, parsed_command.params)
            except Exception as e:
                logger.error(f"Failed to execute command: {e}")

        return ChatResponse(
            response=response,
            model_used=ai_manager.get_current_model(),
            intent=intent
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def execute_command(action: str, params: dict):
    """Execute robot command

    Args:
        action: Command action
        params: Command parameters
    """
    if action == "start_cleaning":
        await valetudo_client.start_cleaning()
    elif action == "stop":
        await valetudo_client.stop_cleaning()
    elif action == "pause":
        await valetudo_client.pause_cleaning()
    elif action == "home":
        await valetudo_client.return_to_dock()
    elif action == "locate":
        await valetudo_client.locate_robot()
    # Add more commands as needed


# === AI Model Management ===
@router.get("/ai/models")
async def get_available_models():
    """Get available AI models"""
    return {
        "current": ai_manager.get_current_model(),
        "available": ai_manager.get_available_models()
    }


@router.post("/ai/switch-model")
async def switch_model(request: ModelSwitchRequest):
    """Switch AI model"""
    try:
        ai_manager.switch_model(request.model)
        return {
            "status": "success",
            "current_model": ai_manager.get_current_model()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ai/clear-history")
async def clear_history():
    """Clear conversation history"""
    ai_manager.clear_history()
    return {"status": "success", "message": "History cleared"}


@router.get("/ai/history")
async def get_history():
    """Get conversation history"""
    return ai_manager.get_history()


# === WebSocket for real-time chat ===
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await ws_manager.connect(websocket)

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "")

            if not message:
                continue

            # Get context
            context = None
            try:
                status = await valetudo_client.get_friendly_status()
                context = {
                    "state": status.state,
                    "battery": status.battery
                }
            except:
                pass

            # Parse command
            parsed_command = command_mapper.parse_command(message)

            # Get AI response
            try:
                response = await ai_manager.chat(message, context=context)

                # Send response
                await ws_manager.send_personal_message({
                    "type": "message",
                    "response": response,
                    "model": ai_manager.get_current_model(),
                    "intent": parsed_command.action if parsed_command else None
                }, websocket)

                # Execute command if detected
                if parsed_command and parsed_command.confidence > 0.7:
                    try:
                        await execute_command(parsed_command.action, parsed_command.params)
                        # Send status update
                        await ws_manager.send_personal_message({
                            "type": "command_executed",
                            "action": parsed_command.action
                        }, websocket)
                    except Exception as e:
                        logger.error(f"Command execution failed: {e}")
                        await ws_manager.send_personal_message({
                            "type": "error",
                            "message": f"Failed to execute command: {e}"
                        }, websocket)

            except Exception as e:
                logger.error(f"Chat error: {e}")
                await ws_manager.send_personal_message({
                    "type": "error",
                    "message": str(e)
                }, websocket)

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)


# Include router
app.include_router(router, prefix="/api/v1")
