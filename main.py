from utils import check_ollama_installation, install_ollama, start_ollama_server, check_model_availability, pull_model

def main():
    # Check if Ollama is installed
    print("Checking Ollama installation...")
    if not check_ollama_installation():
        print("Ollama is not installed or not running. Attempting to install...")
        if not install_ollama():
            print("Failed to install Ollama. Please install it manually.")
            return
        
        print("Starting Ollama server...")
        if not start_ollama_server():
            print("Failed to start Ollama server. Please start it manually.")
            return
    
    # Define the model you want to use
    model_name = "llama3.2:3b"  
    
    # Check if the model is available locally
    print(f"Checking if {model_name} is available...")
    if not check_model_availability(model_name):
        print(f"{model_name} not found locally. Pulling the model...")
        if not pull_model(model_name):
            print(f"Failed to pull {model_name}. Please check your internet connection and try again.")
            return
        print(f"{model_name} pulled successfully!")
    else:
        print(f"{model_name} is already available locally.")
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    main()