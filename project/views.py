from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import logout, authenticate, login
from rest_framework import serializers, status
from django.db.models import F
from django.core.mail import EmailMultiAlternatives,EmailMessage
from .tasks import sleepy
from project.models import UserRegister,Product,Product_category,Order,Offer,Order_Product_List
from project.serializers import UserRegisterSerializer,LoginSerializer,ProductCategorySerializer,ProductSerializer,OfferSerializer,Order_Product_ListSerializer,OrderSerializer
# Create your views here.



class RegisterUserView(APIView):
    permission_classes = ([AllowAny])

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully register a new user."
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        qs = UserRegister.objects.get(pk=request.user.id)
        serializer = UserRegisterSerializer(qs)
        return Response({"resp":serializer.data}, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = ([AllowAny])

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        user = authenticate(request, username = request.data['username'], password = request.data['password'])

        if user:
            login(request, user)
            token = Token.objects.filter(user=user).first()
            if token:
                token.delete()
            token = Token.objects.create(user=user)
            user_token = token.key
            data = {
                'username': request.data['username'],
                'auth_token': user_token
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'Username or Password Incorrect!'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [(IsAuthenticated)]
    serailizer_class = LoginSerializer

    def post(self, request):
        token = request.auth
        print(token)
        try:
            token = Token.objects.get(key=token).delete()
            logout(request)
        except:
            return Response({"error": "session1 does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

class ProductCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        qs = Product_category.objects.all()
        serializer = ProductCategorySerializer(qs, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "ProductCategory": serializer.data,
                    "message": " Product-Category created successfully!",
                    "status code": status.HTTP_201_CREATED
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    "success": "False",
                    'status code': status_code,
                    "message": "Product-Category create failed"
                }
                return Response(response, status=status_code)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Product_category.objects.get(pk=pk)
        except Product_category.DoesNotExist:
            return status.HTTP_404_NOT_FOUND

    def patch(self, request, pk):
        qs = self.get_object(pk)
        try:
            serializer = ProductCategorySerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "ProductCategory": serializer.data,
                    "message": "updated successfully!",
                    "status code": status.HTTP_201_CREATED
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    "success": "False",
                    'status code': status_code,
                    "message": "ProductCategory update failed"
                }
                return Response(response, status=status_code)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = self.get_object(pk)
        qs.delete()
        return Response({"message": "Record has been deleted!"}, status=status.HTTP_200_OK)


class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        qs = Product.objects.all()
        serializers = ProductSerializer(qs,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "Product": serializer.data,
                    "message": "created successfully!",
                    "status code": status.HTTP_201_CREATED
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    "success": "False",
                    'status code': status_code,
                    "message": "Product create failed"
                }
                return Response(response, status=status_code)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return status.HTTP_404_NOT_FOUND

    def patch(self, request, pk):
        qs = self.get_object(pk)
        try:
            serializer = ProductSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "Product": serializer.data,
                    "message": "updated successfully!",
                    "status code": status.HTTP_201_CREATED
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    "success": "False",
                    'status code': status_code,
                    "message": "Product update failed"
                }
                return Response(response, status=status_code)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = self.get_object(pk)
        qs.delete()
        return Response({"message": "Record has been deleted!"}, status=status.HTTP_200_OK)


class OrderView(APIView):

    def post(self, request, pk=None):
        # userId = request.data['user_id']
        userId = request.data['user_id']
        product_id = request.data['product_id']
        if userId == request.user.id:
            try:
                registerUserInstance = UserRegister.objects.get(id=userId)
                product = Product.objects.get(product_id=product_id)
            except:
                return Response(request, "User Id or product Id Does not Exists")
        else:
            return Response(request, "Invalid UserId!")
        if registerUserInstance and product:
            order, created = Order.objects.get_or_create(user_id=registerUserInstance, status=False)

            order_Product_List, created = Order_Product_List.objects.get_or_create(order_id=order, product_id=product)
            order_Product_List.product_price = product.product_price
            order_Product_List.quantity = (order_Product_List.quantity + 1)

            order_Product_List.save()
            order_Product_List_data = []
            order_Product_List_data = Order_Product_List.objects.filter(order_id=order, product_id=product).values('id',
                                                                                                                   'quantity').annotate(
                username=F('order_id__user_id__userName'),
                product=F('product_id__product_name')
            )

            for orderDetail in order_Product_List_data:
                print(orderDetail)

            return Response(request, orderDetail)
        else:
            return Response(request, 'User Id or product id Does not Exists')


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        qs = Order.objects.get(pk=pk,user_id=request.user.id)
        serializer = OrderSerializer(qs,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)


class OrederUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self,request,pk):
        try:
            qs = Order.objects.get(pk=pk,user_id=request.user.id)
            try:
                serializer = OrderSerializer(qs, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                        "Order": serializer.data,
                        "message": "updated successfully!",
                        "status code": status.HTTP_201_CREATED
                    }
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    status_code = status.HTTP_406_NOT_ACCEPTABLE
                    response = {
                        "success": "False",
                        'status code': status_code,
                        "message": "Order update failed"
                    }
                    return Response(response, status=status_code)
            except Exception as e:
                return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"msg":"you are not authenticated"},status=status.HTTP_404_NOT_FOUND)

class OrderDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            qs = Order.objects.get(pk=pk,user_id=request.user.id)
            qs.delete()
            return Response({"message": "Record has been deleted!"}, status=status.HTTP_200_OK)
        except:
            return Response({"msg":"you are not authenticated"},status=status.HTTP_404_NOT_FOUND)

class OfferListView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        qs = Offer.objects.all()
        serializer = OfferSerializer(qs, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

#its for admin-side
class OfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = OfferSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "Offer": serializer.data,
                    "message": "created successfully!",
                    "status code": status.HTTP_201_CREATED
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    "success": "False",
                    'status code': status_code,
                    "message": "Offer create failed"
                }
                return Response(response, status=status_code)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return status.HTTP_404_NOT_FOUND

    def patch(self, request, pk):
        qs = self.get_object(pk)
        try:
            serializer = OfferSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "Offer": serializer.data,
                    "message": "updated successfully!",
                    "status code": status.HTTP_201_CREATED
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_406_NOT_ACCEPTABLE
                response = {
                    "success": "False",
                    'status code': status_code,
                    "message": "Offer update failed"
                }
                return Response(response, status=status_code)
        except Exception as e:
            return Response({"message": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        qs = self.get_object(pk)
        qs.delete()
        return Response({"message": "Record has been deleted!"}, status=status.HTTP_200_OK)

class OrderProductListview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        qs = Order_Product_List.objects.get(user_id=request.user.id)
        serializer = Order_Product_ListSerializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class AddToCart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk=None):
        userId = request.data['user_id']
        product_id = request.data['product_id']
        print(request.user.id)
        if userId == request.user.id:
            try:
                registerUserInstance = UserRegister.objects.get(id=userId)
                product = Product.objects.get(product_id=product_id)
            except:
                return Response({"Error":"User Id or product Id Does not Exists!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error":"Invalid UserId!"}, status=status.HTTP_400_BAD_REQUEST)
        if registerUserInstance and product:
            order, created = Order.objects.get_or_create(user_id=registerUserInstance, status=False)

            order_Product_List, created = Order_Product_List.objects.get_or_create(order_id=order, product_id=product)
            order_Product_List.product_price = product.product_price
            order_Product_List.quantity = (order_Product_List.quantity + 1)

            order_Product_List.save()

            order_Product_List_data = Order_Product_List.objects.filter(order_id=order, product_id=product).values('id',
                                                                                                                   'quantity').annotate(
                username=F('order_id__user_id__userName'),
                product=F('product_id__product_name')
            )

            return Response(order_Product_List_data[0], status=status.HTTP_200_OK)
        else:
            return Response({"Error":"User Id or product id Does not Exists"}, status=status.HTTP_400_BAD_REQUEST)

class SendemailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        qs = Order.objects.get(id=pk)
        if qs != 404:
            User = UserRegister.objects.get(id=request.user.id)
            useremail = User.email
            if qs.user_id == request.user.id:
                html_content = '<p style="text-align:right;">username<br>email<br>your order has been cancle</p>'
                subject, from_email , to = 'rr1618600@gmail.com', 'hye', useremail
                msg = EmailMessage(subject, html_content, from_email, [to])
                msg.content_subtype = "html"  # Main content is now text/html
                sleepy(10)
                msg.send()
                return Response({'msg':'email sent'}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Unauthorized!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "user does not exist!"}, status=status.HTTP_404_NOT_FOUND)





    





        






        




