"""Code Environment Actor"""

import os
import gc
import sys
import random

# Add /app to path to import local modules
if "/app" not in sys.path:
    sys.path.insert(0, "/app")

from code_task import CodeTask


class Actor:
    """Code task evaluation actor"""

    def __init__(
        self,
        api_key: str = None,
    ):
        """
        Initialize Actor with API key

        Args:
            api_key: API key for LLM service. If not provided, will use CHUTES_API_KEY env var
        """
        self.api_key = api_key or os.getenv("CHUTES_API_KEY")

        # Initialize code task instance
        self.code_task = CodeTask()

    async def evaluate(
        self,
        answer="",
        model="deepseek-ai/DeepSeek-V3",
        base_url="https://llm.chutes.ai/v1",
        timeout=600,
        temperature=0.7,
        api_key: str = None,
        seed: int = None,
        task_id: int = None,
        generate_flag=False,
    ):

        if seed is None:
            seed = random.randint(0, 2**32 - 1)

        challenge = await self.code_task.generate(task_id=task_id)

        challenge.extra["model"] = model
        challenge.extra["base_url"] = base_url

        score_search = 0.0
        score_generate = 0.0
        score_search, test_result = await self.code_task.evaluate(answer, challenge)

        import json

        if score_search == 1:
            save_data = {"question": challenge.prompt, "answer": answer}
            with open(f"dataset/{task_id}.json", "w") as f:
                json.dump(save_data, f)
            with open(f"solve_dataset/{task_id}.json", "w") as f:
                json.dump(answer, f)
        else:
            if generate_flag:
                test_case = json.loads(challenge.extra["tests"])
                dic_solve = {}
                for input, output in zip(test_case["inputs"], test_case["outputs"]):
                    dic_solve[json.loads(input)] = json.loads(output)

                code = f"""
```python
import sys
data = sys.stdin.read()
dic_solve = {json.dumps(dic_solve)}
answer = dic_solve[data]
print(answer)
```
    """
                score_generate, test_result = await self.code_task.evaluate(
                    code, challenge
                )

                if score_generate:
                    with open(f"solve_dataset/{task_id}.json", "w") as f:
                        json.dump(code, f)

        if score_search == 0:
            print("-------prompt----------")
            print(challenge.prompt)
            print(challenge.extra["tests"])

        print("Task id:", task_id, " try to search Score:", score_search)
        if score_search != 1 and generate_flag:
            print("Task id:", task_id, " try to generate Score:", score_generate)

        gc.collect()

        result = {
            "task_name": "CDE",
            "score_search": score_search,
            "score_generate": score_generate,
        }

        return result


async def main():
    actor = Actor()
    import json

    fail_search_list = []
    fail_generate_list = []
    # for i in range(100 , 200):
    solve_list = [4912]
    generate_flag = False
    for i in solve_list:

        ##
        with open(f"search_dataset_v1/{i}.json", "r") as f:
            real_answer = json.load(f)

        real_answer = """
```python
import sys


MOD = 10**9 + 7


while 1:
    s = sys.stdin.readline().strip()
    if s == "#" or not s:
        break

    n = len(s)
    dp = [[0 for _ in range(10)] for _ in range(n + 1)]
    dp[0][1] = 1
    for i in range(1, n):

        cnt = 3 if s[i] in "80" else 5
        prevCnt = 3 if s[i - 1] in "80" else 5

        if s[i] == s[i - 1]:
            for j in range(2, cnt + 1):
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % MOD

            for j in range(1, cnt + 1):
                dp[i][1] = (dp[i][1] + dp[i - 1][j]) % MOD

        else:
            for j in range(1, prevCnt + 1):
                dp[i][1] = (dp[i][1] + dp[i - 1][j]) % MOD

    ans = 0
    for j in range(1, 6):
        ans = (ans + dp[n - 1][j]) % MOD

    print(ans)

```
        """

        result = await actor.evaluate(
            answer=real_answer, task_id=i, generate_flag=generate_flag
        )

        if result["score_search"] == 0:
            fail_search_list.append(i)
        if result["score_generate"] == 0:
            fail_generate_list.append(i)
    print("\nFail search : ", len(fail_search_list))
    print(fail_search_list)
    if generate_flag:
        print("\nFail_generate: ", len(fail_generate_list))
        print(fail_generate_list)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
