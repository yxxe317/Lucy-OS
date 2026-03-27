# ============================================================================
# LUCY_OS 2.0 - SETTINGS ROUTES
# FastAPI Endpoints for Master Configuration and VRAM Management
# ============================================================================
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from pathlib import Path

router = APIRouter(prefix="/settings", tags=["settings"])

# ============================================================================
# Pydantic Models
# ============================================================================

class VRAMAllocationRequest(BaseModel):
    model_name: str
    requested_gb: float = Field(..., gt=0, le=6)
    priority: int = Field(default=1, ge=1, le=5)

class VRAMAllocationResponse(BaseModel):
    success: bool
    message: str
    allocated_gb: Optional[float] = None
    available_gb: Optional[float] = None

class HardwareHealthRequest(BaseModel):
    gpu_temp: Optional[float] = None
    fan_speed: Optional[int] = None
    disk_temp: Optional[int] = None

class HardwareHealthResponse(BaseModel):
    gpu_temp: float
    fan_speed: int
    disk_temp: int
    disk_cycles: int
    voltage: float

class SystemConfigRequest(BaseModel):
    autonomy_level: Optional[int] = Field(default=10, ge=1, le=10)
    max_vram_gb: Optional[float] = Field(default=6.0, gt=0)
    max_temp_c: Optional[int] = Field(default=85, gt=0)
    fan_speed_auto: Optional[bool] = True
    auction_enabled: Optional[bool] = True

class SystemConfigResponse(BaseModel):
    autonomy_level: int
    max_vram_gb: float
    max_temp_c: int
    fan_speed_auto: bool
    auction_enabled: bool
    version: str

class TaskHistoryItem(BaseModel):
    task_id: str
    behavior_name: str
    routine_number: int
    priority: int
    message: str
    action_type: str
    status: str
    timestamp: str

class TaskHistoryResponse(BaseModel):
    tasks: List[TaskHistoryItem]
    total_count: int

# ============================================================================
# Settings Router Endpoints
# ============================================================================

@router.get("/master", response_model=SystemConfigResponse)
async def get_master_config():
    """Get master configuration from settings_master.json"""
    config_path = Path("backend/data/settings_master.json")
    
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="Master configuration not found")
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    return SystemConfigResponse(
        autonomy_level=config.get("lucy_os", {}).get("autonomy_level", 10),
        max_vram_gb=config.get("hardware", {}).get("gpu", {}).get("vram_limit_gb", 6.0),
        max_temp_c=config.get("hardware", {}).get("gpu", {}).get("temp_threshold", 85),
        fan_speed_auto=config.get("autonomy", {}).get("fan_speed_auto", True),
        auction_enabled=config.get("hardware", {}).get("memory", {}).get("auction_enabled", True),
        version=config.get("version", "2.0.0")
    )

@router.post("/master", response_model=SystemConfigResponse)
async def update_master_config(config: SystemConfigRequest):
    """Update master configuration"""
    config_path = Path("backend/data/settings_master.json")
    
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="Master configuration not found")
    
    with open(config_path, "r") as f:
        master_config = json.load(f)
    
    # Update configuration
    if config.autonomy_level is not None:
        master_config["lucy_os"]["autonomy_level"] = config.autonomy_level
    if config.max_vram_gb is not None:
        master_config["hardware"]["gpu"]["vram_limit_gb"] = config.max_vram_gb
    if config.max_temp_c is not None:
        master_config["hardware"]["gpu"]["temp_threshold"] = config.max_temp_c
    if config.fan_speed_auto is not None:
        master_config["autonomy"]["fan_speed_auto"] = config.fan_speed_auto
    if config.auction_enabled is not None:
        master_config["hardware"]["memory"]["auction_enabled"] = config.auction_enabled
    
    with open(config_path, "w") as f:
        json.dump(master_config, f, indent=2)
    
    return SystemConfigResponse(
        autonomy_level=config.autonomy_level or master_config["lucy_os"]["autonomy_level"],
        max_vram_gb=config.max_vram_gb or master_config["hardware"]["gpu"]["vram_limit_gb"],
        max_temp_c=config.max_temp_c or master_config["hardware"]["gpu"]["temp_threshold"],
        fan_speed_auto=config.fan_speed_auto or master_config["autonomy"]["fan_speed_auto"],
        auction_enabled=config.auction_enabled or master_config["hardware"]["memory"]["auction_enabled"],
        version=master_config.get("version", "2.0.0")
    )

@router.get("/vram", response_model=VRAMAllocationResponse)
async def get_vram_status():
    """Get current VRAM allocation status"""
    # TODO: Integrate with VRAMManager
    return VRAMAllocationResponse(
        success=True,
        message="VRAM status retrieved successfully",
        allocated_gb=4.0,
        available_gb=2.0
    )

@router.post("/vram/allocate", response_model=VRAMAllocationResponse)
async def allocate_vram(request: VRAMAllocationRequest):
    """Allocate VRAM for a model"""
    # TODO: Integrate with VRAMManager
    if request.requested_gb > 6.0:
        return VRAMAllocationResponse(
            success=False,
            message="Requested VRAM exceeds maximum limit"
        )
    
    return VRAMAllocationResponse(
        success=True,
        message=f"Allocated {request.requested_gb}GB to {request.model_name}",
        allocated_gb=request.requested_gb,
        available_gb=max(0, 6.0 - request.requested_gb)
    )

@router.get("/hardware/health", response_model=HardwareHealthResponse)
async def get_hardware_health():
    """Get current hardware health status"""
    try:
        import psutil
        import subprocess
        
        # Get GPU temperature (mock for now)
        gpu_temp = 65.0  # Mock value
        
        # Get fan speed (mock for now)
        fan_speed = 45  # Mock value
        
        # Get disk temperature
        disk_temp = 45  # Mock value
        
        # Get disk cycles
        disk_cycles = 123456  # Mock value
        
        # Get voltage
        voltage = 12.0  # Mock value
        
        return HardwareHealthResponse(
            gpu_temp=gpu_temp,
            fan_speed=fan_speed,
            disk_temp=disk_temp,
            disk_cycles=disk_cycles,
            voltage=voltage
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get hardware health: {str(e)}")

@router.post("/hardware/health", response_model=HardwareHealthResponse)
async def update_hardware_health(request: HardwareHealthRequest):
    """Update hardware health readings"""
    # TODO: Store hardware health readings
    return HardwareHealthResponse(
        gpu_temp=request.gpu_temp or 65.0,
        fan_speed=request.fan_speed or 45,
        disk_temp=request.disk_temp or 45,
        disk_cycles=123456,
        voltage=12.0
    )

@router.get("/tasks/history", response_model=TaskHistoryResponse)
async def get_task_history(limit: int = 50):
    """Get task history"""
    # TODO: Integrate with routine managers
    sample_tasks = [
        TaskHistoryItem(
            task_id=f"task_{i}",
            behavior_name=f"routine_{i}",
            routine_number=i % 81 + 1,
            priority=i % 10,
            message=f"Sample task message {i}",
            action_type="test",
            status="completed",
            timestamp=datetime.now().isoformat()
        )
        for i in range(limit)
    ]
    
    return TaskHistoryResponse(
        tasks=sample_tasks,
        total_count=len(sample_tasks)
    )

@router.get("/layers/status", response_model=Dict[str, Any])
async def get_layers_status():
    """Get status of all routine layers"""
    return {
        "base": {"enabled": True, "routines": 15, "status": "active"},
        "advanced": {"enabled": True, "routines": 20, "status": "active"},
        "ultra": {"enabled": True, "routines": 20, "status": "active"},
        "omega": {"enabled": True, "routines": 20, "status": "active"}
    }

@router.get("/voice/engine", response_model=Dict[str, Any])
async def get_voice_engine_status():
    """Get E2-TTS voice engine status"""
    return {
        "engine": "E2-TTS",
        "status": "ready",
        "emotion_range": ["calm", "excited", "serious", "warm", "neutral", "concerned", "curious", "confident"],
        "breath_enabled": True,
        "pause_enabled": True
    }

@router.post("/voice/synthesize")
async def synthesize_voice(text: str, emotion: str = "neutral") -> Dict[str, Any]:
    """Synthesize voice using E2-TTS"""
    # TODO: Integrate with E2TTSVoiceEngine
    return {
        "success": True,
        "message": f"Synthesized: {text[:50]}...",
        "emotion": emotion,
        "audio_length_ms": 5000
    }

@router.get("/dashboard/config")
async def get_dashboard_config():
    """Get dashboard configuration"""
    return {
        "cognitive": True,
        "hardware_monitor": True,
        "task_history": True,
        "visualizer": True,
        "sovereign_status": True
    }

# ============================================================================
# Health Check
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }