# blockchain_prj
Stuff about our blockchain project of a decentralized exchange. 

To be able to compile the contracts you have to install OpenZeppelin libraries through the brownie packet manager. 
To do so follow this steps: 

    - activate your conda environment
    - launch the command: 
        brownie pm install OpenZeppelin/openzeppelin-contracts@2.5.0
    - this command will install the git repo of OpenZeppelin in ~/.brownie/packages/
    
After this steps you should be able to compile correctly all the contracts in `contracts/ `

