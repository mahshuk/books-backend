
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import UpdateAPIView
  
from pages.models import Page, Category, Comment
from api.v1.pages.serializers import PagesSerializer, CategorySerializer,\
DeleteSerializer,EditSerializer, CommentSerializer, PageSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def pages(request):
    instances = Page.objects.filter(is_deleted = False)
    q = request.GET.get("q")
    print(q)

    if q :
        instances = instances.filter(book_name__icontains = q)

    filter = request.GET.get("filter")
    if filter : 
        ids = filter.split(",")
        instances = instances.filter(category__in=ids)
        instances = instances.distinct()

    context = {
        "request" : request
    }
    serializer = PagesSerializer(instances, many= True,context = context)
    response_data = {
        "status_code" : 6000,
        "data" : serializer.data,
        "message" : "succecss"
    }
    return Response (response_data)

 

@api_view(["GET"])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def page(request, id):
    if Page.objects.filter(pk=id).exists():    
        instance = Page.objects.get(pk=id)
        context = {
        "request" : request
        }
        serializer = PageSerializer(instance,context = context)
        response_data = {
            "status_code" : 6000,
            "data" : serializer.data,
            "message" : "success"
        }
        return Response (response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! page not found"
        }
        return Response (response_data)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):

    book_name = request.data["book_name"]
    description = request.data["description"]
    user_name = request.user.first_name
    featured_image = request.data["featured_image"]
    categories_ids = request.data.get("category")

    selected_categories_ids = [int(id) for id in categories_ids.split(',')]
    
    print(selected_categories_ids)

    instance = Page.objects.create(
    book_name = book_name,
    description = description,
    user_name = user_name,
    featured_image = featured_image

    )

    selected_categories = Category.objects.filter(id__in=selected_categories_ids)
    instance.category.add(*selected_categories)

    instance.save()

    response_data = {
            "status_code" : 6000,
            "message" : "sucecss"
        }
    return Response (response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mypost(request):

    instance = Page.objects.filter(user_name = request.user.first_name , is_deleted = False)

    context = {
        "request" : request
    }
    serializer = PageSerializer(instance,many=True,context = context)
    response_data = {
        "status_code" : 6000,
        "data" : serializer.data,
        "message" : "sucecss"
        }
    return Response (response_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def delete(request, id):
    if Page.objects.filter(id=id).exists():
        instance = Page.objects.get(id=id)
        serializer  = DeleteSerializer(instance,data=request.data,partial = True)
        print(instance)
        if serializer.is_valid():
            serializer.save()

        response_data = {
        "status_code" : 6000,
        "message" : "sucecssfully deleted"
        }
        return Response(response_data)
    else:
        response_data = {
        "status_code" : 6001,
        "message" : "post not found"
        }
        return Response(response_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def EditPage(request, id):
    if Page.objects.filter(pk=id).exists():    
        instance = Page.objects.get(pk=id)
        context = {
        "request" : request
        }
        serializer = EditSerializer(instance,context = context)
        response_data = {
            "status_code" : 6000,
            "data" : serializer.data,
            "message" : "sucecss"
        }
        return Response (response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! recipee not found"
        }
        return Response (response_data)



@api_view(["POST"])
@permission_classes([AllowAny])
def edit(request, id):
    if Page.objects.filter(pk=id).exists():
        instance = Page.objects.get(pk=id)

        book_name = request.data.get("book_name", instance.book_name)
        description = request.data.get("description", instance.description)
        featured_image = request.data.get("featured_image", instance.featured_image)

        categories_ids = request.data.get("category")
        selected_categories_ids = [int(id) for id in categories_ids.split(',')]

        instance.book_name = book_name
        instance.description = description
        instance.featured_image = featured_image

        instance.category.clear()
        selected_categories = Category.objects.filter(id__in=selected_categories_ids)
        instance.category.add(*selected_categories)

        instance.save()

        response_data = {
            "status_code": 6000,
            "message": "Successfully updated"
        }
        return Response(response_data)
    else:
        response_data = {
            "status_code": 6001,
            "message": "Post not found"
        }
        return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postLikes(request, id):
    if Page.objects.filter(id=id).exists():
        instance = Page.objects.get(id=id)

        if instance.like.filter(username = request.user.username).exists():
            instance.like.remove(request.user)
            message  = "like removed"

        else:
            instance.like.add(request.user)
            message  = "liked"

        response_data =  {
                "status_code" : 6000,
                "message" : message                                                                                     
            }
        return Response(response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! place not found"
        }
        return Response (response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postComment(request, id):
    if Page.objects.filter(pk=id).exists():
        instance = Page.objects.get(pk=id)
        comment = request.data["comment"]
        username = request.user

        # try:
        #     parent_comment = request.data["parent_comment"]
        # except:
        #     parent_comment = None

        Comment.objects.create(
            comment = comment,
            username = username,
            book = instance
        )
        # if parent_comment:
        #     if Comment.objects.filter(pk=parent_comment).exists():
        #         parent = Comment.objects.get(pk=parent_comment)
        #         instance.parent_comment = parent
        #         instance.save()

        response_data =  {
                "status_code" : 6000,
                "message" : "comment Succesfully posted"                                                                                     
            }
        return Response(response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! book not found"
        }
        return Response (response_data)
    

@api_view(["GET"])
@permission_classes([AllowAny])
def listComment(request, id):
    if Page.objects.filter(pk=id).exists():
        page = Page.objects.get(pk=id)

        instance= Comment.objects.filter(book=page)
        context = {
            "request" : request
        }

        serializer = CommentSerializer(instance,many = True,context= context)

        response_data =  {
                "status_code" : 6000,
                "data" : serializer.data,
                "message" : "comment Succesfully posted"                                                                                     
            }
        return Response(response_data)
    else:
        response_data =  {
            "status_code" : 6001,
            "message" : "oops..! place not found"
        }
        return Response (response_data)
    
