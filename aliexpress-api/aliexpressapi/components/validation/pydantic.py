from pydantic import ValidationError


def format_pydantic_errors(error: ValidationError) -> list[dict[str, str]]:
    return [
        {
            "code": "VALIDATION_ERROR",
            "message": f"{'.'.join(map(str, item['loc']))}: {item['msg']}",
        }
        for item in error.errors()
    ]
