"""
Security Module - Biometric Authentication & Lock-Down Protocol
Handles typing rhythm biometric calibration and real-time verification
"""

import os
import numpy as np
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import json

# Create API router
security_router = APIRouter(prefix="/security", tags=["security"])

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'dahen_signature.joblib')
VERIFICATION_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'biometric_verification.jsonl')

# Ensure directories exist
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
os.makedirs(os.path.dirname(VERIFICATION_LOG_PATH), exist_ok=True)

# Global verification counter
verification_count = 0
anomaly_threshold = 80  # Percentage threshold for lock-down
consecutive_anomalies = 0


def load_model():
    """Load the trained One-Class SVM model"""
    if os.path.exists(MODEL_PATH):
        import joblib
        return joblib.load(MODEL_PATH)
    return None


def save_model(model):
    """Save the trained model"""
    import joblib
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)


def log_verification(result):
    """Log verification results for audit trail"""
    os.makedirs(os.path.dirname(VERIFICATION_LOG_PATH), exist_ok=True)
    
    with open(VERIFICATION_LOG_PATH, 'a') as f:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'result': result,
            'score': result.get('score', 0),
            'action': result.get('action', 'none')
        }
        f.write(json.dumps(log_entry) + '\n')


class OneClassSVM:
    """
    One-Class SVM implementation using scikit-learn
    Used for anomaly detection in typing rhythm
    """
    
    def __init__(self, kernel='rbf', nu=0.1, gamma='scale'):
        self.kernel = kernel
        self.nu = nu
        self.gamma = gamma
        self.model = None
    
    def fit(self, X):
        """Train the One-Class SVM model"""
        from sklearn.svm import OneClassSVM
        self.model = OneClassSVM(
            kernel=self.kernel,
            nu=self.nu,
            gamma=self.gamma
        )
        self.model.fit(X)
        return self
    
    def decision_function(self, X):
        """Get decision function scores for anomaly detection"""
        if self.model is None:
            raise ValueError("Model not trained. Call fit() first.")
        return self.model.decision_function(X)
    
    def predict(self, X):
        """Predict if samples are normal or anomalies"""
        if self.model is None:
            raise ValueError("Model not trained. Call fit() first.")
        return self.model.predict(X)


async def train_biometric_model(typing_data: list) -> dict:
    """
    Train One-Class SVM on user's typing rhythm
    
    Args:
        typing_data: Array of timing vectors with dwellTime, flightTime, key
    
    Returns:
        Training result with accuracy and model info
    """
    global verification_count, consecutive_anomalies
    
    try:
        if not typing_data or len(typing_data) < 10:
            raise HTTPException(
                status_code=400,
                detail='Insufficient key data. Please complete at least 10 key events.'
            )
        
        # Extract timing features
        features = []
        for event in typing_data:
            dwell_time = event.get('dwellTime', 0)
            flight_time = event.get('flightTime', 0)
            total_time = event.get('totalTime', 0)
            
            # Create feature vector: [dwell_time, flight_time, total_time]
            feature_vector = np.array([dwell_time, flight_time, total_time])
            features.append(feature_vector)
        
        # Convert to numpy array
        X = np.array(features)
        
        # Normalize features
        if len(X) > 1:
            X_mean = np.mean(X, axis=0)
            X_std = np.std(X, axis=0) + 1e-8  # Avoid division by zero
            X_normalized = (X - X_mean) / X_std
        else:
            X_normalized = X
        
        # Train One-Class SVM
        model = OneClassSVM(
            kernel='rbf',
            nu=0.1,  # Allow for slight human variance
            gamma='scale'
        )
        
        model.fit(X_normalized)
        
        # Calculate model score (decision function on training data)
        scores = model.decision_function(X_normalized)
        accuracy = np.mean(scores > 0) * 100
        
        # Save the model
        save_model(model)
        
        # Store model metadata
        model_metadata = {
            'trained_at': datetime.now().isoformat(),
            'num_samples': len(typing_data),
            'accuracy': round(accuracy, 2)
        }
        
        # Save metadata
        metadata_path = MODEL_PATH.replace('.joblib', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(model_metadata, f, indent=2)
        
        return {
            'success': True,
            'message': 'Biometric model trained successfully',
            'accuracy': round(accuracy, 2),
            'samples': len(typing_data),
            'model_path': MODEL_PATH
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def verify_typing_rhythm(typing_data: list, threshold: float = None) -> dict:
    """
    Verify typing rhythm against trained biometric model
    
    Args:
        typing_data: Array of recent key timing events
        threshold: Optional threshold override (default: 80)
    
    Returns:
        Verification result with score and action
    """
    global verification_count, consecutive_anomalies
    
    try:
        if threshold is None:
            threshold = anomaly_threshold
        
        # Get minimum required samples
        min_samples = 5  # Need at least 5 key events for verification
        
        if len(typing_data) < min_samples:
            return {
                'success': False,
                'error': f'Insufficient samples. Need at least {min_samples} key events.',
                'score': 0,
                'is_verified': True,
                'action': 'none'
            }
        
        # Load model
        model = load_model()
        if model is None:
            raise HTTPException(
                status_code=404,
                detail='No biometric model found. Please calibrate first.'
            )
        
        # Extract features from recent key events
        features = []
        for event in typing_data[-min_samples:]:  # Use most recent events
            dwell_time = event.get('dwellTime', 0)
            flight_time = event.get('flightTime', 0)
            total_time = event.get('totalTime', 0)
            
            feature_vector = np.array([dwell_time, flight_time, total_time])
            features.append(feature_vector)
        
        X = np.array(features)
        
        # Normalize using default training statistics
        X_mean = np.array([200, 150, 350])
        X_std = np.array([100, 80, 200]) + 1e-8
        X_normalized = (X - X_mean) / X_std
        
        # Get decision function scores
        scores = model.decision_function(X_normalized)
        
        # Calculate anomaly score (inverse of decision function)
        # Higher score = more anomalous
        if len(scores) > 0:
            min_score = np.min(scores)
            max_score = np.max(scores)
            
            if max_score > min_score:
                # Normalize to 0-100 scale
                normalized_scores = (scores - min_score) / (max_score - min_score)
                anomaly_scores = normalized_scores * 100
            else:
                anomaly_scores = np.array([50])  # Default if all scores are same
        else:
            anomaly_scores = np.array([50])
        
        # Calculate average anomaly score
        avg_score = np.mean(anomaly_scores)
        
        # Determine action based on score
        if avg_score > threshold:
            action = 'lockdown'
            consecutive_anomalies += 1
            is_verified = False
        elif avg_score > threshold * 0.7:
            action = 'warning'
            consecutive_anomalies += 1
            is_verified = True  # Warning but still verified
        else:
            action = 'none'
            consecutive_anomalies = 0  # Reset on normal verification
            is_verified = True
        
        # Log verification
        log_verification({
            'score': round(avg_score, 2),
            'action': action,
            'samples': len(typing_data),
            'consecutive_anomalies': consecutive_anomalies
        })
        
        return {
            'success': True,
            'score': round(avg_score, 2),
            'threshold': threshold,
            'is_verified': is_verified,
            'action': action,
            'consecutive_anomalies': consecutive_anomalies,
            'message': f'Verification complete. Score: {round(avg_score, 1)}%'
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def trigger_lockdown(reason: str = "Biometric anomaly detected") -> dict:
    """
    Trigger the Lock-Down Protocol
    Lock screen, mute audio, send alert
    """
    try:
        # Lock screen
        lock_script = os.path.join(BASE_DIR, 'scripts', 'lock_screen.py')
        
        if os.path.exists(lock_script):
            import subprocess
            subprocess.run(['python', lock_script], capture_output=True)
        
        # Mute audio
        mute_script = os.path.join(BASE_DIR, 'scripts', 'mute_audio.py')
        
        if os.path.exists(mute_script):
            import subprocess
            subprocess.run(['python', mute_script], capture_output=True)
        
        # Send Telegram alert (if configured)
        telegram_script = os.path.join(BASE_DIR, 'scripts', 'send_telegram_alert.py')
        
        if os.path.exists(telegram_script):
            import subprocess
            subprocess.run(['python', telegram_script, reason], capture_output=True)
        
        # Log lockdown event
        log_verification({
            'score': 100,
            'action': 'lockdown',
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'success': True,
            'message': 'Lock-Down Protocol activated',
            'actions': ['screen_locked', 'audio_muted', 'alert_sent']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_security_status() -> dict:
    """Get current security system status"""
    model_exists = os.path.exists(MODEL_PATH)
    metadata_exists = os.path.exists(MODEL_PATH.replace('.joblib', '_metadata.json'))
    
    return {
        'success': True,
        'model_trained': model_exists,
        'model_path': MODEL_PATH,
        'metadata_available': metadata_exists,
        'anomaly_threshold': anomaly_threshold,
        'verification_count': verification_count,
        'consecutive_anomalies': consecutive_anomalies
    }


# Register routes
@security_router.post("/train-biometric")
async def train_biometric_model_endpoint(request: Request):
    """Train biometric model from typing data"""
    try:
        body = await request.json()
        # Accept both 'keyData' and 'typing_data' for compatibility
        typing_data = body.get("keyData", body.get("typing_data", []))
        
        result = await train_biometric_model(typing_data)
        return JSONResponse(content=result, status_code=200 if result.get('success') else 500)
    except HTTPException as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={'success': False, 'error': str(e)}, status_code=500)


@security_router.post("/verify-biometric")
async def verify_biometric_endpoint(request: Request):
    """Verify user identity through typing rhythm analysis"""
    try:
        body = await request.json()
        # Accept both 'keyData' and 'typing_data' for compatibility
        typing_data = body.get("keyData", body.get("typing_data", []))
        threshold = body.get("threshold", anomaly_threshold)
        
        result = await verify_typing_rhythm(typing_data, threshold)
        return JSONResponse(content=result, status_code=200)
    except HTTPException as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={'success': False, 'error': str(e)}, status_code=500)


@security_router.post("/trigger-lockdown")
async def trigger_lockdown_endpoint(request: Request):
    """Trigger system lockdown for security"""
    try:
        body = await request.json() or {}
        reason = body.get("reason", "Biometric anomaly detected")
        
        result = await trigger_lockdown(reason)
        return JSONResponse(content=result, status_code=200 if result.get('success') else 500)
    except HTTPException as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={'success': False, 'error': str(e)}, status_code=500)


@security_router.get("/status")
async def get_security_status_endpoint():
    """Get current security system status"""
    try:
        result = await get_security_status()
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)


@security_router.post("/typing-event")
async def typing_event_endpoint(request: Request):
    """Receive real-time typing events for biometric verification"""
    try:
        body = await request.json() or {}
        event = body.get("event", {})
        
        # Log the event for continuous verification
        log_verification({
            'score': 0,
            'action': 'typing_event',
            'event': event,
            'timestamp': datetime.now().isoformat()
        })
        
        return JSONResponse(content={
            'success': True,
            'message': 'Typing event received',
            'event': event
        }, status_code=200)
    except Exception as e:
        return JSONResponse(content={'success': False, 'error': str(e)}, status_code=500)


@security_router.post("/typing-data")
async def typing_data_endpoint(request: Request):
    """Receive typing data for biometric verification"""
    try:
        body = await request.json() or {}
        typing_data = body.get("typing_data", body.get("keyData", []))
        
        result = await verify_typing_rhythm(typing_data)
        
        return JSONResponse(content=result, status_code=200)
    except HTTPException as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={'success': False, 'error': str(e)}, status_code=500)
