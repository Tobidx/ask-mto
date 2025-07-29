"""
Azure Monitor Integration for Ask MTO RAG System
Simple monitoring and telemetry for production deployment
"""

import os
import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.tracer import Tracer
from opencensus.trace import config_integration
from opencensus.trace.samplers import ProbabilitySampler

# Azure Monitor Configuration
AZURE_CONNECTION_STRING = os.getenv("AZURE_MONITOR_CONNECTION_STRING")
APP_INSIGHTS_KEY = os.getenv("AZURE_APP_INSIGHTS_KEY")

class AzureMonitor:
    """Simple Azure Monitor wrapper for the Ask MTO application"""
    
    def __init__(self):
        self.enabled = bool(AZURE_CONNECTION_STRING or APP_INSIGHTS_KEY)
        self.logger = None
        self.tracer = None
        
        if self.enabled:
            self._setup_logging()
            self._setup_tracing()
        else:
            print("Azure Monitor not configured - using local logging only")
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
    
    def _setup_logging(self):
        """Setup Azure Log Analytics integration"""
        try:
            # Create logger
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            
            # Add Azure handler if connection string available
            if AZURE_CONNECTION_STRING:
                azure_handler = AzureLogHandler(connection_string=AZURE_CONNECTION_STRING)
                azure_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
                self.logger.addHandler(azure_handler)
            
            # Always add console handler for local development
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Failed to setup Azure logging: {e}")
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
    
    def _setup_tracing(self):
        """Setup Azure Application Insights tracing"""
        try:
            if AZURE_CONNECTION_STRING:
                # Configure tracing
                config_integration.trace_integrations(['requests', 'fastapi'])
                
                # Create tracer with Azure exporter
                exporter = AzureExporter(connection_string=AZURE_CONNECTION_STRING)
                self.tracer = Tracer(
                    exporter=exporter,
                    sampler=ProbabilitySampler(1.0)  # Sample all requests in development
                )
                
        except Exception as e:
            print(f"Failed to setup Azure tracing: {e}")
    
    def log_info(self, message: str, extra: Dict[str, Any] = None):
        """Log info message with optional extra data"""
        if extra:
            self.logger.info(message, extra={"custom_dimensions": extra})
        else:
            self.logger.info(message)
    
    def log_error(self, message: str, error: Exception = None, extra: Dict[str, Any] = None):
        """Log error message with optional exception and extra data"""
        error_data = {"custom_dimensions": extra or {}}
        if error:
            error_data["custom_dimensions"]["error_type"] = type(error).__name__
            error_data["custom_dimensions"]["error_message"] = str(error)
        
        self.logger.error(message, extra=error_data, exc_info=error is not None)
    
    def log_metric(self, name: str, value: float, properties: Dict[str, str] = None):
        """Log custom metric"""
        metric_data = {
            "metric_name": name,
            "metric_value": value,
            "properties": properties or {}
        }
        self.log_info(f"METRIC: {name} = {value}", metric_data)
    
    def track_request(self, endpoint: str, method: str = "POST"):
        """Decorator to track API requests"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    # Execute the function
                    result = await func(*args, **kwargs)
                    
                    # Log successful request
                    duration = time.time() - start_time
                    self.log_info(
                        f"Request completed: {method} {endpoint}",
                        {
                            "endpoint": endpoint,
                            "method": method,
                            "duration_ms": round(duration * 1000, 2),
                            "status": "success"
                        }
                    )
                    
                    # Log performance metric
                    self.log_metric(
                        "request_duration",
                        duration * 1000,
                        {"endpoint": endpoint, "method": method}
                    )
                    
                    return result
                
                except Exception as e:
                    # Log failed request
                    duration = time.time() - start_time
                    self.log_error(
                        f"Request failed: {method} {endpoint}",
                        e,
                        {
                            "endpoint": endpoint,
                            "method": method,
                            "duration_ms": round(duration * 1000, 2),
                            "status": "error"
                        }
                    )
                    raise
            
            return wrapper
        return decorator
    
    def track_rag_performance(self, question: str, answer: str, sources_count: int, 
                            duration: float, evaluation: Dict[str, float] = None):
        """Track RAG system performance metrics"""
        
        # Log RAG request details
        self.log_info(
            "RAG request processed",
            {
                "question_length": len(question),
                "answer_length": len(answer),
                "sources_count": sources_count,
                "processing_time_ms": round(duration * 1000, 2)
            }
        )
        
        # Log performance metrics
        self.log_metric("rag_processing_time", duration * 1000)
        self.log_metric("rag_sources_retrieved", sources_count)
        
        # Log RAGAS evaluation metrics if available
        if evaluation:
            for metric_name, score in evaluation.items():
                if metric_name != "error" and isinstance(score, (int, float)):
                    self.log_metric(f"ragas_{metric_name}", score)

# Global monitor instance
monitor = AzureMonitor()

# Convenience functions
def log_info(message: str, extra: Dict[str, Any] = None):
    monitor.log_info(message, extra)

def log_error(message: str, error: Exception = None, extra: Dict[str, Any] = None):
    monitor.log_error(message, error, extra)

def log_metric(name: str, value: float, properties: Dict[str, str] = None):
    monitor.log_metric(name, value, properties)

def track_request(endpoint: str, method: str = "POST"):
    return monitor.track_request(endpoint, method)

def track_rag_performance(question: str, answer: str, sources_count: int, 
                        duration: float, evaluation: Dict[str, float] = None):
    monitor.track_rag_performance(question, answer, sources_count, duration, evaluation)
