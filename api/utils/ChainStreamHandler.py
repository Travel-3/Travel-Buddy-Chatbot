from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Any


class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        # print("Token: {}".format(token), end="\n")
        print(token, end="")
        self.tokens.append(token)

    def on_llm_end(self, response, **kwargs: Any) -> None:
        self.finish = True

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        print(str(error))
        self.tokens.append(str(error))

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                pass
