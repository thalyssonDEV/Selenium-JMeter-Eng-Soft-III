import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def api_itens(request):
    # GET: Listar
    if request.method == 'GET':
        itens = list(Item.objects.values())
        return JsonResponse(itens, safe=False)
    
    # POST: Criar
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        
        # --- 1. VALIDAÇÃO DE CAMPOS OBRIGATÓRIOS ---
        nome = data.get('nome', '').strip()
        if not nome:
            return JsonResponse({'error': 'O nome do componente não pode ser vazio.'}, status=400)

        # --- 2. VALIDAÇÃO DE VALORES NUMÉRICOS (Preço e Watts) ---
        try:
            preco = float(data.get('preco', 0))
            watts = int(data.get('watts', 0))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Preço e Watts devem ser números válidos.'}, status=400)

        if preco < 0:
            return JsonResponse({'error': 'O preço não pode ser negativo.'}, status=400)
        
        if watts < 0:
            return JsonResponse({'error': 'Os Watts não podem ser negativos.'}, status=400)

        # --- 3. VALIDAÇÃO DE REGRA DE NEGÓCIO (Unicidade) ---
        categoria = data.get('categoria')
        categorias_unicas = ['Processador', 'Placa Mãe', 'Gabinete', 'Fonte']
        
        if categoria in categorias_unicas:
            if Item.objects.filter(categoria=categoria).exists():
                return JsonResponse(
                    {'error': f'O setup já possui um(a) {categoria}. Remova o anterior primeiro.'}, 
                    status=400
                )

        # --- SALVAR ---
        links_str = json.dumps(data.get('links', []))

        item = Item.objects.create(
            nome=nome, # Salva o nome já sem espaços extras
            categoria=categoria,
            preco=preco,
            watts=watts,
            comprado=data.get('comprado', False),
            links_json=links_str
        )
        return JsonResponse({'id': item.id, 'msg': 'Criado com sucesso'}, status=201)

@csrf_exempt
def api_item_detail(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Item não encontrado'}, status=404)

    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({'msg': 'Item deletado'})

    # PUT: Editar
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        # 1. Validação de Nome Vazio
        if 'nome' in data:
            novo_nome = data['nome'].strip()
            if not novo_nome:
                return JsonResponse({'error': 'O nome não pode ser vazio.'}, status=400)
            item.nome = novo_nome

        # 2. Validação de Números
        if 'preco' in data:
            try:
                novo_preco = float(data['preco'])
                if novo_preco < 0: return JsonResponse({'error': 'Preço negativo.'}, status=400)
                item.preco = novo_preco
            except ValueError:
                return JsonResponse({'error': 'Preço inválido.'}, status=400)

        if 'watts' in data:
            try:
                novo_watts = int(data['watts'])
                if novo_watts < 0: return JsonResponse({'error': 'Watts negativos.'}, status=400)
                item.watts = novo_watts
            except ValueError:
                return JsonResponse({'error': 'Watts inválidos.'}, status=400)

        # 3. Validação de Categoria Única
        if 'categoria' in data:
            nova_categoria = data['categoria']
            if nova_categoria != item.categoria:
                categorias_unicas = ['Processador', 'Placa Mãe', 'Gabinete', 'Fonte']
                if nova_categoria in categorias_unicas:
                    if Item.objects.filter(categoria=nova_categoria).exists():
                        return JsonResponse({'error': f'Já existe um(a) {nova_categoria} no setup.'}, status=400)
            item.categoria = nova_categoria

        # Atualiza outros campos simples
        if 'comprado' in data: item.comprado = data['comprado']
        if 'links' in data: item.links_json = json.dumps(data['links'])
            
        item.save()
        return JsonResponse({'msg': 'Atualizado com sucesso'})