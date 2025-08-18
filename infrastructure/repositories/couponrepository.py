from django.utils import timezone
from django.db import transaction
from infrastructure.models.couponsdb import CouponsDB
from infrastructure.models.cuponUser import CouponUsageDB
from infrastructure.models.socionegociodb import SocioNegocioDB

class CouponRepository:

    @staticmethod
    @transaction.atomic
    def mark_coupon_as_used(coupon_code: str, user_code: str):
        """
        Marca el cupón como usado por el usuario.
        Si no existe un registro previo, lo crea.
        """
        try:
            coupon = CouponsDB.objects.get(cupon_code=coupon_code)
            user = SocioNegocioDB.objects.get(codigoSN=user_code)


            usage = CouponUsageDB.objects.create(
                coupon=coupon,
                user=user,
                used=True,
                used_at=timezone.now(),
                remaining_uses=0
            )

            return usage

        except CouponsDB.DoesNotExist:
            raise ValueError(f"El cupón con código {coupon_code} no existe")
        except SocioNegocioDB.DoesNotExist:
            raise ValueError(f"El usuario con código {user_code} no existe")

    @staticmethod
    def count_coupon_uses(coupon_code: str, user_code: str) -> int:
        """
        Retorna el número de veces que un usuario ha usado un cupón.
        """

        print(f"Contando usos del cupón {coupon_code} para el usuario {user_code}")
        return CouponUsageDB.objects.filter(
            coupon__cupon_code=coupon_code,
            user__codigoSN=user_code,
            used=True
        ).count()