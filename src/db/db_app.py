from dataclasses import dataclass
from datetime import datetime

@dataclass
class FakeConnection:
    tx_id: str
    active: bool = True

def begin_transaction() -> FakeConnection:
    tx_id = datetime.now().strftime("%H%M%S%f")
    print(f">> BEGIN TRANSACTION (tx={tx_id})")
    return FakeConnection(tx_id=tx_id)

def commit(cn: FakeConnection) -> None:
    if cn and cn.active:
        print(f">> COMMIT (tx={cn.tx_id})")
        cn.active = False

def rollback(cn: FakeConnection) -> None:
    if cn and cn.active:
        print(f">> ROLLBACK (tx={cn.tx_id})")
        cn.active = False

def savepoint(cn: FakeConnection, name: str) -> None:
    if cn and cn.active:
        print(f">> SAVEPOINT {name} (tx={cn.tx_id})")
