from CerebrasAI import CerebrasAI
import time

if __name__ == "__main__":
    AI = CerebrasAI()
    while True:
        query = input("You: ")
        if not query.strip():continue
        start_time = time.time()
        response = AI.ask(query)
        if response is not None:print(f"\033[1;93mCerebrasAI: {response}, Time Taken: {time.time()-start_time:.2f} Seconds.\033[0m\n")