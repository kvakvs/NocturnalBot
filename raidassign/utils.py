def safe_cast(value: any, target_type: type, default: any = None) -> any:  # type: ignore
    try:
        return target_type(value) if value is not None else default
    except (ValueError, TypeError):
        return default
