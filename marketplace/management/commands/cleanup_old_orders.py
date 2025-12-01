from django.core.management.base import BaseCommand
from marketplace.models import OrderHistory
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Remove pedidos do histórico com mais de 90 dias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Número de dias para considerar um pedido como antigo (padrão: 90)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Apenas mostra quantos pedidos seriam deletados sem deletar'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        old_orders = OrderHistory.objects.filter(order_date__lt=cutoff_date)
        count = old_orders.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY RUN] Seriam deletados {count} pedidos com mais de {days} dias.'
                )
            )
            return
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Nenhum pedido com mais de {days} dias encontrado.'
                )
            )
            return
        
        # Deleta os pedidos antigos
        deleted_count, _ = old_orders.delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ {deleted_count} pedidos com mais de {days} dias foram removidos com sucesso!'
            )
        )
