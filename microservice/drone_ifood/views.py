import json
from .models import *
from django.db.models import Q
from datetime import datetime
from django.db.transaction import atomic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    response = {'response': 'OK'}

    return JsonResponse(response)

@csrf_exempt
def insert(request):
    body_info = request.body.decode()

    if len(body_info) > 0:
        data = json.loads(body_info)
        data_insert_list = []
        error_list = []
        confirm_list = []

        if 'cliente' in data.keys():
            aux_confirm_list = []
            for i in data['cliente']:
                nome = i['nome']
                rua = i['rua']
                numero = i['numero']
                complemento = i['complemento']
                telefone = i['telefone']

                if len(Cliente.objects.filter(nome=nome)) == 0:
                    aux_cliente = Cliente(nome=nome, rua=rua, numero=numero, complemento=complemento, telefone=telefone)
                    data_insert_list.append(aux_cliente)
                    aux_confirm_list.append(nome)
                else:
                    error_list.append(nome)

            with atomic():
                for data in data_insert_list:
                    data.save()

            for id in aux_confirm_list:
                aux = Cliente.objects.filter(nome=id).values()
                confirm_list.append(aux[0])

        elif 'restaurante' in data.keys():
            aux_confirm_list = []
            for i in data['restaurante']:
                nome = i['nome']
                rua = i['rua']
                numero = i['numero']
                telefone = i['telefone']

                if len(Restaurante.objects.filter(nome=nome)) == 0:
                    aux_restaurante = Restaurante(nome=nome, rua=rua, numero=numero, telefone=telefone)
                    data_insert_list.append(aux_restaurante)
                    aux_confirm_list.append(nome)
                else:
                    error_list.append(nome)

            with atomic():
                for data in data_insert_list:
                    data.save()

            for id in aux_confirm_list:
                aux = Restaurante.objects.filter(nome=id).values()
                confirm_list.append(aux[0])

        elif 'drone' in data.keys():
            aux_confirm_list = []
            for i in data['drone']:
                nome = i['nome_drone']
                latitude = i['latitude']
                longitude = i['longitude']
                em_voo = i['em_voo']

                if len(Drone.objects.filter(nome_drone=nome)) == 0:
                    aux_drone = Drone(nome_drone=nome, latitude=latitude, longitude=longitude, em_voo=em_voo)
                    data_insert_list.append(aux_drone)
                    aux_confirm_list.append(nome)
                else:
                    error_list.append(nome)

            with atomic():
                for data in data_insert_list:
                    data.save()

            for id in aux_confirm_list:
                aux = Drone.objects.filter(nome_drone=id).values()
                confirm_list.append(aux[0])

        elif 'pedido' in data.keys():
            aux_confirm_list = []
            for i in data['pedido']:
                cliente = i['cliente']
                restaurante = i['restaurante']
                drone = i['drone']
                tempo_entrega = i['tempo_entrega']
                descricao = i['descricao']
                valor = i['valor']
                data_time = datetime.strptime(i['data'] + ' ' + i['hora'], "%d/%m/%Y %H:%M:%S")

                aux_pedido = Pedido(cliente=Cliente.objects.get(nome=cliente),
                                    restaurante=Restaurante.objects.get(nome=restaurante),
                                    drone=Drone.objects.get(nome_drone=drone), tempo_entrega=tempo_entrega,
                                    descricao=descricao, valor_pedido=valor, data_pedido=data_time)
                data_insert_list.append(aux_pedido)
                aux_confirm_list.append({"cliente": cliente, "restaurante": restaurante, "data_time": data_time})

            try:
                with atomic():
                    for data in data_insert_list:
                        data.save()
            except:
                for i in aux_confirm_list:
                    error_list.append(Pedido.objects.filter(Q(cliente=i['cliente']) & Q(restaurante=i['restaurante'])
                                                            & Q(data_pedido=i['data_time'])).values()[0])
                response = {
                    "Message": "Data already exists in the database",
                    "Data": error_list
                }
                return JsonResponse(response)

            for id in aux_confirm_list:
                aux = Pedido.objects.filter(Q(cliente=id['cliente']) & Q(restaurante=id['restaurante'])
                                            & Q(data_pedido=id['data_time'])).values()

                confirm_list.append(aux[0])

    if len(error_list) > 0:
        response = {
            "Message": "Data already exists in the database",
            "Data": error_list
        }
        return JsonResponse(response)

    response = {
        'Message': 'Data inserted in the database',
        "Data": confirm_list
    }

    return JsonResponse(response)

@csrf_exempt
def update(request):
    body_info = request.body.decode()

    if len(body_info) > 0:
        data = json.loads(body_info)

        if 'cliente' in data.keys():
            aux_dict = data['cliente']
            for values in aux_dict:
                Cliente.objects.filter(nome=values['nome']).update(rua=values['rua'])
                Cliente.objects.filter(nome=values['nome']).update(numero=values['numero'])
                Cliente.objects.filter(nome=values['nome']).update(complemento=values['complemento'])
                Cliente.objects.filter(nome=values['nome']).update(telefone=values['telefone'])

            response = {
                'Message': 'Cliente updated',
                'Data': aux_dict
            }

        elif 'restaurante' in data.keys():
            aux_dict = data['restaurante']
            for values in aux_dict:
                Restaurante.objects.filter(nome=values['nome']).update(rua=values['rua'])
                Restaurante.objects.filter(nome=values['nome']).update(numero=values['numero'])
                Restaurante.objects.filter(nome=values['nome']).update(telefone=values['telefone'])

            response = {
                'Message': 'Restaurante updated',
                'Data': aux_dict
            }

        elif 'drone' in data.keys():
            aux_dict = data['drone']
            for values in aux_dict:
                Drone.objects.filter(nome_drone=values['nome_drone']).update(latitude=values['latitude'])
                Drone.objects.filter(nome_drone=values['nome_drone']).update(longitude=values['longitude'])
                Drone.objects.filter(nome_drone=values['nome_drone']).update(em_voo=values['em_voo'])

            response = {
                'Message': 'Drone updated',
                'Data': aux_dict
            }

        elif 'pedido' in data.keys():
            aux_dict = data['pedido']
            for values in aux_dict:
                Pedido.objects.filter(cliente=values['cliente']).update(tempo_entrega=values['tempo_entrega'])
                Pedido.objects.filter(cliente=values['cliente']).update(descricao=values['descricao'])
                Pedido.objects.filter(cliente=values['cliente']).update(valor=values['valor'])
                Pedido.objects.filter(cliente=values['cliente']).update(data=values['data'])
                Pedido.objects.filter(cliente=values['cliente']).update(hora=values['hora'])

            response = {
                'Message': 'Pedido updated',
                'Data': aux_dict
            }

        else:
            response = {'Message': 'Data not updated'}

    return JsonResponse(response)

@csrf_exempt
def delete(request):
    body_info = request.body.decode()

    if len(body_info) > 0:
        data = json.loads(body_info)

        if 'cliente' in data.keys():
            aux_dict = data['cliente']
            for values in aux_dict:
                try:
                    data = Cliente.objects.get(nome=values['nome'])
                    data.delete()
                except:
                    response = {
                        'Message': 'Data not found',
                    }
                    return JsonResponse(response)

            response = {
                'Message': 'Cliente deleted',
                'Data': aux_dict
            }

        elif 'restaurante' in data.keys():
            aux_dict = data['restaurante']
            for values in aux_dict:
                try:
                    data = Restaurante.objects.get(nome=values['nome'])
                    data.delete()
                except:
                    response = {
                        'Message': 'Data not found',
                    }
                    return JsonResponse(response)

            response = {
                'Message': 'Restaurante deleted',
                'Data': aux_dict
            }

        elif 'drone' in data.keys():
            aux_dict = data['drone']
            for values in aux_dict:
                try:
                    data = Drone.objects.get(nome_drone=values['nome_drone'])
                    data.delete()
                except:
                    response = {
                        'Message': 'Data not found',
                    }
                    return JsonResponse(response)

            response = {
                'Message': 'Drone deleted',
                'Data': aux_dict
            }

        elif 'pedido' in data.keys():
            aux_dict = data['pedido']
            for values in aux_dict:
                try:
                    data = Pedido.objects.get(cliente=values['cliente'])
                    data.delete()
                except:
                    response = {
                        'Message': 'Data not found',
                    }
                    return JsonResponse(response)

            response = {
                'Message': 'Pedido deleted',
                'Data': aux_dict
            }

        else:
            response = {'Message': 'Data not deleted'}

    return JsonResponse(response)

@csrf_exempt
def tracking(request):
    body_info = request.body.decode()

    if len(body_info) > 0:
        data = json.loads(body_info)
        tracking_list = []
        if 'tracking' in data.keys():
            for i in data['tracking']:
                cliente = i['cliente']
                restaurante = i['restaurante']
                data_time = datetime.strptime(i['data'] + ' ' + i['hora'], "%d/%m/%Y %H:%M:%S")

                try:
                    info = Pedido.objects.filter(Q(cliente=cliente) & Q(restaurante=restaurante)
                                          & Q(data_pedido=data_time)).values()[0]
                except:
                    response = {'Message': 'Data not found'}
                    return JsonResponse(response)

                tracking_list.append(info)

            response = {
                'Message': 'Tracking',
                'Data': tracking_list
            }

        else:
            response = {'Message': 'Data not found'}

    return JsonResponse(response)