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
            request.data.get("last_block_hex")
            or get_latest_block_number_request().json()["result"]
        )
        if not IsHex(last_block_number_hex):
            message = "Block number should be Hex."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        blocks_info_list = [last_block_number_hex - x for x in range(5)]

        block_data = get_block_by_number_request(last_block_number_hex).json()["result"]
        block_data_serializer = BlockDetailSerializer(data=block_data, many=True)

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
        block_number_hex = request.data.get("block_no")
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
        tx_hash = request.data.get("tx_hash")
        if not tx_hash:
            message = "Transaction hash was not provided."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        print(tx_hash)
        transaction_data = get_transaction_by_transaction_hash_request(
            tx_hash=tx_hash
        ).json()["result"]
        transaction_data_serializer = TransactionDetailSerializer(data=transaction_data)
        return Response(transaction_data, status=status.HTTP_200_OK)
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
        address_number = request.data.get("address_no")
        page = request.data.get("page", 1)

        if not IsHex(address_number):
            message = "Address was not provided or was incorrect."
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        block_data = get_transactions_by_address_request(
            address=address_number, page=page
        ).json()

        if block_data["status"] == 0:
            message = block_data["message"]
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
