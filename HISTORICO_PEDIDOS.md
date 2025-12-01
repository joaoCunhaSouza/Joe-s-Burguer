# Sistema de Histórico de Pedidos

## Funcionalidades Implementadas

### 1. Histórico Automático
- Quando a cozinha finaliza um pedido (status = DONE), ele é automaticamente adicionado ao histórico do usuário
- Os pedidos são armazenados com todas as informações: itens, customizações, valores e data

### 2. Filtros de Período
O usuário pode filtrar o histórico por:
- **Últimos 7 dias**: Mostra pedidos da última semana
- **Últimos 30 dias**: Mostra pedidos do último mês
- **Últimos 90 dias**: Mostra todos os pedidos disponíveis

### 3. Limpeza Automática
- Pedidos com mais de 90 dias são automaticamente removidos do histórico
- A limpeza ocorre automaticamente quando o usuário acessa a página de histórico
- Também pode ser executada manualmente via comando de gerenciamento

### 4. Visualização
- **Lista de Pedidos**: Mostra resumo com data, valor total e itens
- **Detalhes do Pedido**: Ao clicar, mostra todos os itens, customizações e valores detalhados

## URLs

- `/historico/` - Lista de pedidos do histórico
- `/historico/<id>/` - Detalhes de um pedido específico

## Navegação

O histórico pode ser acessado de duas formas:
1. Pelo ícone de histórico (relógio) na barra inferior de navegação
2. Pelo menu do usuário (clique no avatar) > "Histórico de Pedidos"

## Comandos de Gerenciamento

### Limpar pedidos antigos manualmente

```bash
# Remove pedidos com mais de 90 dias
python manage.py cleanup_old_orders

# Remove pedidos com mais de X dias
python manage.py cleanup_old_orders --days 60

# Modo dry-run (apenas mostra quantos seriam deletados)
python manage.py cleanup_old_orders --dry-run
```

## Estrutura de Dados

### Modelo OrderHistory
- `user`: Usuário dono do pedido
- `order_data`: JSON com todos os dados do pedido (itens, customizações, etc)
- `total`: Valor total do pedido
- `order_date`: Data em que o pedido foi criado
- `created_at`: Data em que foi adicionado ao histórico

### Formato do order_data (JSON)
```json
[
  {
    "name": "Combo X-Burguer",
    "quantity": 2,
    "unit_price": 25.00,
    "total_price": 50.00,
    "customization": {
      "1": 2,  // ID do subproduto: quantidade
      "3": 0   // quantidade 0 = removido
    }
  }
]
```

## Fluxo de Funcionamento

1. **Cliente faz um pedido** → Pedido criado com status "new"
2. **Cozinha aceita** → Status muda para "preparing"
3. **Cozinha finaliza** → Status muda para "done"
4. **Sistema detecta mudança** → Adiciona automaticamente ao histórico do usuário
5. **Cliente acessa histórico** → Vê todos os pedidos finalizados
6. **Sistema limpa automaticamente** → Remove pedidos com mais de 90 dias

## Agendamento de Limpeza (Opcional)

Para automatizar a limpeza em produção, você pode:

### Opção 1: Cron Job (Linux/Mac)
```bash
# Editar crontab
crontab -e

# Adicionar linha para executar diariamente às 3h da manhã
0 3 * * * cd /caminho/do/projeto && /caminho/do/venv/bin/python manage.py cleanup_old_orders
```

### Opção 2: Task Scheduler (Windows)
- Criar uma tarefa agendada que execute o comando diariamente

### Opção 3: Django-Cron ou Celery
- Instalar django-cron ou Celery para agendamento mais robusto

## Observações Importantes

1. **Privacidade**: Cada usuário só vê seus próprios pedidos
2. **Performance**: A consulta ao histórico é otimizada com índices de data
3. **Armazenamento**: Pedidos antigos são removidos para economizar espaço
4. **Integridade**: Os dados são armazenados como JSON para preservar informações mesmo se produtos/subprodutos forem deletados

## Próximos Passos (Melhorias Futuras)

- [ ] Permitir download do histórico em PDF
- [ ] Adicionar busca por nome de produto
- [ ] Estatísticas de pedidos (produto mais pedido, valor médio, etc)
- [ ] Opção de "pedir novamente" (adicionar ao carrinho os mesmos itens)
- [ ] Notificação quando pedido for finalizado
