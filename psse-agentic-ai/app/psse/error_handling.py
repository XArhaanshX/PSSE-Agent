def validate_ierr(ierr: int, operation_name: str, parameters: dict):
    """
    Validates the return code (ierr) from a PSSE operation.
    Fails loudly and aborts execution if ierr != 0.
    """
    if ierr != 0:
        error_msg = (
            f"\nPSSE operation failed\n\n"
            f"operation:\n{operation_name}\n\n"
            f"parameters:\n"
        )
        for k, v in parameters.items():
            error_msg += f"{k}={v}\n"
        
        error_msg += f"\nreturn_code:\n{ierr}\n"
        
        print(error_msg)
        raise Exception(f"PSSE operation '{operation_name}' failed with return code {ierr}")
