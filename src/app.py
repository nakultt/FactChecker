from agents.fact_checker_agent import create_fact_checker_agent


def main():
    print("🔍 Fact Checker Agent initialized!")
    print("=" * 50)
    
    agent = create_fact_checker_agent()
    
    while True:
        query = input("\n📝 Enter your query (or 'quit' to exit): ")
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query.strip():
            continue
        
        print("\n🤖 Agent is working...\n")
        
        try:
            result = agent.invoke({"input": query})
            print("\n✅ Final Answer:")
            print("=" * 50)
            print(result['output'])
            print("=" * 50)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()