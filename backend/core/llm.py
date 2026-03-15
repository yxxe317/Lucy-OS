# backend/core/llm.py
import httpx
import logging
import sqlite3
import asyncio
import json
from typing import Optional, Dict, AsyncGenerator
from datetime import datetime
from core.evolution import evolution

logger = logging.getLogger("LLM")

LM_STUDIO_URL = "http://127.0.0.1:1234/v1"
DEFAULT_MODEL = "local-model"

class LLM:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model_name = DEFAULT_MODEL
        self.client = httpx.AsyncClient(timeout=120.0)

    async def generate(self, prompt: str, system_prompt: str = "", 
                      user_id: int = 1, emotion: str = "neutral") -> str:
        """Original non-streaming generate method (keep for compatibility)"""
        try:
            start_time = datetime.now()
            
            # Try to get best prompt, but don't fail if method doesn't exist
            try:
                best_prompt = await evolution.get_best_prompt(system_prompt)
            except AttributeError:
                # If method doesn't exist, just use original system_prompt
                best_prompt = system_prompt
                logger.warning("⚠️ evolution.get_best_prompt not available, using default")
            
            messages = []
            if best_prompt:
                messages.append({"role": "system", "content": best_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4096,
                    "stream": False
                }
            )
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                
                # Track success for evolution
                asyncio.create_task(
                    evolution.evaluate_response_success(
                        prompt=prompt,
                        response=content,
                        user_id=user_id,
                        response_time=response_time,
                        emotion=emotion
                    )
                )
                return content
            else:
                return f"Error: LM Studio returned status {response.status_code}"
                
        except httpx.ConnectError:
            return "❌ Cannot connect to LM Studio. Please start the server on port 1234."
        except Exception as e:
            logger.error(f"❌ Generation error: {e}")
            return f"Error: {str(e)}"

    async def generate_stream(self, prompt: str, system_prompt: str = "", 
                             user_id: int = 1, emotion: str = "neutral") -> AsyncGenerator[str, None]:
        """
        NEW: Generate response in chunks for real-time streaming
        Yields text chunks as they arrive from LM Studio
        """
        try:
            start_time = datetime.now()
            
            # Get best evolved prompt
            try:
                best_prompt = await evolution.get_best_prompt(system_prompt)
            except AttributeError:
                best_prompt = system_prompt
            
            messages = []
            if best_prompt:
                messages.append({"role": "system", "content": best_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Use streaming endpoint
            async with self.client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4096,
                    "stream": True  # 👈 ENABLE STREAMING
                }
            ) as response:
                
                full_response = ""
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and chunk["choices"]:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    content = delta["content"]
                                    full_response += content
                                    yield content  # 👈 SEND CHUNK TO FRONTEND
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            logger.error(f"Error parsing chunk: {e}")
                            continue
                
                # Track success for evolution after full response
                response_time = (datetime.now() - start_time).total_seconds()
                asyncio.create_task(
                    evolution.evaluate_response_success(
                        prompt=prompt,
                        response=full_response,
                        user_id=user_id,
                        response_time=response_time,
                        emotion=emotion
                    )
                )
                
        except httpx.ConnectError:
            yield "❌ Cannot connect to LM Studio. Please start the server on port 1234."
        except Exception as e:
            logger.error(f"❌ Stream error: {e}")
            yield f"Error: {str(e)}"

    async def ensemble_generate(self, query: str, system_prompt: str = "") -> Dict:
        """Query multiple models and pick best"""
        responses = {}
        
        # Try different temperatures for variety
        temps = [0.3, 0.7, 0.9]
        for i, temp in enumerate(temps):
            try:
                response = await self.client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model_name,
                        "messages": [{"role": "user", "content": query}],
                        "temperature": temp,
                        "max_tokens": 2048
                    }
                )
                if response.status_code == 200:
                    result = response.json()
                    responses[f"model_{i}"] = result["choices"][0]["message"]["content"].strip()
            except:
                responses[f"model_{i}"] = "[failed]"
        
        # Pick longest response as best (simple heuristic)
        best = max(responses.values(), key=len) if responses else "No response"
        
        return {
            "response": best,
            "all_responses": responses,
            "model_used": "ensemble"
        }

    async def learn_from_feedback(self, response_id: str, feedback: int):
        """Learn from user feedback"""
        conn = sqlite3.connect("data/evolution.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE success_metrics
            SET user_feedback = ?
            WHERE response_id = ?
        ''', (feedback, response_id))
        conn.commit()
        conn.close()
        await evolution.evolve_prompts()

    def set_model(self, model_name: str):
        self.model_name = model_name
        logger.info(f"🎯 Model set to: {model_name}")

    def get_model(self) -> str:
        return self.model_name

    async def close(self):
        await self.client.aclose()

# Global instance
llm = LLM()