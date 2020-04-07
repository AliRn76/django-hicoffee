
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from app.models import Item

from app.api.serializers import ItemSerializers, CreateItemSerializers, EditItemSerializers, SellItemSerializers



@api_view(['GET', ])
@permission_classes((AllowAny,))
def show_all_items_view(request):
    data = {}
    # Collecting Data
    items = Item.objects.all()

    # Serialize and Response
    if items:
        serializer = ItemSerializers(items, many=True)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {"response": "there is no item"}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', ])
@permission_classes((AllowAny, ))
def show_item_view(request, item_name):
    try:
        item = Item.objects.get(name=item_name)

    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if item:
        serializer = ItemSerializers(item)
        print(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)





@api_view(['POST', ])
@permission_classes((AllowAny, ))
def add_item_view(request):
    print(request.data)
    serializer = CreateItemSerializers(data=request.data)
    if serializer.is_valid():
        item = Item.objects.create(
            name        = serializer.data.get("name"),
            category    = serializer.data.get("category"),
            number      = serializer.data.get("number"),
            price       = serializer.data.get("price"),
            description = serializer.data.get("description"),
        )
        item.save()

        return Response(data={"response": "ok"}, status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors)



@api_view(['PUT', ])
@permission_classes((AllowAny, ))
def edit_item_view(request):
    serializer = EditItemSerializers(data=request.data)
    if serializer.is_valid():
        # print(serializer.data.get("number"))

        name = serializer.data.get("name")
        number = serializer.data.get("number")
        price = serializer.data.get("price")
        description = serializer.data.get("description")

        item = Item.objects.filter(name=request.data.get("last_name")).update(name=name, number=number, price=price, description=description)

        if item:
            return Response(data={"response": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(data=serializer.errors)



@api_view(['DELETE', ])
@permission_classes((AllowAny, ))
def delete_item_view(request, item_name):
    try:
        item = Item.objects.get(name=item_name)

    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    result = item.delete()

    if result:
        return Response(data={"response": "ok"}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_409_CONFLICT)



@api_view(['POST', ])
@permission_classes((AllowAny, ))
def sell_item_view(request):
    serializer = EditItemSerializers(data=request.data)

    # Check Value
    if serializer.is_valid():
        name = serializer.data.get("name")
        number = serializer.data.get("number")

        try:
            item = Item.objects.get(name=name)

        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check Is Number Positive
        new_number = item.number - number
        print("sell nubmer: " + str(number))
        print("new nubmer: " + str(new_number))
        if new_number < 0:
            print("error, you cant sell that much")
            return Response(data={"response": "error, you cant sell that much"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Update Number Value
        item = Item.objects.filter(name=name).update(number=new_number)

        # Set Response
        if item:
            return Response(data={"response": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(data=serializer.errors)
