import { useEthers } from "@usedapp/core"
import helperConfig from "../contracts/helper-config.json"
import networkMapping from "../contracts/chain-info/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../contracts/brownie-config.json"
import dapp from "../public/dapp.png"
import eth from "../public/eth.png"
import dai from "../public/dai.png"

import { StaticImageData } from "next/image"
import { YourWallet } from "./yourWallet/YourWallet"

export type Token = {
    image: StaticImageData
    address: string
    name: string
}

export const Main = () => {
    const { chainId } = useEthers()
    const networkName = chainId ? helperConfig[chainId] : "dev"

    const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "DAPP"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        }, {
            image: dai,
            address: fauTokenAddress,
            name: "DAI"
        },
    ]

    return <YourWallet supportedTokens={supportedTokens} />
}