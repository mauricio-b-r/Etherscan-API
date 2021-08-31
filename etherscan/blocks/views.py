from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .methods import IsHex
from .serializers import (
    BlockDetailSerializer,
    TransactionByAddressDetailSerializer,
    TransactionDetailSerializer,
)
from .utils import (
    get_block_by_number_request,
    get_latest_block_number_request,
    get_transaction_by_transaction_hash_request,
    get_transactions_by_address_request,
)


class BlocksApiView(APIView):
    """
    Returns blocks based on latest block or requested more blocks
    """

    def get(self, request, format=None):
        last_block_number_hex = (
            request.query_params.get("last_block_hex")
            or get_latest_block_number_request().json()["result"]
        )
        if not IsHex(last_block_number_hex):
            message = "Block number should be Hex."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        last_block_number_dec = int(last_block_number_hex, 16)
        block_data_list = []
        for x in range(5):
            block_no_hex = hex(last_block_number_dec - x)
            block_data_list.append(
                get_block_by_number_request(block_no_hex).json()["result"]
            )
        block_data_serializer = BlockDetailSerializer(data=block_data_list, many=True)

        if not block_data_serializer.is_valid():
            return Response(
                block_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = block_data_serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


class BlockDetailApiView(APIView):
    """
    Returns blocks information
    """

    def get(self, request, format=None):
        block_number_hex = request.query_params.get("block_no")
        if not IsHex(block_number_hex):
            message = "Block number was not provided or was incorrect."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        block_data = get_block_by_number_request(block_number_hex).json()["result"]
        block_data_serializer = BlockDetailSerializer(data=block_data)

        if not block_data_serializer.is_valid():
            return Response(
                block_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = block_data_serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


class TransactionByHashApiView(APIView):
    """
    Returns transactions information by hash
    """

    def get(self, request, format=None):
        tx_hash = request.query_params.get("tx_hash")
        if not tx_hash:
            message = "Transaction hash was not provided."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        transaction_data = get_transaction_by_transaction_hash_request(
            tx_hash=tx_hash
        ).json()

        if transaction_data.get("error"):
            message = transaction_data["error"]["message"]
            return Response(
                messaage,
                status=status.HTTP_404_NOT_FOUND,
            )

        transaction_data_serializer = TransactionDetailSerializer(
            data=transaction_data["result"]
        )

        if not transaction_data_serializer.is_valid():
            return Response(
                transaction_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = transaction_data_serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


class TransactionsByAddressApiView(APIView):
    """
    Returns transactions information by address
    """

    def get(self, request, format=None):
        address_number = request.query_params.get("address_no")
        page = request.query_params.get("page", 1)

        if not IsHex(address_number):
            message = "Address was not provided or was incorrect."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        block_data = get_transactions_by_address_request(
            address=address_number, page=page
        ).json()
        if block_data["status"] == "0":
            message = f"{block_data['message']} | {block_data['result']}"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        block_data_serializer = TransactionByAddressDetailSerializer(
            data=block_data["result"], many=True
        )
        if not block_data_serializer.is_valid():
            return Response(
                block_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = block_data_serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)
