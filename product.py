class Product:
    """
    This is the product class

    The product class tries to retrieve data from a webpage. It fm....

    Attribute:

    """
    def __init__(self, internal_identifier: int):
        self.internal_id = internal_identifier
        self.netprice = 0

    def setnetprice(self, netprice):
        if type(netprice) != float:
            raise IOError("Expecting a float as netprice!")
        self.netprice = netprice

    def 