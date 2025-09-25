import pytest

from infrastructure.repositories.productorepository import ProductoRepository


def test_bodegas_db():
    repo = ProductoRepository()
    bodegas = repo.get_bodegas_permitidas()

    assert isinstance(bodegas, set), "El resultado debe ser un conjunto"
    assert len(bodegas) > 0, "El conjunto de bodegas no debe estar vacío"

    print(f"Bodegas permitidas desde la BD: {bodegas}")
