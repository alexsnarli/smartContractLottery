## Smart Contract Lottery 

1. Users can enter the lottery with eth based on a USD fee
2. An admin will chose when the lottery is over
3. Lottery will select a random winner


How do we want to test this?
1. `mainnet-fork`
2. `development` with mocks
3. `testnet`



### If running into issues

#### ValueError: Unable to expand environment variable in host setting: 'https://rinkeby.infura.io/v3/$WEB3_INFURA_PROJECT_ID'
Fix: in terminal, run `source .env`