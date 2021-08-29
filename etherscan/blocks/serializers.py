from rest_framework import serializers


class BlockListSerializer(serializers.Serializer):
    block_no = serializers.CharField()


class BlockDetailSerializer(serializers.Serializer):
    baseFeePerGas = serializers.CharField()
    difficulty = serializers.CharField()
    extraData = serializers.CharField()
    gasLimit = serializers.CharField()
    gasUsed = serializers.CharField()
    hash = serializers.CharField()
    logsBloom = serializers.CharField()
    miner = serializers.CharField()
    mixHash = serializers.CharField()
    nonce = serializers.CharField()
    number = serializers.CharField()
    parentHash = serializers.CharField()
    receiptsRoot = serializers.CharField()
    sha3Uncles = serializers.CharField()
    size = serializers.CharField()
    stateRoot = serializers.CharField()
    timestamp = serializers.CharField()
    totalDifficulty = serializers.CharField()
    transactions = serializers.ListField()
    transactionsRoot = serializers.CharField()
    uncles = serializers.ListField()


class TransactionBaseSerializer(serializers.Serializer):
    blockHash = serializers.CharField(allow_blank=True)
    blockNumber = serializers.CharField()
    from_ = serializers.CharField()
    gas = serializers.CharField()
    gasPrice = serializers.CharField()
    hash = serializers.CharField()
    input = serializers.CharField(allow_blank=True)
    nonce = serializers.CharField(allow_blank=True)
    to = serializers.CharField()
    transactionIndex = serializers.CharField()
    value = serializers.CharField()

    def get_fields(self):
        result = super().get_fields()
        from_ = result.pop("from_")
        result["from"] = from_
        return result


class TransactionDetailSerializer(TransactionBaseSerializer):
    type = serializers.CharField()
    v = serializers.CharField()
    r = serializers.CharField()
    s = serializers.CharField()


class TransactionByAddressDetailSerializer(TransactionBaseSerializer):
    timeStamp = serializers.CharField()
    isError = serializers.CharField()
    txreceipt_status = serializers.CharField(allow_blank=True)
    contractAddress = serializers.CharField(allow_blank=True)
    cumulativeGasUsed = serializers.CharField()
    gasUsed = serializers.CharField()
    confirmations = serializers.CharField()
