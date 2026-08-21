"""Code Environment Actor"""

import os
import time
import gc
import httpx
import openai
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

    async def _llm_chat(
        self, prompt, model, base_url, timeout, temperature, current_api_key, seed=None
    ):
        """Call LLM API with specified API key and optional seed"""
        # Unset SSL_CERT_FILE to avoid certificate path issues in container
        # Let httpx/certifi use default certificate bundle
        os.environ.pop("SSL_CERT_FILE", None)
        os.environ.pop("REQUESTS_CA_BUNDLE", None)

        client = openai.AsyncOpenAI(
            base_url=base_url.rstrip("/"),
            api_key=current_api_key,
            timeout=httpx.Timeout(timeout),
            max_retries=0,
        )

        # Prepare API call parameters
        params = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": False,
        }

        # Add seed if provided
        if seed is not None:
            params["seed"] = seed

        response = await client.chat.completions.create(**params)

        # Handle case where API returns None content
        if not response.choices:
            raise ValueError("LLM API returned empty choices list")

        content = response.choices[0].message.content
        if content is None:
            raise ValueError(
                "LLM API returned None content (possible content filtering or API error)"
            )

        return content.strip()

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
    ):

        if seed is None:
            seed = random.randint(0, 2**32 - 1)

        # Allow per-call api_key override
        current_api_key = api_key or self.api_key

        start = time.time()

        # Generate challenge
        challenge = await self.code_task.generate(task_id=task_id)

        # Add model and base_url info to challenge.extra for logging
        challenge.extra["model"] = model
        challenge.extra["base_url"] = base_url

        # Call LLM
        # try:
        #     resp = await self._llm_chat(
        #         challenge.prompt,
        #         model,
        #         base_url,
        #         timeout,
        #         temperature,
        #         current_api_key,
        #         seed,
        #     )
        #     error = None
        # except Exception as e:
        #     import traceback

        #     resp = None
        #     error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

        resp = answer

        # Evaluate
        score = 0.0
        test_result = "0/0"
        if resp:
            score, test_result = await self.code_task.evaluate(resp, challenge)

        conversation = [
            {"role": "user", "content": challenge.prompt},
            {"role": "assistant", "content": resp},
        ]

        # print("=" * 100)
        # print(challenge.prompt)
        # print("-" * 20)
        # print(resp)
        # print("-" * 20)
        # print(score)
        # print("=" * 100)

        result = {
            "task_name": "CDE",
            "score": score,
        }

        import json
        # print("-------prompt")
        # print(challenge.prompt)
        # print(challenge.extra["tests"])
        # if score == 1:
        #     save_data = {"question": challenge.prompt, "answer": resp}
        #     with open(f"dataset/{task_id}.json", "w") as f:
        #         json.dump(save_data, f)
        #     with open(f"search_dataset/{task_id}.json", "w") as f:
        #         json.dump(resp, f)

        # Add error info if present
        # if error:
        #     result["error"] = error
        #     result["error_type"] = "llm_failure"

        # Force garbage collection to free memory immediately
        gc.collect()

        return result


async def main():
    actor = Actor()
    import json

    list_miss = []

    save_list_miss_file_name = "list_miss-3000-4000.json"

    with open(save_list_miss_file_name, "r") as f:
        save_data = json.load(f)

    print(save_data)
    list_miss = save_data
    # save_data = [2999]

    # for i in range(100 , 200):
    for i in range(save_data[-1] + 1 , 4000):
        with open(f"search_dataset_v1/{i}.json", "r") as f:
            try:
                answer = json.load(f)
                result = await actor.evaluate(answer=answer, task_id=i)
                score = result["score"]
            except Exception as e:
                print(f"id : {i} json format error")
                list_miss.append(i)
                score = 0
                continue

        if score == 0:
            print(f"id : {i} score is zero")
            list_miss.append(i)
            with open(save_list_miss_file_name, "w", encoding="utf-8") as f:
                json.dump(list_miss, f, indent=2)
        else:
            print(f"id : {i} score: {score}")
    print(list_miss)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
