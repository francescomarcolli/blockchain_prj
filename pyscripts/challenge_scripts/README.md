# Monitor and interact with the ropsten blockchain

- Script 1, other teams tokens lookup:
    - interacts with other teams contracts
    - read the price history
    - try to guess future price fluctuations
    - make decisions for buying and selling tokens
    - high priority

- Script 2, whale script:
    - interacts with our token challenge
    - launch and monitor PriceOvernight
    - integrate with script 3 to monitor price changes around -+10% 
    - try to win it
    - high priority

- Script 3, challenges script: 
    - monitors the blockchain for direct/team challenge related events
    - tries to win them 
    - high priority

- Script 4, token price management:
    - it interacts with our contract and it changes the price of our token based
   on price history.
    - medium priority

- Script 5, Lender interaction:
  - launch when in need, asks for a loan to the lender contract
  - low priority

- Script 6, opening time exchange: 
  - each day at 18 o'clock changes the opening and closing time of the exchange
  - low priority
