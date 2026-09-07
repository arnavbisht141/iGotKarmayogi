# Existing AI assistant

This package contains the original in-process LangGraph assistant and remains
unchanged during the repository reorganization. It continues to expose the existing
`/api/agents/chat` route through the LMS backend.

The future extraction boundary is documented in [`../../../ai-service/README.md`](../../../ai-service/README.md).
Do not partially split this package across processes without an explicit API,
authorization, failure-handling, and data-ownership design.
