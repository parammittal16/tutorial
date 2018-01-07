from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer,UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework import generics
# from snippets.permissions import IsOwnerOrReadOnly


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        print("1111111111111111111")
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    # def pre_save(self, serializer):
    #     serializer.save(owner=self.request.user)
    #
    def pre_save(self, serializer):
        print("10101010101010101010")
        print(self.request.user)
        serializer.owner = self.request.user
        # serializer["owner"]= self.request.user

    def post(self, request, format=None):
        print("222222222222")
        serializer = SnippetSerializer(data=request.data)
        # print(serializer.data)
        print("3")
        # self.pre_save(serializer)
        print(self.request.user)
        # print(serializer.owner)
        serializer.owner = self.request.user
        print("4")
        print(serializer.is_valid())
        print(serializer.data)
        if serializer.is_valid():
            print("5")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes((permissions.AllowAny,))
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class SnippetDetail(APIView,):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
