FROM langchain/langgraph-api:3.11



# -- Adding local package . --
ADD . /deps/react-agent-python
# -- End of local package . --

# -- Installing all local dependencies --
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*
# -- End of local dependencies install --
ENV LANGSERVE_GRAPHS='{"agent": "/deps/react-agent-python/src/react_agent/graph.py:make_graph"}'

WORKDIR /deps/react-agent-python