# Spring Challenge 2023 Strategies

## Wood 2 League Strategy

The Wood 2 League boss is inefficient. On several occassions, it does not choose the closest crystal deposit, nor the most massive deposit. A simple strategy is to (every frame) just select the closest two crystal deposits, create a LINE from the base to those two. The strength of each line should be equal to the value of the crystal deposit. This got us to the next league.

*CellInformation* is a class that holds the data for a singular class. *CellConnections* is a class that holds the data for the connections between the cells. It holds a binary matrix that signifies a connection when the matrix is 1 and no connection when the matrix is 0. The matrix is symmetric because cells[id1][id2] = cells[id2][id1] which makes total sense.

## Wood 1 League Strategy

To be Determined... :)