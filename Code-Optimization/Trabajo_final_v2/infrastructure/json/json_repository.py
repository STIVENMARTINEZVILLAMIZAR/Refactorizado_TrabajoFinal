from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class JsonListRepository:
    """
    Adaptador JSON para persistir una lista de objetos (dicts).

    Mantiene compatibilidad con el baseline:
    - archivos con nombres `usuarios.json`, `herramientas.json`, etc.
    - estructura como lista de dicts con clave `id`
    """

    data_dir: Path
    filename: str
    id_key: str = "id"

    def _path(self) -> Path:
        return self.data_dir / self.filename

    def load_all(self) -> List[Dict[str, Any]]:
        path = self._path()
        if not path.exists():
            return []
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return list(data) if data else []
        except json.JSONDecodeError:
            return []

    def save_all(self, entities: List[Dict[str, Any]]) -> None:
        self._path().parent.mkdir(parents=True, exist_ok=True)
        with self._path().open("w", encoding="utf-8") as f:
            json.dump(entities, f, indent=4, ensure_ascii=False)

    def next_id(self, entities: List[Dict[str, Any]]) -> int:
        current = []
        for e in entities:
            if self.id_key in e:
                try:
                    current.append(int(e[self.id_key]))
                except Exception:
                    continue
        return (max(current) + 1) if current else 1

    def list_all(self) -> List[Dict[str, Any]]:
        return self.load_all()

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        for e in self.load_all():
            if e.get(self.id_key) == entity_id:
                return e
        return None

    def add(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        entities = self.load_all()
        entity = dict(entity)
        entity[self.id_key] = self.next_id(entities)
        entities.append(entity)
        self.save_all(entities)
        return entity

    def update(self, entity: Dict[str, Any]) -> None:
        entities = self.load_all()
        entity_id = int(entity.get(self.id_key))
        updated = False
        for i, e in enumerate(entities):
            if e.get(self.id_key) == entity_id:
                entities[i] = dict(entity)
                updated = True
                break
        if updated:
            self.save_all(entities)

    def delete_by_id(self, entity_id: int) -> None:
        entities = self.load_all()
        entities = [e for e in entities if e.get(self.id_key) != entity_id]
        self.save_all(entities)

