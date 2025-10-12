from my_library_database.common import get_connection
from my_library_genai.common import get_llm

def main():
    print("Hello from my-application!")
    print(f"Database connection: {get_connection()}")
    print(f"LLM: {get_llm()}")


if __name__ == "__main__":
    main()
