"""
LLM Configuration Manager

Provides flexible LLM configuration supporting multiple providers and
role-optimized model selection for different agent types.
"""

import os
from typing import Dict, Any, Optional, Union
import structlog

from langchain_community.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class LLMConfig(BaseModel):
    """Configuration for a specific LLM."""
    provider: str = Field(..., description="LLM provider (openai, anthropic, azure, local)")
    model: str = Field(..., description="Model name")
    temperature: float = Field(default=0.1, description="Temperature setting")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens")
    api_key: Optional[str] = Field(default=None, description="API key")
    base_url: Optional[str] = Field(default=None, description="Base URL for API")


class LLMConfigManager:
    """
    Manages LLM configurations for different providers and agent roles.
    
    This class provides flexible LLM configuration supporting multiple providers
    (OpenAI, Anthropic, Azure, local models) with role-optimized model selection
    for different types of agents in the competitive analysis crew.
    """
    
    def __init__(self):
        """Initialize the LLM configuration manager."""
        self.providers = {
            'openai': self._configure_openai,
            'anthropic': self._configure_anthropic,
            'azure': self._configure_azure,
            'local': self._configure_local
        }
        
        # Role-optimized model configurations
        self.role_configs = {
            'manager': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.1,
                'description': 'High-capability model for crew management and coordination'
            },
            'research': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.2,
                'description': 'Balanced model for research and analysis tasks'
            },
            'writing': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.3,
                'description': 'Language-optimized model for content generation'
            },
            'editing': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.1,
                'description': 'Detail-focused model for quality assurance'
            },
            'translation': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.2,
                'description': 'Multilingual model for translation tasks'
            },
            'onboarding': {
                'provider': 'openai',
                'model': 'gpt-4o-mini',
                'temperature': 0.1,
                'description': 'Efficient model for user interaction and data collection'
            },
            'management': {
                'provider': 'openai',
                'model': 'gpt-4o',
                'temperature': 0.1,
                'description': 'Management-focused model for quality assurance and coordination'
            }
        }
        
        logger.info("LLM Configuration Manager initialized", 
                   providers=list(self.providers.keys()),
                   roles=list(self.role_configs.keys()))
    
    def get_llm(self, provider: str, model: str, role: str = "general") -> Any:
        """
        Get a configured LLM instance for a specific provider, model, and role.
        
        Args:
            provider: LLM provider name (openai, anthropic, azure, local)
            model: Model name
            role: Agent role for optimized configuration
            
        Returns:
            Configured LLM instance
        """
        try:
            # Get role-specific configuration if available
            role_config = self.role_configs.get(role, {})
            
            # Override with role-specific settings if available
            if role_config:
                provider = role_config.get('provider', provider)
                model = role_config.get('model', model)
                temperature = role_config.get('temperature', 0.1)
            else:
                temperature = 0.1
            
            # Get provider configuration function
            config_func = self.providers.get(provider)
            if not config_func:
                logger.warning(f"Unknown provider {provider}, falling back to OpenAI")
                config_func = self._configure_openai
                provider = 'openai'
                model = 'gpt-4o-mini'
            
            # Configure and return LLM
            llm = config_func(model, temperature, role)
            
            logger.info("LLM configured", 
                       provider=provider, 
                       model=model, 
                       role=role,
                       temperature=temperature)
            
            return llm
            
        except Exception as e:
            logger.error("Error configuring LLM", 
                        provider=provider, 
                        model=model, 
                        role=role, 
                        error=str(e))
            
            # Fallback to basic OpenAI configuration
            return self._configure_openai('gpt-4o-mini', 0.1, role)
    
    def _configure_openai(self, model: str, temperature: float, role: str) -> ChatOpenAI:
        """
        Configure OpenAI LLM.
        
        Args:
            model: OpenAI model name
            temperature: Temperature setting
            role: Agent role
            
        Returns:
            Configured ChatOpenAI instance
        """
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        # Model validation and fallback
        valid_models = [
            'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4', 
            'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'
        ]
        
        if model not in valid_models:
            logger.warning(f"Model {model} not in validated list, using gpt-4o-mini")
            model = 'gpt-4o-mini'
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=None,  # Let the model decide
            model_kwargs={
                'frequency_penalty': 0.1,
                'presence_penalty': 0.1
            }
        )
    
    def _configure_anthropic(self, model: str, temperature: float, role: str) -> Any:
        """
        Configure Anthropic LLM.
        
        Args:
            model: Anthropic model name
            temperature: Temperature setting
            role: Agent role
            
        Returns:
            Configured Anthropic LLM instance
        """
        try:
            from langchain_anthropic import ChatAnthropic
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                logger.warning("ANTHROPIC_API_KEY not found, falling back to OpenAI")
                return self._configure_openai('gpt-4o-mini', temperature, role)
            
            # Model validation and fallback
            valid_models = [
                'claude-3-5-sonnet-20241022', 'claude-3-opus-20240229', 
                'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'
            ]
            
            if model not in valid_models:
                logger.warning(f"Model {model} not in validated list, using claude-3-5-sonnet")
                model = 'claude-3-5-sonnet-20241022'
            
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                api_key=api_key,
                max_tokens=4096
            )
            
        except ImportError:
            logger.warning("langchain_anthropic not available, falling back to OpenAI")
            return self._configure_openai('gpt-4o-mini', temperature, role)
    
    def _configure_azure(self, model: str, temperature: float, role: str) -> Any:
        """
        Configure Azure OpenAI LLM.
        
        Args:
            model: Azure OpenAI model name
            temperature: Temperature setting
            role: Agent role
            
        Returns:
            Configured Azure OpenAI LLM instance
        """
        try:
            from langchain_openai import AzureChatOpenAI
            
            api_key = os.getenv('AZURE_OPENAI_API_KEY')
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
            
            if not api_key or not endpoint:
                logger.warning("Azure OpenAI credentials not found, falling back to OpenAI")
                return self._configure_openai('gpt-4o-mini', temperature, role)
            
            return AzureChatOpenAI(
                azure_deployment=model,
                api_version=api_version,
                temperature=temperature,
                api_key=api_key,
                azure_endpoint=endpoint
            )
            
        except ImportError:
            logger.warning("Azure OpenAI not available, falling back to OpenAI")
            return self._configure_openai('gpt-4o-mini', temperature, role)
    
    def _configure_local(self, model: str, temperature: float, role: str) -> Any:
        """
        Configure local LLM (e.g., Ollama).
        
        Args:
            model: Local model name
            temperature: Temperature setting
            role: Agent role
            
        Returns:
            Configured local LLM instance
        """
        try:
            from langchain_community.llms import Ollama
            
            base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            
            return Ollama(
                model=model,
                temperature=temperature,
                base_url=base_url
            )
            
        except ImportError:
            logger.warning("Ollama not available, falling back to OpenAI")
            return self._configure_openai('gpt-4o-mini', temperature, role)
    
    def get_role_config(self, role: str) -> Dict[str, Any]:
        """
        Get configuration for a specific role.
        
        Args:
            role: Agent role name
            
        Returns:
            Dict containing role configuration
        """
        return self.role_configs.get(role, {
            'provider': 'openai',
            'model': 'gpt-4o-mini',
            'temperature': 0.1,
            'description': 'Default configuration'
        })
    
    def list_available_roles(self) -> Dict[str, str]:
        """
        List all available role configurations.
        
        Returns:
            Dict mapping role names to descriptions
        """
        return {
            role: config.get('description', 'No description available')
            for role, config in self.role_configs.items()
        }
    
    def update_role_config(self, role: str, config: Dict[str, Any]) -> None:
        """
        Update configuration for a specific role.
        
        Args:
            role: Role name to update
            config: New configuration dictionary
        """
        if role in self.role_configs:
            self.role_configs[role].update(config)
            logger.info(f"Updated configuration for role: {role}")
        else:
            self.role_configs[role] = config
            logger.info(f"Created new configuration for role: {role}")
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate current LLM configuration.
        
        Returns:
            Dict containing validation results
        """
        validation_results = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        # Check for required environment variables
        required_vars = {
            'openai': ['OPENAI_API_KEY'],
            'anthropic': ['ANTHROPIC_API_KEY'],
            'azure': ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT']
        }
        
        for provider, vars_list in required_vars.items():
            missing_vars = [var for var in vars_list if not os.getenv(var)]
            if missing_vars:
                validation_results['warnings'].append(
                    f"Missing environment variables for {provider}: {missing_vars}"
                )
        
        # Check role configurations
        for role, config in self.role_configs.items():
            if 'provider' not in config or 'model' not in config:
                validation_results['issues'].append(
                    f"Incomplete configuration for role {role}"
                )
                validation_results['valid'] = False
        
        return validation_results