

import base64
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.core.files.base import ContentFile
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
    data = {}
    last_name = request.data.get("last_name")

    # check is last_name Valid or Not
    if last_name is None:
        data = {'error': 'last_name Is Not Valid'}
        return Response(data=data, status=status.HTTP_406_NOT_ACCEPTABLE)

    # serialize all request data
    serializer = EditItemSerializers(data=request.data)

    # collect serialized data
    if serializer.is_valid():
        name = serializer.data.get("name")
        number = serializer.data.get("number")
        price = serializer.data.get("price")
        description = serializer.data.get("description")
        image_url = serializer.data.get("image_url")
        req_image_url = request.data.get("image_url")

        # get item with last_name
        items = Item.objects.filter(name=last_name)

        # update only one item if we have at least one
        try:
            item = items[0]
        except:
            item = None


        # If We Have at least one item
        if item:
            print("last item.name: ", item.name)
            print("last item.number: ", item.number)
            print("last item.price: ", item.price)
            print("last item.description: ", item.description)
            print("last item.image_url: ", item.image_url)

            # If Value Was Not Null Update It
            if name is not None:
                item.name = name

            if number is not None:
                item.number = number

            if price is not None:
                item.price = price

            if description is not None:
                item.description = description

            if req_image_url is not None:
                item.image_url = req_image_url

            # Update Response, Should be Null
            response = item.save()
            print("response: ", response)

            data = {
                "response": "update successfully",
                'last_name': last_name,
                'name': name,
                'number': number,
                'price': price,
                'description': description,
                'image_url': str(req_image_url),
            }
            return Response(data=data, status=status.HTTP_202_ACCEPTED)

        else:
            data = {
                "error": "item Not Found",
                'last_name': last_name,
                'name': name,
                'number': number,
                'price': price,
                'description': description,
                'image_url': str(req_image_url),
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

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



# baraye in function bayad model change beshe va jadvale sell be soorate joda goone tarif beshe
# in ro ham bayad bezaram baraye ver 2.0
@api_view(['GET', ])
@permission_classes((AllowAny, ))
def show_chart_view():
    pass