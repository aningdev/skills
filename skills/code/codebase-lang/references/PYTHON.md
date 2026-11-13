# Python

- **Modern typing.** `X | None`, built-in generics (`list[T]`, `dict[K, V]`), `type` aliases. Use `object` for a value that must be narrowed before use, not `Any`. Every `# type: ignore` names the error code and says why.
- **Data.** `dataclass` for field-shaped data, or Pydantic v2 if the project already uses it. `Enum` or `Literal` for finite values. Never a mutable default argument: use `None` or `default_factory`.
- **Idioms.** `pathlib.Path` for paths. `zip(..., strict=True)` when unequal lengths are a bug. Context managers for every resource.
- **Errors.** `raise ... from err` when converting. No bare `except:`.
- **Async.** Blocking calls go through `asyncio.to_thread()` or the project's executor. Use `asyncio.TaskGroup` for tasks that live and fail together. After catching cancellation, clean up and re-raise.
- **Security.** `subprocess` with an argument list, never `shell=True`. `secrets` for tokens, never `random`. No `pickle` on untrusted data.
