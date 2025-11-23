from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer(auto_error=False)
SecurityDep = Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)]
