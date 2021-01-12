# Step-by-step guide

## The instruction below show you how to use Tron-Accounts MS with the Tron test network.

1. Create a Tron wallet - https://tronscan.org/#/ . Save your wallet-file in safe place.
2. Install **Tronlink ** Google Chrome extension. Log in using your credentials. 
3. Go to "Settings" in Tronlink. Set up your node to Shasta Testnet.
4. You can receive free test TRX by typing your wallet address here - https://www.trongrid.io/shasta/ . You will need TRX to receive some amount of **Bandwitdth**. It's the same as the gas in Ethereum. You receive 5000 Bandwitdth everyday. You can also freeze TRX to get Bandwitdth.
5. Build a docker container. Then run it with the following command:
`docker run -p <host-port>:5000 --env env.list <container-tag>`
6. Finally you have access to Accounts MS that working with Tron testnet. 

## Autherization
Some of the request should be provided with HTTP Base Auth headers. The login is your wallet address, and the password is your private key. 

## Routes:
**/create-account**

Just creates a new wallet.

Method - **POST**

**/create-token**  

Creates new TRC-10 token. Autherization required.

Method - **POST**

Required fields:
- name(string)
  The token's full name. For example "AQUIX". You should not use space character.
- abbreviation(string)
  The token's short name. For example "AQX". You should not use space character.
- description(string)
- url(string)
  Token's website URL. For example "https://AQUIX.pro/"
- total_supply(number)
  The total amount of tokens to be isssued.
- frozen_amount(number)
  Must be greater or equal to 1.
- frozen_duration(number)
  Must be greater or equal to 2.
- free_bandwidth(number)
  The amount of free Bandwitdth for users to transfer this token. You pay for this.
- free_bandwidth_limit(number)
- sale_period(number)
  The amount of days the token is on sale. For example 365.
- vote_score(number)

You can learn more about TRC-10 issuing here - https://developers.tron.network/docs/issue-trc10

After creating token, you can see it's amount in your Tronklink wallet. There you can find **Token's id**.

**/send-tokens**
Transfers some amount of token to some wallet. Use it for not trx transferring.

Method - **POST**

Required fields:
- to(string)
  The address of the wallet to transfer tokens to
- tokenID(number)
  The token ID of the token to be transferred
- amount(number)
  The amount of tokens to transfer

**/send-trx**
Transfers some amount of trx to some wallet.

Method - **POST**

Required fields:
- to(string)
  The address of the wallet to transfer trx to
- amount(float number)
  The amount of trx to transfer. For example 1.0

**/get-balance**
Gets all tokens balances of given wallet addresses.

Method - **GET**

Required fields:
- addresses(array)
  The addresses which balances will be checked

**NOTE: the request body should be JSON formatted**

## Main Net and Test Net
To use Tron Main Network just set NODES_URL env to https://api.trongrid.io in env.list file and rebuild Docker container. You may also change the current node to main in Tronklink. If you want to use Test Net again type https://api.shasta.trongrid.io.

## Troubleshooting

**500** Internal server error
It may be some Tron lag so you should try to make a request again.
Also this error may appear as a resulf of making request if you didn't provide HTTP Basic Auth headers.

**400** Bad Request
Check if your body fields are the same as required fields specified above.
