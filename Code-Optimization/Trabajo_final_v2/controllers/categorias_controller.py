from __future__ import annotations

from typing import List, Optional

from application.gestion_categorias import GestionCategorias
from domain.dtos import ActualizarCategoriaDTO, CrearCategoriaDTO
from domain.entities import Categoria


class CategoriasController:
    def __init__(self, service: GestionCategorias) -> None:
        self._service = service

    def crear_categoria(self, dto: CrearCategoriaDTO) -> Categoria:
        return self._service.crear(dto)

    def listar_categorias(self) -> List[Categoria]:
        return self._service.listar()

    def obtener_categoria(self, categoria_id: int) -> Optional[Categoria]:
        return self._service.get_por_id(categoria_id)

    def actualizar_categoria(self, dto: ActualizarCategoriaDTO) -> Optional[Categoria]:
        return self._service.actualizar(dto)

    def eliminar_categoria(self, categoria_id: int) -> bool:
        return self._service.eliminar(categoria_id)

