from fastapi import APIRouter
import hashlib
import bcrypt as pybcrypt

router = APIRouter(prefix="/a02-crypto-failures", tags=["A02 - Cryptographic Failures"])

@router.get("/vulnerable/hash")
def crypto_vulnerable(password: str = "MyPassword123"):
    """
    VULNERABLE:
    Uses obsolete MD5 algorithm without salt to hash passwords.
    MD5 is vulnerable to rainbow table lookups and collision attacks.
    """
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    return {
        "status": "vulnerable",
        "category": "A02:2021 - Cryptographic Failures",
        "algorithm": "MD5 (Obsolete & Insecure)",
        "input": password,
        "hash_output": md5_hash
    }

@router.get("/secure/hash")
def crypto_secure(password: str = "MyPassword123"):
    """
    SECURE:
    Uses modern Bcrypt password hashing algorithm with auto-generated salt and work factor.
    """
    salt = pybcrypt.gensalt()
    hashed = pybcrypt.hashpw(password.encode('utf-8')[:72], salt)
    return {
        "status": "secure",
        "category": "A02:2021 - Cryptographic Failures",
        "algorithm": "Bcrypt (Adaptive Salt & Work Factor)",
        "input": password,
        "hash_output": hashed.decode('utf-8')
    }
