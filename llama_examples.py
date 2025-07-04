"""
Advanced Llama Usage Examples
Demonstrates various use cases for Llama 3.1/3.2 models
"""

from llama_api import LlamaAPI
import json
import time
from typing import List, Dict

class LlamaExamples:
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.api = LlamaAPI()
        self.model = model_name
        
    def code_generation(self, task: str, language: str = "python") -> str:
        """Generate code using Llama"""
        prompt = f"""
        Generate {language} code for the following task:
        {task}
        
        Provide clean, well-commented code with proper error handling.
        Only return the code, no explanations.
        """
        
        response = self.api.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.1}  # Lower temperature for more consistent code
        )
        
        return response['response']
    
    def text_analysis(self, text: str) -> Dict:
        """Analyze text for sentiment, topics, and summary"""
        prompt = f"""
        Analyze the following text and provide:
        1. Sentiment (positive/negative/neutral)
        2. Main topics (3-5 keywords)
        3. Brief summary (1-2 sentences)
        4. Key insights
        
        Text: {text}
        
        Respond in JSON format.
        """
        
        response = self.api.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.3}
        )
        
        try:
            return json.loads(response['response'])
        except json.JSONDecodeError:
            return {"error": "Could not parse JSON response", "raw": response['response']}
    
    def creative_writing(self, genre: str, prompt: str, length: str = "short") -> str:
        """Generate creative content"""
        system_prompt = f"""
        You are a creative writer specializing in {genre}. 
        Write a {length} {genre} story based on the following prompt.
        Focus on engaging narrative, character development, and vivid descriptions.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = self.api.chat(
            model=self.model,
            messages=messages,
            options={"temperature": 0.8}  # Higher temperature for creativity
        )
        
        return response['message']['content']
    
    def data_extraction(self, text: str, fields: List[str]) -> Dict:
        """Extract structured data from unstructured text"""
        fields_str = ", ".join(fields)
        
        prompt = f"""
        Extract the following information from the text: {fields_str}
        
        Text: {text}
        
        Return the information in JSON format with the specified fields as keys.
        If information is not found, use null for that field.
        """
        
        response = self.api.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.1}
        )
        
        try:
            return json.loads(response['response'])
        except json.JSONDecodeError:
            return {"error": "Could not parse response", "raw": response['response']}
    
    def question_answering(self, context: str, question: str) -> str:
        """Answer questions based on provided context"""
        prompt = f"""
        Context: {context}
        
        Question: {question}
        
        Answer the question based only on the provided context. 
        If the answer cannot be found in the context, say "I cannot answer based on the provided context."
        """
        
        response = self.api.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.2}
        )
        
        return response['response']
    
    def language_translation(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        prompt = f"""
        Translate the following text to {target_language}:
        
        {text}
        
        Provide only the translation, no explanations.
        """
        
        response = self.api.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": 0.1}
        )
        
        return response['response']
    
    def conversation_assistant(self):
        """Interactive conversation assistant"""
        print(f"🤖 Llama Assistant ({self.model}) - Type 'quit' to exit")
        print("=" * 50)
        
        conversation_history = [
            {"role": "system", "content": "You are a helpful AI assistant. Be concise but informative."}
        ]
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Assistant: Goodbye! 👋")
                break
            
            if user_input.lower() == 'clear':
                conversation_history = [conversation_history[0]]  # Keep system message
                print("Assistant: Conversation history cleared.")
                continue
            
            conversation_history.append({"role": "user", "content": user_input})
            
            print("Assistant: ", end="", flush=True)
            
            # Stream the response
            full_response = ""
            for chunk in self.api.chat(
                model=self.model,
                messages=conversation_history,
                stream=True,
                options={"temperature": 0.7}
            ):
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    print(content, end="", flush=True)
                    full_response += content
                
                if chunk.get('done'):
                    break
            
            print()  # New line after response
            
            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": full_response})

def run_examples():
    """Run example demonstrations"""
    print("🦙 Llama 3.1/3.2 Examples")
    print("=" * 40)
    
    # Check if models are available
    api = LlamaAPI()
    try:
        models = api.list_models()
        if not models:
            print("❌ No models found. Please install a model first using llama_setup.py")
            return
        
        # Use the first available model
        model_name = models[0]['name']
        print(f"Using model: {model_name}\n")
        
        examples = LlamaExamples(model_name)
        
        while True:
            print("\nChoose an example:")
            print("1. Code Generation")
            print("2. Text Analysis")
            print("3. Creative Writing")
            print("4. Data Extraction")
            print("5. Question Answering")
            print("6. Language Translation")
            print("7. Interactive Chat")
            print("8. Exit")
            
            choice = input("\nEnter choice (1-8): ").strip()
            
            if choice == '1':
                task = input("Describe the coding task: ")
                language = input("Programming language (default: python): ") or "python"
                print("\nGenerated code:")
                print("=" * 30)
                print(examples.code_generation(task, language))
                
            elif choice == '2':
                text = input("Enter text to analyze: ")
                print("\nAnalysis:")
                print("=" * 20)
                analysis = examples.text_analysis(text)
                print(json.dumps(analysis, indent=2))
                
            elif choice == '3':
                genre = input("Enter genre (e.g., sci-fi, mystery, romance): ")
                prompt = input("Enter story prompt: ")
                print("\nGenerated story:")
                print("=" * 30)
                print(examples.creative_writing(genre, prompt))
                
            elif choice == '4':
                text = input("Enter text to extract data from: ")
                fields = input("Enter fields to extract (comma-separated): ").split(',')
                fields = [f.strip() for f in fields]
                print("\nExtracted data:")
                print("=" * 30)
                data = examples.data_extraction(text, fields)
                print(json.dumps(data, indent=2))
                
            elif choice == '5':
                context = input("Enter context: ")
                question = input("Enter question: ")
                print("\nAnswer:")
                print("=" * 20)
                print(examples.question_answering(context, question))
                
            elif choice == '6':
                text = input("Enter text to translate: ")
                target = input("Target language: ")
                print("\nTranslation:")
                print("=" * 20)
                print(examples.language_translation(text, target))
                
            elif choice == '7':
                examples.conversation_assistant()
                
            elif choice == '8':
                print("Goodbye! 👋")
                break
                
            else:
                print("Invalid choice. Please try again.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Ollama is running with: ollama serve")

if __name__ == "__main__":
    run_examples()
