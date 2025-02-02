import platform
import subprocess
import requests
import os
import sys

def check_ollama_installation():
    """Check if Ollama is installed and running"""
    try:
        # Try to make a request to Ollama API
        response = requests.get('http://localhost:11434/api/tags')
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def install_ollama():
    """Install Ollama based on the operating system"""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        try:
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            print("Ollama installed successfully via Homebrew")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install Ollama via Homebrew")
            return False
            
    elif system == "linux":
        try:
            # Install Ollama using curl
            subprocess.run([
                'curl', '-fsSL', 
                'https://ollama.com/install.sh', 
                '|', 'sh'
            ], check=True, shell=True)
            print("Ollama installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install Ollama")
            return False
            
    elif system == "windows":
        print("Please download and install Ollama from: https://ollama.com/download")
        return False
    
    return False

def start_ollama_server():
    """Start the Ollama server"""
    try:
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"Failed to start Ollama server: {e}")
        return False

def check_model_availability(model_name):
    """Check if a model is available locally"""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json().get('models', [])
            return any(model.get('name') == model_name for model in models)
    except requests.exceptions.RequestException:
        return False
    return False

def pull_model(model_name):
    """Pull a model from Ollama"""
    try:
        subprocess.run(['ollama', 'pull', model_name], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to pull model: {model_name}")
        return False